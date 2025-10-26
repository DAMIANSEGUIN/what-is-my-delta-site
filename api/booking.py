"""
Booking API - Coaching Session Booking Endpoints
Handles appointment creation, cancellation, rescheduling, and availability checks.
"""

import logging
from datetime import datetime, timedelta, time
from typing import Optional, List, Dict
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr, Field
import uuid

from api.storage import get_conn
from api.google_calendar_service import get_calendar_service
from api.paypal_service import get_paypal_service
from api.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/booking", tags=["booking"])


# ============================================================================
# Request/Response Models
# ============================================================================

class AvailabilityRequest(BaseModel):
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD


class AvailabilityResponse(BaseModel):
    available_slots: List[Dict]
    blocked_dates: List[str]


class PromoCodeRequest(BaseModel):
    code: str


class PromoCodeResponse(BaseModel):
    valid: bool
    uses_remaining: int
    message: str


class FreeBookingRequest(BaseModel):
    scheduled_datetime: str  # ISO 8601
    backup_datetime: Optional[str] = None
    user_phone: str
    promo_code: str


class PaidBookingRequest(BaseModel):
    scheduled_datetime: str
    backup_datetime: Optional[str] = None
    user_phone: str
    currency: str  # USD or CAD
    paypal_order_id: str  # Order ID after user approves PayPal payment


class PackagePurchaseRequest(BaseModel):
    currency: str  # USD or CAD
    paypal_order_id: str


class PackageBookingRequest(BaseModel):
    package_id: str
    scheduled_datetime: str
    backup_datetime: Optional[str] = None
    user_phone: str


class CancelAppointmentRequest(BaseModel):
    reason: Optional[str] = None


class RescheduleAppointmentRequest(BaseModel):
    new_datetime: str
    new_backup_datetime: Optional[str] = None


# ============================================================================
# Helper Functions
# ============================================================================

def validate_promo_code(code: str) -> tuple[bool, int]:
    """
    Check if promo code is valid and has uses remaining

    Returns:
        (is_valid, uses_remaining)
    """
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT max_uses, current_uses, active
            FROM promo_codes
            WHERE code = %s
        """, (code,))

        result = cursor.fetchone()

        if not result:
            return (False, 0)

        max_uses, current_uses, active = result

        if not active:
            return (False, 0)

        uses_remaining = max_uses - current_uses

        if uses_remaining <= 0:
            return (False, 0)

        return (True, uses_remaining)


def increment_promo_code_usage(code: str):
    """Increment promo code usage counter"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE promo_codes
            SET current_uses = current_uses + 1
            WHERE code = %s
        """, (code,))
        conn.commit()


def get_blocked_dates(start_date: datetime, end_date: datetime) -> List[str]:
    """Get list of blocked dates in date range"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT blocked_date
            FROM blocked_dates
            WHERE blocked_date BETWEEN %s AND %s
            ORDER BY blocked_date
        """, (start_date.date(), end_date.date()))

        return [row[0].isoformat() for row in cursor.fetchall()]


def check_time_slot_available(requested_datetime: datetime) -> bool:
    """
    Check if requested time slot is available

    Rules:
    - Must be during coach availability hours
    - Must not be on a blocked date
    - Must not conflict with existing appointment
    """
    # Check if date is blocked
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM blocked_dates
            WHERE blocked_date = %s
        """, (requested_datetime.date(),))

        if cursor.fetchone()[0] > 0:
            return False

        # Check coach availability for day of week
        day_of_week = requested_datetime.isoweekday()  # Monday=1, Sunday=7
        requested_time = requested_datetime.time()

        cursor.execute("""
            SELECT COUNT(*)
            FROM coach_availability
            WHERE day_of_week = %s
              AND start_time <= %s
              AND end_time >= %s
              AND active = true
        """, (day_of_week, requested_time, requested_time))

        if cursor.fetchone()[0] == 0:
            return False

        # Check for existing appointments (allow 30min buffer)
        start_window = requested_datetime - timedelta(minutes=30)
        end_window = requested_datetime + timedelta(minutes=30)

        cursor.execute("""
            SELECT COUNT(*)
            FROM appointments
            WHERE scheduled_datetime BETWEEN %s AND %s
              AND status IN ('scheduled', 'rescheduled')
        """, (start_window, end_window))

        if cursor.fetchone()[0] > 0:
            return False

    # Check Google Calendar conflicts
    calendar_service = get_calendar_service()
    busy_times = calendar_service.check_availability(
        start_datetime=start_window,
        end_datetime=end_window
    )

    return len(busy_times) == 0


def create_appointment_record(
    user_id: str,
    google_event_id: str,
    session_type: str,
    scheduled_datetime: datetime,
    user_phone: str,
    user_email: str,
    backup_datetime: Optional[datetime] = None,
    promo_code: Optional[str] = None,
    payment_amount: Optional[float] = None,
    payment_currency: Optional[str] = None,
    paypal_order_id: Optional[str] = None,
    package_id: Optional[str] = None
) -> str:
    """Create appointment record in database"""
    appointment_id = str(uuid.uuid4())

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (
                id, user_id, google_event_id, session_type, promo_code,
                scheduled_datetime, backup_datetime, user_phone, user_email,
                payment_amount, payment_currency, stripe_payment_intent_id,
                package_id, status, payment_status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            appointment_id, user_id, google_event_id, session_type, promo_code,
            scheduled_datetime, backup_datetime, user_phone, user_email,
            payment_amount, payment_currency, paypal_order_id,
            package_id, 'scheduled', 'paid' if payment_amount else None
        ))
        conn.commit()

    return appointment_id


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/availability", response_model=AvailabilityResponse)
async def get_availability(
    start_date: str,
    end_date: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get available time slots for booking

    Returns slots in 30-minute increments during coach availability hours,
    excluding blocked dates and existing appointments.
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Get blocked dates
    blocked = get_blocked_dates(start, end)

    # Get coach availability schedule
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT day_of_week, start_time, end_time
            FROM coach_availability
            WHERE active = true
            ORDER BY day_of_week, start_time
        """)
        availability_schedule = cursor.fetchall()

    # Generate available slots
    available_slots = []
    current_date = start

    while current_date <= end:
        # Skip if date is blocked
        if current_date.date().isoformat() in blocked:
            current_date += timedelta(days=1)
            continue

        # Check if day has availability
        day_of_week = current_date.isoweekday()
        day_schedule = [row for row in availability_schedule if row[0] == day_of_week]

        for schedule in day_schedule:
            start_time, end_time = schedule[1], schedule[2]

            # Generate 30-min slots
            slot_time = datetime.combine(current_date.date(), start_time)
            end_datetime = datetime.combine(current_date.date(), end_time)

            while slot_time < end_datetime:
                # Check if slot is available
                if check_time_slot_available(slot_time):
                    available_slots.append({
                        'datetime': slot_time.isoformat(),
                        'duration_minutes': 30
                    })

                slot_time += timedelta(minutes=30)

        current_date += timedelta(days=1)

    return AvailabilityResponse(
        available_slots=available_slots,
        blocked_dates=blocked
    )


@router.get("/promo/{code}", response_model=PromoCodeResponse)
async def validate_promo(
    code: str,
    current_user: dict = Depends(get_current_user)
):
    """Validate promo code and check remaining uses"""
    is_valid, uses_remaining = validate_promo_code(code)

    if is_valid:
        message = f"Promo code valid! {uses_remaining} uses remaining."
    else:
        message = "Invalid or expired promo code."

    return PromoCodeResponse(
        valid=is_valid,
        uses_remaining=uses_remaining,
        message=message
    )


@router.post("/create-free")
async def create_free_booking(
    request: FreeBookingRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create free coaching session booking with promo code
    """
    user_id = current_user['user_id']
    user_email = current_user['email']

    # Validate promo code
    is_valid, uses_remaining = validate_promo_code(request.promo_code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired promo code")

    # Parse datetime
    try:
        scheduled_dt = datetime.fromisoformat(request.scheduled_datetime)
        backup_dt = datetime.fromisoformat(request.backup_datetime) if request.backup_datetime else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # Check availability
    if not check_time_slot_available(scheduled_dt):
        raise HTTPException(status_code=409, detail="Time slot not available")

    # Create Google Calendar event
    calendar_service = get_calendar_service()
    google_event_id = calendar_service.create_coaching_session(
        user_name=current_user.get('name', user_email.split('@')[0]),
        user_email=user_email,
        user_phone=request.user_phone,
        scheduled_datetime=scheduled_dt,
        session_type='free'
    )

    if not google_event_id:
        raise HTTPException(status_code=500, detail="Failed to create calendar event")

    # Create appointment record
    appointment_id = create_appointment_record(
        user_id=user_id,
        google_event_id=google_event_id,
        session_type='free',
        scheduled_datetime=scheduled_dt,
        backup_datetime=backup_dt,
        user_phone=request.user_phone,
        user_email=user_email,
        promo_code=request.promo_code
    )

    # Increment promo code usage
    increment_promo_code_usage(request.promo_code)

    logger.info(f"Free booking created: {appointment_id} for user {user_id}")

    return {
        'appointment_id': appointment_id,
        'google_event_id': google_event_id,
        'status': 'scheduled',
        'message': 'Free session booked successfully!'
    }


@router.post("/create-paid")
async def create_paid_booking(
    request: PaidBookingRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create paid coaching session booking after PayPal payment approval
    """
    user_id = current_user['user_id']
    user_email = current_user['email']

    # Capture PayPal payment
    paypal_service = get_paypal_service()
    capture_result = paypal_service.capture_order(request.paypal_order_id)

    if not capture_result or capture_result.get('status') != 'COMPLETED':
        raise HTTPException(status_code=400, detail="Payment capture failed")

    # Parse datetime
    try:
        scheduled_dt = datetime.fromisoformat(request.scheduled_datetime)
        backup_dt = datetime.fromisoformat(request.backup_datetime) if request.backup_datetime else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # Check availability
    if not check_time_slot_available(scheduled_dt):
        # Refund payment if slot not available
        capture_id = capture_result.get('capture_id')
        if capture_id:
            paypal_service.refund_capture(capture_id)
        raise HTTPException(status_code=409, detail="Time slot not available. Payment refunded.")

    # Get payment amount from order
    order = paypal_service.get_order(request.paypal_order_id)
    payment_amount = float(order['purchase_units'][0]['amount']['value']) if order else 150.00

    # Create Google Calendar event
    calendar_service = get_calendar_service()
    google_event_id = calendar_service.create_coaching_session(
        user_name=current_user.get('name', user_email.split('@')[0]),
        user_email=user_email,
        user_phone=request.user_phone,
        scheduled_datetime=scheduled_dt,
        session_type='paid_single'
    )

    if not google_event_id:
        # Refund on calendar failure
        capture_id = capture_result.get('capture_id')
        if capture_id:
            paypal_service.refund_capture(capture_id)
        raise HTTPException(status_code=500, detail="Failed to create calendar event. Payment refunded.")

    # Create appointment record
    appointment_id = create_appointment_record(
        user_id=user_id,
        google_event_id=google_event_id,
        session_type='paid_single',
        scheduled_datetime=scheduled_dt,
        backup_datetime=backup_dt,
        user_phone=request.user_phone,
        user_email=user_email,
        payment_amount=payment_amount,
        payment_currency=request.currency,
        paypal_order_id=request.paypal_order_id
    )

    logger.info(f"Paid booking created: {appointment_id} for user {user_id}")

    return {
        'appointment_id': appointment_id,
        'google_event_id': google_event_id,
        'status': 'scheduled',
        'payment_status': 'paid',
        'message': 'Paid session booked successfully!'
    }


@router.get("/my-appointments")
async def get_my_appointments(current_user: dict = Depends(get_current_user)):
    """Get all appointments for current user"""
    user_id = current_user['user_id']

    with get_conn() as conn:
        cursor = conn.cursor()

        # Get upcoming appointments
        cursor.execute("""
            SELECT id, session_type, scheduled_datetime, backup_datetime,
                   user_phone, status, payment_status, payment_amount,
                   payment_currency, created_at
            FROM appointments
            WHERE user_id = %s
              AND scheduled_datetime >= NOW()
              AND status IN ('scheduled', 'rescheduled')
            ORDER BY scheduled_datetime ASC
        """, (user_id,))

        upcoming = []
        for row in cursor.fetchall():
            upcoming.append({
                'id': row[0],
                'session_type': row[1],
                'scheduled_datetime': row[2].isoformat(),
                'backup_datetime': row[3].isoformat() if row[3] else None,
                'user_phone': row[4],
                'status': row[5],
                'payment_status': row[6],
                'payment_amount': float(row[7]) if row[7] else None,
                'payment_currency': row[8],
                'created_at': row[9].isoformat()
            })

        # Get past appointments
        cursor.execute("""
            SELECT id, session_type, scheduled_datetime, status, payment_amount,
                   payment_currency, created_at
            FROM appointments
            WHERE user_id = %s
              AND (scheduled_datetime < NOW() OR status IN ('completed', 'cancelled', 'no_show'))
            ORDER BY scheduled_datetime DESC
            LIMIT 10
        """, (user_id,))

        past = []
        for row in cursor.fetchall():
            past.append({
                'id': row[0],
                'session_type': row[1],
                'scheduled_datetime': row[2].isoformat(),
                'status': row[3],
                'payment_amount': float(row[4]) if row[4] else None,
                'payment_currency': row[5],
                'created_at': row[6].isoformat()
            })

        # Get session packages
        cursor.execute("""
            SELECT id, package_type, sessions_total, sessions_used,
                   purchase_date, amount_paid, currency, status
            FROM session_packages
            WHERE user_id = %s
            ORDER BY purchase_date DESC
        """, (user_id,))

        packages = []
        for row in cursor.fetchall():
            packages.append({
                'id': row[0],
                'package_type': row[1],
                'sessions_total': row[2],
                'sessions_used': row[3],
                'sessions_remaining': row[2] - row[3],
                'purchase_date': row[4].isoformat(),
                'amount_paid': float(row[5]),
                'currency': row[6],
                'status': row[7]
            })

    return {
        'upcoming': upcoming,
        'past': past,
        'packages': packages
    }
