# Google Calendar Booking Integration - Requirements Elicitation
**Date:** 2025-10-25
**Phase:** Requirements Analysis (ELICIT, DON'T INVENT)
**Status:** Awaiting User Clarification

---

## Phase 1: Initial Analysis

### What IS Specified
- **Feature:** Google Calendar booking integration
- **Context:** WIMD/Mosaic platform (career coaching + job search)
- **UI Location:** mosaic_ui/index.html (frontend already has coach interface)
- **Backend:** Railway FastAPI deployment (what-is-my-delta-site-production.up.railway.app)

### What IS NOT Specified
- Booking scenarios (1-on-1 coaching? Group sessions? Events?)
- Calendar provider scope (Google only? Outlook? iCal?)
- User flow (embedded? redirect? modal?)
- Authentication (OAuth? API key? Service account?)
- Data persistence (store appointments in PostgreSQL?)
- Timezone handling
- Conflict prevention / double-booking logic
- Notification/reminder strategy
- Cancellation/rescheduling workflow

---

## Phase 2: Gap Analysis by Technical Dimension

### 1. **User Experience & Behavior**

**GAPS:**
- [ ] Who initiates booking? (User books coach session? Coach schedules with user?)
- [ ] Where does booking UI appear? (Dedicated page? Modal in chat? External link?)
- [ ] Pre-booking flow? (Must be logged in? Trial users allowed?)
- [ ] Post-booking experience? (Confirmation email? Calendar invite? In-app notification?)
- [ ] Mobile responsiveness required?

**ASSUMPTIONS TO VALIDATE:**
- Booking is user-initiated (user schedules time with coach)
- Booking appears as button/link in chat or guide interface
- Requires authentication (no anonymous bookings)

### 2. **Data & State Management**

**GAPS:**
- [ ] Store appointments in database? (Or just create calendar event?)
- [ ] Data schema:
  - User ID
  - Coach ID (if multiple coaches)
  - Appointment datetime
  - Duration (30 min? 60 min? Variable?)
  - Meeting type (video call link? Phone? In-person?)
  - Status (scheduled, completed, cancelled, no-show)
  - Notes/agenda
- [ ] Sync bidirectional? (Update calendar → update DB, vice versa?)
- [ ] Historical appointments tracking?

**ASSUMPTIONS TO VALIDATE:**
- Need to store appointments in PostgreSQL for tracking
- One-way sync (create calendar event, don't sync back)

### 3. **Interfaces & Integration**

**GAPS:**
- [ ] Google Calendar API:
  - Which API endpoints? (Events: insert, list, update, delete?)
  - Authentication method? (OAuth 2.0? Service account?)
  - Refresh token handling?
  - Rate limiting considerations?
- [ ] Video conferencing integration:
  - Auto-generate Google Meet link?
  - Zoom integration?
  - Manual link entry?
- [ ] Email notifications:
  - Send via SendGrid/AWS SES (currently pending)?
  - Or rely on Google Calendar's built-in notifications?

**ASSUMPTIONS TO VALIDATE:**
- Use Google Calendar API with OAuth 2.0
- Auto-generate Google Meet link with event
- Rely on Google Calendar notifications (no custom emails yet)

### 4. **Security & Privacy**

**GAPS:**
- [ ] OAuth consent flow:
  - Request minimal scopes (calendar.events only?)
  - Store tokens securely (encrypted in DB?)
  - Token expiration handling?
- [ ] PII considerations:
  - What appointment data is sensitive?
  - GDPR compliance for EU users?
  - Data retention policy?
- [ ] Authorization:
  - Can users only book their own appointments?
  - Can users cancel/reschedule?
  - Can coaches see all appointments?

**ASSUMPTIONS TO VALIDATE:**
- Use Google OAuth 2.0 with calendar.events scope
- Store encrypted tokens in PostgreSQL
- Users can only manage their own appointments

### 5. **Performance & Scale**

**GAPS:**
- [ ] Expected booking volume? (10/day? 100/day? 1000/day?)
- [ ] Availability lookup performance:
  - Real-time calendar availability check?
  - Pre-computed availability slots?
  - Cache strategy?
- [ ] Acceptable latency? (< 2 seconds for booking confirmation?)

**ASSUMPTIONS TO VALIDATE:**
- Low volume initially (< 50 bookings/day)
- Real-time availability check acceptable
- 2-3 second latency acceptable

### 6. **Business Logic & Rules**

**GAPS:**
- [ ] Availability logic:
  - Fixed coach availability hours? (9AM-5PM EST?)
  - Dynamic availability (coach sets their own hours?)
  - Blackout dates (holidays, PTO)?
- [ ] Booking constraints:
  - Minimum advance notice? (24 hours? 1 week?)
  - Maximum future booking? (30 days? 90 days?)
  - Session duration options? (30/60/90 minutes?)
- [ ] Conflict prevention:
  - Check coach calendar for conflicts?
  - Check user calendar for conflicts?
  - Allow double-booking or block?
- [ ] Cancellation policy:
  - How far in advance can user cancel? (24 hours? 48 hours?)
  - Penalty for late cancellation?
  - Rescheduling rules?

**ASSUMPTIONS TO VALIDATE:**
- Coach has fixed availability (configurable in admin)
- 24-hour minimum advance notice
- 30-day maximum future booking
- 30 or 60-minute sessions
- Block double-booking
- 24-hour cancellation notice

### 7. **Reliability & Operations**

**GAPS:**
- [ ] Error handling:
  - What if Google Calendar API is down?
  - What if user's calendar is full?
  - What if timezone conversion fails?
- [ ] Monitoring:
  - Track booking success rate?
  - Alert on failures?
  - Log API errors?
- [ ] Rollback strategy:
  - If booking fails mid-creation (DB created but calendar failed)?
  - Idempotent operations?

**ASSUMPTIONS TO VALIDATE:**
- Graceful degradation (show error, don't crash)
- Log all API errors to Railway
- Idempotent: check if appointment exists before creating

### 8. **Testing & Validation**

**GAPS:**
- [ ] Test accounts:
  - Need test Google Calendar account?
  - Sandbox environment for OAuth?
- [ ] Test scenarios:
  - Happy path (successful booking)
  - Conflict scenarios
  - Edge cases (leap day, DST transitions, different timezones)
- [ ] User acceptance criteria?

**ASSUMPTIONS TO VALIDATE:**
- Test with personal Google account initially
- Manual testing for MVP
- Automated tests for production

---

## Phase 3: Clarifying Questions (Organized by Stakeholder)

### Questions for Product Owner (User - Damian)

#### Booking Scenarios & User Flow
1. **Who books whom?**
   - Is this user booking time with a coach?
   - Or coach scheduling sessions with user?
   - Or both directions possible?

2. **Where does booking happen in the UI?**
   - Dedicated "Book a Session" button in chat interface?
   - Link in coach guide?
   - Separate /booking page?
   - Modal overlay?

3. **What happens after booking?**
   - User sees confirmation page?
   - Receives email confirmation?
   - Gets calendar invite?
   - Redirect to calendar event?

4. **Session types?**
   - Only 1-on-1 coaching sessions?
   - Group sessions / webinars?
   - Different session types (resume review vs. career strategy vs. interview prep)?

5. **Trial users?**
   - Can free trial users book sessions?
   - Or only paid/authenticated users?
   - Limit on number of sessions?

#### Business Rules
6. **Availability model?**
   - Fixed availability (e.g., weekdays 9AM-5PM EST)?
   - Dynamic availability (coach sets their schedule)?
   - One coach or multiple coaches?

7. **Booking constraints?**
   - Minimum advance notice? (24 hours? Same-day allowed?)
   - Maximum future booking? (How far ahead can users book?)
   - Session duration? (30 min standard? 60 min? User chooses?)

8. **Cancellation/rescheduling?**
   - Users can cancel/reschedule?
   - How far in advance? (24 hours? 48 hours?)
   - Penalty or limit on cancellations?

9. **Video conferencing?**
   - Auto-generate Google Meet link?
   - Use Zoom? (Integration needed?)
   - Phone call? In-person?

10. **Notifications?**
    - Email reminders? (Day before? Hour before?)
    - In-app notifications?
    - SMS reminders? (Out of scope for MVP?)

### Questions for Engineering (Technical Decisions)

#### Integration Approach
11. **Google Calendar API authentication?**
    - OAuth 2.0 with user consent flow? (User authorizes access to their calendar)
    - Service account? (Backend creates events on coach's calendar)
    - API key? (Less secure, not recommended)

12. **Which calendar(s)?**
    - Create event on coach's calendar only?
    - Create event on both user and coach calendars?
    - User doesn't need Google Calendar (just coach does)?

13. **Data persistence?**
    - Store appointments in PostgreSQL database?
    - Or just create calendar event and rely on Google Calendar as source of truth?
    - If storing in DB: full schema or minimal (user ID + event ID)?

14. **Availability lookup?**
    - Real-time API call to check coach calendar for conflicts?
    - Pre-compute availability slots daily?
    - Manual availability configuration (no calendar integration)?

#### Technical Implementation
15. **Frontend framework?**
    - Continue vanilla JS in mosaic_ui/index.html?
    - Or use external library (FullCalendar.js, Calendly embed)?

16. **Backend API endpoints needed?**
    - `POST /booking/create` - Create appointment
    - `GET /booking/availability` - Get available slots
    - `PUT /booking/:id/cancel` - Cancel appointment
    - `PUT /booking/:id/reschedule` - Reschedule appointment
    - `GET /booking/user/:user_id` - List user's appointments

17. **OAuth token storage?**
    - Store in PostgreSQL `oauth_tokens` table?
    - Encrypt tokens at rest?
    - Refresh token handling strategy?

18. **Timezone handling?**
    - Store all times in UTC in database?
    - Display in user's local timezone?
    - Coach's timezone vs. user's timezone?

19. **Error handling?**
    - What if Google Calendar API is unavailable? (Show error message? Fallback to waitlist?)
    - What if user's token expires mid-session? (Re-authenticate?)

20. **Rate limiting?**
    - Google Calendar API has quotas - cache availability lookups?
    - Implement request throttling?

---

## Phase 4: Risk Assessment

### CRITICAL Risks (Block Implementation)

**RISK 1: Scope Ambiguity**
- **Issue:** Don't know who is booking whom, or what user flow looks like
- **Impact:** Can't design UI or API without this clarity
- **Severity:** CRITICAL
- **Mitigation:** User must answer questions 1-5 before proceeding

**RISK 2: OAuth Complexity**
- **Issue:** Google OAuth 2.0 consent flow is complex for users unfamiliar with it
- **Impact:** High drop-off if users confused by Google permission screen
- **Severity:** HIGH
- **Mitigation:** Start with service account (simpler) if only coach calendar needs updating

**RISK 3: Data Consistency**
- **Issue:** If storing in both DB and Google Calendar, sync issues possible
- **Impact:** Appointment created in calendar but not DB (or vice versa)
- **Severity:** HIGH
- **Mitigation:** Use idempotent operations, implement transaction rollback

### HIGH Risks (Needs Assumptions to Proceed)

**RISK 4: Timezone Bugs**
- **Issue:** Timezone conversions are notoriously error-prone
- **Impact:** User books 2PM EST but calendar shows 2PM PST (wrong time)
- **Severity:** HIGH
- **Mitigation:** Store UTC, use robust library (Luxon.js), extensive timezone testing

**RISK 5: Availability Calculation**
- **Issue:** Real-time availability lookup can be slow or inaccurate
- **Impact:** User sees slot as available, but booking fails due to race condition
- **Severity:** MEDIUM
- **Mitigation:** Lock slot during booking process, or pre-compute availability

**RISK 6: Email Service Dependency**
- **Issue:** WIMD currently has no email service (SendGrid/AWS SES pending)
- **Impact:** No confirmation emails unless relying on Google Calendar's emails
- **Severity:** MEDIUM
- **Mitigation:** Accept Google Calendar's built-in emails for MVP

### MEDIUM Risks (Create Uncertainty)

**RISK 7: Mobile UX**
- **Issue:** Calendar picker may not be mobile-friendly in vanilla JS
- **Impact:** Poor mobile booking experience
- **Severity:** MEDIUM
- **Mitigation:** Use mobile-responsive date/time picker library

**RISK 8: API Rate Limits**
- **Issue:** Google Calendar API has quotas (varies by account type)
- **Impact:** Bookings fail if quota exceeded
- **Severity:** MEDIUM
- **Mitigation:** Monitor usage, implement caching, request quota increase if needed

### LOW Risks (Can Resolve Later)

**RISK 9: Cancellation Policy Enforcement**
- **Issue:** No automated enforcement of 24-hour cancellation policy (if required)
- **Impact:** Users cancel last-minute without penalty
- **Severity:** LOW
- **Mitigation:** Acceptable for MVP, add policy enforcement later

**RISK 10: Multi-Coach Scalability**
- **Issue:** If adding multiple coaches later, availability logic becomes complex
- **Impact:** Current design may not scale to multiple coaches
- **Severity:** LOW
- **Mitigation:** Design with single coach for MVP, refactor if needed

---

## Phase 5: Recommendation

### Implementation Readiness: 🔴 BLOCKED - Missing Critical Requirements

**Cannot proceed until clarified:**
1. User flow and booking scenario (questions 1-5)
2. Business rules (questions 6-10)
3. Technical authentication approach (question 11-12)

**Suggested Next Step:**
User (Damian) provides answers to questions 1-12, then we can:
- Design UI mockup
- Define API endpoints
- Create implementation plan with accurate blast radius estimate

---

## Proposed MVP Scope (Pending User Confirmation)

### Assumptions for Initial Implementation (To Be Validated)

**User Flow:**
1. Authenticated user clicks "Book a Coaching Session" in chat interface
2. Calendar picker shows next 30 days
3. User selects date, sees available time slots (30 or 60 min)
4. User confirms booking
5. Appointment created on coach's Google Calendar with Google Meet link
6. User sees confirmation screen with meeting details
7. Both user and coach receive Google Calendar email invitations

**Business Rules:**
- Single coach (Damian's calendar)
- Fixed availability: Weekdays 9AM-5PM EST
- 30 or 60-minute sessions
- 24-hour minimum advance notice
- 30-day maximum future booking
- Users can book 1 session at a time (authenticated users only)
- Cancellation allowed up to 24 hours before

**Technical Implementation:**
- Google Calendar API with service account (coach's calendar only)
- Store appointments in PostgreSQL (`appointments` table)
- Vanilla JS calendar picker UI in mosaic_ui/index.html
- Backend API: `POST /booking/create`, `GET /booking/availability`
- Timezone: Store UTC, display in user's local timezone
- Auto-generate Google Meet link with event
- Rely on Google Calendar's email notifications (no custom emails)

**Out of Scope for MVP:**
- Multi-coach scheduling
- Dynamic availability (coach sets their own hours)
- Recurring appointments
- Group sessions
- Custom email notifications
- Cancellation/rescheduling UI (manual for MVP)
- SMS reminders
- Payment integration

---

## Blast Radius Estimate (Pending Confirmation)

**If MVP scope above is confirmed:**

**Files to Create (3-5 new files):**
- `/api/booking.py` - Booking API endpoints
- `/api/google_calendar.py` - Google Calendar API integration
- `/mosaic_ui/booking.html` - Booking interface (or modal in index.html)
- `/mosaic_ui/booking.js` - Booking frontend logic
- `/data/migrations/add_appointments_table.sql` - Database schema

**Files to Modify (2-3 existing files):**
- `/mosaic_ui/index.html` - Add "Book Session" button/link
- `/api/index.py` - Register booking routes
- `requirements.txt` - Add `google-api-python-client`, `google-auth`

**Estimated Blast Radius: 5-8 files**

**Implementation Time Estimate: 4-6 hours** (assumes requirements confirmed)

---

## Next Action Required

**User (Damian) to provide answers to questions 1-12**, specifically:
- Booking scenario (user books coach? coach books user?)
- UI location (where does booking button appear?)
- Session types and duration
- Availability model (fixed hours? dynamic?)
- Authentication approach (OAuth or service account?)

Once clarified, proceed to implementation with accurate scope and blast radius.

---

**END OF REQUIREMENTS ELICITATION - AWAITING USER INPUT**
