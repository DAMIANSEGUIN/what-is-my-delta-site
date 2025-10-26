# Booking Implementation Plan - Full Feature
**Date:** 2025-10-25
**Scope:** Phase 1 + Phase 2 Combined (Free + Paid Sessions)
**Estimated Time:** 8-10 hours

---

## Final Requirements (All Questions Answered)

### Answers to Follow-Up Questions

1. ✅ **Paid sessions advance notice:** 24 hours minimum
2. ✅ **Phone calls:** Coach calls user (user provides phone number)
3. ✅ **50% cancellation fee:** Auto-charge original card
4. ✅ **SMS notifications:** Wire it but don't trigger (enable in 2 weeks)
5. ✅ **Promo code:** `WIMD25` (single code, 25 uses)
6. ✅ **Backup slot handling:** Auto-email user when coach blocks dates, auto-book backup if provided
7. ✅ **Package sessions:** User pays all upfront ($500), books 1 session at a time

### Payment Integration Cost Analysis

**Stripe Fees:**
- **Transaction fee:** 2.9% + $0.30 per transaction
- **Setup cost:** $0 (free account)
- **Monthly fee:** $0 (pay-per-transaction only)

**Example Costs:**
- $150 USD session → Stripe takes $4.65 → You receive $145.35
- $500 USD package → Stripe takes $14.80 → You receive $485.20

**Total Cost to Run:** $0 monthly, only per-transaction fees

**Verdict:** ✅ **FREE to set up, reasonable transaction fees**

---

## Implementation Plan

### Prerequisites (Before Coding)

**1. Google Cloud Setup (15 minutes)**
- [ ] Go to https://console.cloud.google.com
- [ ] Create new project: "WIMD-Booking"
- [ ] Enable Google Calendar API
- [ ] Create service account: "wimd-booking-service"
- [ ] Download service account JSON key
- [ ] Share your Google Calendar with service account email (Editor permission)

**2. Stripe Setup (10 minutes)**
- [ ] Go to https://stripe.com
- [ ] Create account (free)
- [ ] Get API keys: Dashboard → Developers → API keys
  - Publishable key (starts with `pk_test_...`)
  - Secret key (starts with `sk_test_...`)
- [ ] Enable test mode for development
- [ ] Add products:
  - Single Session: $150 USD / $150 CAD
  - 3-Session Package: $500 USD / $500 CAD

**3. Environment Variables**
- [ ] Add to Railway (or .env for local):
```bash
# Google Calendar
GOOGLE_SERVICE_ACCOUNT_KEY='{"type":"service_account",...}'
COACH_GOOGLE_CALENDAR_ID='primary'
COACH_PHONE_NUMBER='+1234567890'
COACH_EMAIL='your@email.com'

# Stripe
STRIPE_PUBLISHABLE_KEY='pk_test_...'
STRIPE_SECRET_KEY='sk_test_...'
STRIPE_WEBHOOK_SECRET='whsec_...'  # Get after creating webhook

# SMS (Twilio - wire but don't trigger)
TWILIO_ACCOUNT_SID='...'
TWILIO_AUTH_TOKEN='...'
TWILIO_PHONE_NUMBER='+1...'
TWILIO_SMS_ENABLED='false'  # Set to 'true' in 2 weeks
```

---

## File Structure

### New Files (10 files)

```
/api/booking.py                      # Booking API endpoints
/api/google_calendar_service.py     # Google Calendar integration
/api/stripe_service.py               # Stripe payment integration
/api/notification_service.py         # Email/SMS/in-app notifications
/mosaic_ui/js/booking-modal.js       # Booking modal logic
/mosaic_ui/css/booking-modal.css     # Modal styling
/data/migrations/001_add_booking_tables.sql
/data/migrations/002_seed_promo_code.sql
/data/migrations/003_seed_coach_availability.sql
/scripts/test_booking.py             # Test script
```

### Modified Files (4 files)

```
/mosaic_ui/index.html                # Add booking button + modal HTML
/api/index.py                        # Register booking routes
/requirements.txt                    # Add dependencies
/netlify.toml                        # Add booking API redirect
```

---

## Database Schema

### Tables to Create

```sql
-- 1. Appointments
CREATE TABLE appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  google_event_id VARCHAR(255) UNIQUE NOT NULL,

  -- Session details
  session_type VARCHAR(50) NOT NULL, -- 'free', 'paid_single', 'paid_package'
  promo_code VARCHAR(50),
  scheduled_datetime TIMESTAMPTZ NOT NULL,
  backup_datetime TIMESTAMPTZ,
  duration_minutes INTEGER DEFAULT 30,

  -- Contact info
  user_phone VARCHAR(20) NOT NULL,
  user_email VARCHAR(255) NOT NULL,

  -- Status tracking
  status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'completed', 'cancelled', 'no_show', 'rescheduled'

  -- Payment
  payment_status VARCHAR(50), -- 'pending', 'paid', 'refunded', 'partial_refund'
  payment_amount DECIMAL(10,2),
  payment_currency VARCHAR(3), -- 'USD' or 'CAD'
  stripe_payment_intent_id VARCHAR(255),
  package_id UUID REFERENCES session_packages(id),

  -- Reschedule tracking
  reschedule_count INTEGER DEFAULT 0,
  cancellation_fee_applied BOOLEAN DEFAULT FALSE,
  cancellation_fee_amount DECIMAL(10,2),

  -- Notifications
  notification_preferences JSONB DEFAULT '{"email": true, "inapp": true, "sms": false}'::jsonb,

  -- Preparation notes
  preparation_notes TEXT DEFAULT 'Prepare for your session by completing the AI prompts from your previous conversations as far as you are able.',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  cancelled_at TIMESTAMPTZ
);

-- 2. Promo Codes
CREATE TABLE promo_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(50) UNIQUE NOT NULL,
  max_uses INTEGER DEFAULT 25,
  current_uses INTEGER DEFAULT 0,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Coach Availability (default schedule)
CREATE TABLE coach_availability (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  day_of_week INTEGER NOT NULL, -- 0=Sunday, 1=Monday, ..., 6=Saturday
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  timezone VARCHAR(50) DEFAULT 'America/Toronto',
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Blocked Dates (PTO, holidays, etc.)
CREATE TABLE blocked_dates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  blocked_date DATE NOT NULL,
  reason VARCHAR(255),
  notify_affected_users BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Session Packages
CREATE TABLE session_packages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  package_type VARCHAR(50) NOT NULL, -- 'three_pack'
  sessions_total INTEGER NOT NULL, -- 3
  sessions_used INTEGER DEFAULT 0,
  sessions_remaining INTEGER GENERATED ALWAYS AS (sessions_total - sessions_used) STORED,

  -- Payment
  purchase_date TIMESTAMPTZ DEFAULT NOW(),
  stripe_payment_intent_id VARCHAR(255) UNIQUE,
  amount_paid DECIMAL(10,2) NOT NULL,
  currency VARCHAR(3) NOT NULL,

  -- Status
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'expired', 'refunded'
  expires_at TIMESTAMPTZ, -- Optional: packages expire after X months

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Notification Log (track what was sent)
CREATE TABLE notification_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  appointment_id UUID REFERENCES appointments(id) ON DELETE CASCADE,
  notification_type VARCHAR(50) NOT NULL, -- 'email', 'sms', 'inapp'
  notification_event VARCHAR(50) NOT NULL, -- 'booking_confirmed', 'reminder_24h', 'cancellation', 'reschedule'
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'sent', -- 'sent', 'failed', 'delivered'
  error_message TEXT
);

-- Indexes for performance
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
CREATE INDEX idx_appointments_scheduled_datetime ON appointments(scheduled_datetime);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_session_packages_user_id ON session_packages(user_id);
CREATE INDEX idx_blocked_dates_date ON blocked_dates(blocked_date);

-- Seed promo code
INSERT INTO promo_codes (code, max_uses, active) VALUES ('WIMD25', 25, true);

-- Seed default coach availability (example: Mon-Fri 9AM-5PM EST)
-- You'll need to customize these hours
INSERT INTO coach_availability (day_of_week, start_time, end_time, timezone) VALUES
  (1, '09:00:00', '17:00:00', 'America/Toronto'), -- Monday
  (2, '09:00:00', '17:00:00', 'America/Toronto'), -- Tuesday
  (3, '09:00:00', '17:00:00', 'America/Toronto'), -- Wednesday
  (4, '09:00:00', '17:00:00', 'America/Toronto'), -- Thursday
  (5, '09:00:00', '17:00:00', 'America/Toronto'); -- Friday
```

---

## API Endpoints

### Backend Routes (`/api/booking.py`)

```python
# Availability
GET  /booking/availability
  → Returns: { available_slots: [{ datetime, duration }], blocked_dates: [...] }
  → Query params: start_date, end_date
  → Auth: Required

# Promo Code Validation
GET  /booking/promo/:code
  → Returns: { valid: bool, uses_remaining: int }
  → Auth: Required

# Create Booking (Free)
POST /booking/create-free
  → Body: { scheduled_datetime, backup_datetime, user_phone, promo_code }
  → Returns: { appointment_id, google_event_id, confirmation }
  → Auth: Required

# Create Booking (Paid - Single)
POST /booking/create-paid-single
  → Body: { scheduled_datetime, backup_datetime, user_phone, currency, stripe_payment_intent_id }
  → Returns: { appointment_id, google_event_id, confirmation }
  → Auth: Required

# Create Booking (Paid - Package)
POST /booking/create-paid-package
  → Body: { currency, stripe_payment_intent_id }
  → Returns: { package_id, sessions_remaining }
  → Auth: Required

# Book Session from Package
POST /booking/use-package-session
  → Body: { package_id, scheduled_datetime, backup_datetime, user_phone }
  → Returns: { appointment_id, google_event_id, sessions_remaining }
  → Auth: Required

# User's Appointments
GET  /booking/my-appointments
  → Returns: { upcoming: [...], past: [...], packages: [...] }
  → Auth: Required

# Cancel Appointment
PUT  /booking/:id/cancel
  → Body: { reason }
  → Returns: { cancelled: bool, fee_applied: bool, refund_amount }
  → Auth: Required (must own appointment)

# Reschedule Appointment
PUT  /booking/:id/reschedule
  → Body: { new_datetime, new_backup_datetime }
  → Returns: { rescheduled: bool, fee_applied: bool }
  → Auth: Required (must own appointment)

# Stripe Webhook (payment confirmation)
POST /booking/stripe-webhook
  → Handles: payment_intent.succeeded, payment_intent.failed
  → Auth: Stripe signature verification

# Admin: Block Date
POST /booking/admin/block-date
  → Body: { date, reason }
  → Returns: { blocked: bool, users_notified: int }
  → Auth: Admin only

# Admin: List All Bookings
GET  /booking/admin/appointments
  → Returns: { appointments: [...] }
  → Query params: status, start_date, end_date
  → Auth: Admin only
```

---

## Implementation Steps

### Step 1: Database Setup (30 minutes)

Create migration files and run them on PostgreSQL.

### Step 2: Google Calendar Service (1 hour)

`/api/google_calendar_service.py`:
- Load service account credentials
- Create event with phone call details
- Update event (reschedule)
- Delete event (cancellation)
- List events (check availability conflicts)

### Step 3: Stripe Service (1.5 hours)

`/api/stripe_service.py`:
- Create PaymentIntent for single session ($150)
- Create PaymentIntent for package ($500)
- Handle currency (USD vs CAD based on user location)
- Process refunds (50% for late cancellation)
- Webhook handler for payment confirmation

### Step 4: Notification Service (1 hour)

`/api/notification_service.py`:
- Email: Booking confirmation, reminder, cancellation
- SMS: Wire Twilio but disable (`TWILIO_SMS_ENABLED=false`)
- In-app: Create notification record in database
- Template system for messages

### Step 5: Booking API (2 hours)

`/api/booking.py`:
- Implement all endpoints listed above
- Validation logic (promo code, availability, payment)
- Transaction handling (payment → calendar → database)
- Rollback on failure

### Step 6: Frontend Modal (2.5 hours)

`/mosaic_ui/js/booking-modal.js` + `/mosaic_ui/css/booking-modal.css`:
- Modal HTML structure
- Session type selector (Free / Paid Single / Paid Package)
- Promo code input (shows if Free selected)
- Calendar date picker (next 90 days, blocked dates grayed out)
- Time slot selector (based on availability)
- Backup slot selector
- Phone number input
- Notification preferences checkboxes
- Stripe Elements integration (payment form)
- Confirmation screen

### Step 7: Testing (1.5 hours)

- Test promo code validation
- Test free booking flow
- Test paid single booking flow
- Test package purchase + booking from package
- Test cancellation with fee calculation
- Test reschedule logic
- Test backup slot email trigger

### Step 8: Deployment (1 hour)

- Add environment variables to Railway
- Run database migrations
- Deploy backend
- Deploy frontend (Netlify auto-deploy)
- Set up Stripe webhook endpoint
- Test on production

---

## Cost Breakdown

### Free Services
- **Google Calendar API:** Free (up to 1M requests/day)
- **Stripe account:** Free setup
- **Railway PostgreSQL:** Free tier (sufficient for bookings)

### Paid/Transaction-Based
- **Stripe fees:** 2.9% + $0.30 per transaction
  - $150 session = $4.65 fee
  - $500 package = $14.80 fee
- **Twilio SMS (optional, disabled for 2 weeks):** $0.0075 per SMS
  - 100 SMS = $0.75
  - Recommend: Enable only if high demand

### Total Setup Cost: $0
### Monthly Cost: $0 (only transaction fees)

---

## Next Actions

### Immediate (You Need to Do)
1. **Google Cloud:** Create project, enable Calendar API, create service account, share calendar
2. **Stripe:** Create account, get test API keys
3. **Railway:** Add environment variables

### Then I Will
1. Create database migrations
2. Implement backend services (Google Calendar, Stripe, Notifications)
3. Implement booking API endpoints
4. Implement frontend modal
5. Test end-to-end
6. Deploy to production

**Ready to start?**
- Share service account JSON key (as environment variable format)
- Share Stripe API keys (test mode first)
- Confirm your Google Calendar email
- Confirm your phone number (for calendar invites)

---

**Estimated Total Time: 8-10 hours**
**Estimated Total Cost: $0 setup + transaction fees**

