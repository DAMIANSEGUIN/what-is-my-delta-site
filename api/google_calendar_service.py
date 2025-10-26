"""
Google Calendar Service - Coaching Session Management
Handles creation, updating, and deletion of coaching sessions in Google Calendar.
Uses service account authentication for server-to-server access.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# Google Calendar API (will be initialized with credentials)
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    logger.warning("Google Calendar libraries not installed. Install with: pip install google-api-python-client google-auth")


class GoogleCalendarService:
    """Service for managing coaching sessions in Google Calendar"""

    def __init__(self):
        self.service = None
        self.calendar_id = os.getenv('COACH_GOOGLE_CALENDAR_ID', 'primary')
        self.coach_email = os.getenv('COACH_EMAIL')
        self.coach_phone = os.getenv('COACH_PHONE_NUMBER')
        self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Calendar API service with service account credentials"""
        if not GOOGLE_CALENDAR_AVAILABLE:
            logger.error("Google Calendar libraries not available")
            return

        try:
            # Get service account key from environment variable
            service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY')

            if not service_account_json:
                logger.warning("GOOGLE_SERVICE_ACCOUNT_KEY not set. Calendar integration will be mocked.")
                return

            # Parse JSON key
            service_account_info = json.loads(service_account_json)

            # Create credentials
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/calendar']
            )

            # Build Calendar API service
            self.service = build('calendar', 'v3', credentials=credentials)
            logger.info("Google Calendar service initialized successfully")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid GOOGLE_SERVICE_ACCOUNT_KEY JSON: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Calendar service: {e}")

    def create_coaching_session(
        self,
        user_name: str,
        user_email: str,
        user_phone: str,
        scheduled_datetime: datetime,
        duration_minutes: int = 30,
        session_type: str = 'free',
        preparation_notes: str = None
    ) -> Optional[str]:
        """
        Create a coaching session event in Google Calendar

        Args:
            user_name: Name of the user booking the session
            user_email: User's email for calendar invite
            user_phone: User's phone number (coach will call)
            scheduled_datetime: When the session is scheduled
            duration_minutes: Session duration (default 30)
            session_type: 'free', 'paid_single', or 'paid_package'
            preparation_notes: Optional preparation instructions

        Returns:
            Google Calendar event ID if successful, None if failed
        """
        if not self.service:
            # Mock mode for development without credentials
            mock_event_id = f"mock_event_{datetime.now().timestamp()}"
            logger.warning(f"Calendar service not initialized. Returning mock event ID: {mock_event_id}")
            return mock_event_id

        try:
            end_datetime = scheduled_datetime + timedelta(minutes=duration_minutes)

            # Default preparation notes
            if not preparation_notes:
                preparation_notes = "Prepare for your session by completing the AI prompts from your previous conversations as far as you are able."

            # Build event description
            description_parts = [
                f"Coaching Session with {user_name}",
                "",
                f"📞 Call: {user_phone}",
                f"📧 Email: {user_email}",
                "",
                "📝 Preparation:",
                preparation_notes,
                "",
                "🔔 Cancellation Policy:",
                "- Free sessions: No penalty",
                "- Paid sessions: 48-hour notice required",
                "- Late cancellation: 50% fee after first reschedule",
                "",
                f"Session Type: {session_type}",
            ]

            description = "\n".join(description_parts)

            # Create event
            event = {
                'summary': f'Coaching Session - {user_name}',
                'description': description,
                'start': {
                    'dateTime': scheduled_datetime.isoformat(),
                    'timeZone': 'America/Toronto',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/Toronto',
                },
                'attendees': [
                    {'email': user_email, 'displayName': user_name},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 24 hours before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
                'conferenceData': None,  # No video conferencing (phone only)
            }

            # Insert event
            event_result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='all'  # Send email invites to attendees
            ).execute()

            event_id = event_result['id']
            logger.info(f"Created calendar event {event_id} for {user_name} at {scheduled_datetime}")
            return event_id

        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            return None

    def update_coaching_session(
        self,
        event_id: str,
        new_datetime: datetime,
        duration_minutes: int = 30
    ) -> bool:
        """
        Reschedule a coaching session

        Args:
            event_id: Google Calendar event ID
            new_datetime: New scheduled time
            duration_minutes: Session duration

        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.warning(f"Calendar service not initialized. Mock rescheduling event {event_id}")
            return True

        try:
            # Get existing event
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()

            # Update datetime
            end_datetime = new_datetime + timedelta(minutes=duration_minutes)
            event['start'] = {
                'dateTime': new_datetime.isoformat(),
                'timeZone': 'America/Toronto',
            }
            event['end'] = {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'America/Toronto',
            }

            # Update event
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event,
                sendUpdates='all'  # Notify attendees of change
            ).execute()

            logger.info(f"Rescheduled event {event_id} to {new_datetime}")
            return True

        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to reschedule event: {e}")
            return False

    def cancel_coaching_session(self, event_id: str, cancellation_reason: str = None) -> bool:
        """
        Cancel a coaching session

        Args:
            event_id: Google Calendar event ID
            cancellation_reason: Optional reason for cancellation

        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.warning(f"Calendar service not initialized. Mock cancelling event {event_id}")
            return True

        try:
            # Get existing event to update description with cancellation reason
            if cancellation_reason:
                event = self.service.events().get(
                    calendarId=self.calendar_id,
                    eventId=event_id
                ).execute()

                event['description'] = f"{event.get('description', '')}\n\n❌ CANCELLED\nReason: {cancellation_reason}"

                self.service.events().update(
                    calendarId=self.calendar_id,
                    eventId=event_id,
                    body=event,
                    sendUpdates='all'
                ).execute()

            # Delete event
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
                sendUpdates='all'  # Notify attendees of cancellation
            ).execute()

            logger.info(f"Cancelled event {event_id}")
            return True

        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to cancel event: {e}")
            return False

    def check_availability(
        self,
        start_datetime: datetime,
        end_datetime: datetime
    ) -> List[Dict]:
        """
        Check for conflicts in coach's calendar

        Args:
            start_datetime: Start of availability check window
            end_datetime: End of availability check window

        Returns:
            List of busy time slots
        """
        if not self.service:
            logger.warning("Calendar service not initialized. Returning empty availability")
            return []

        try:
            # Query for busy times using freebusy API
            body = {
                "timeMin": start_datetime.isoformat(),
                "timeMax": end_datetime.isoformat(),
                "timeZone": "America/Toronto",
                "items": [{"id": self.calendar_id}]
            }

            freebusy_result = self.service.freebusy().query(body=body).execute()
            busy_times = freebusy_result['calendars'][self.calendar_id]['busy']

            logger.info(f"Found {len(busy_times)} busy slots between {start_datetime} and {end_datetime}")
            return busy_times

        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to check availability: {e}")
            return []


# Singleton instance
_calendar_service = None

def get_calendar_service() -> GoogleCalendarService:
    """Get or create singleton GoogleCalendarService instance"""
    global _calendar_service
    if _calendar_service is None:
        _calendar_service = GoogleCalendarService()
    return _calendar_service
