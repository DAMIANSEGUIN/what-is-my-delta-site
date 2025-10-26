# Google Calendar Booking - Finalized Requirements
**Date:** 2025-10-25
**Status:** ✅ Requirements Confirmed - Ready for Implementation

---

## Requirements Summary (User Responses)

### Most Critical (1-5)

**1. Who books whom?**
- ✅ **User books coach** (Damian)

**2. Where in UI?**
- ⚠️ **User asked for recommendation:** "link pop up? Or just a link? Suggestion?"
- **SSE Recommendation:** Modal overlay (better UX, keeps user in context)
  - Button in chat interface: "Schedule Coaching Session"
  - Clicking opens modal with calendar picker
  - Alternative: Could also add link in coach guide sidebar
  - Benefits: No page navigation, seamless flow, mobile-friendly

**3. Post-booking experience?**
- ✅ **Calendar invite** with:
  - 30-minute appointment
  - Note: "Prepare for session by completing AI prompts from your previous conversations as far as you're able"
  - Phone call instructions (number provided in invite)
  - Cancellation policy reminder (48 hours)

**4. Session types?**
- ✅ **1-on-1 only**

**5. Trial user access?**
- ✅ **Free trial with code:**
  - Requires promo code to book free session
  - Limit: 25 free sessions total (system-wide cap)
  - Duration: 30 minutes

### Business Rules (6-10)

**6. Availability model?**
- ✅ **Fixed hours with admin flexibility:**
  - Coach (Damian) sets fixed availability hours
  - Coach can block specific dates (PTO, holidays)
  - User selects primary slot + backup slot (in case coach cancels)

**7. Booking constraints?**
- ✅ **Advance notice:**
  - Block availability 2 days in advance from current date
  - Exception: Paid sessions can book closer (need to clarify: same-day? 24 hours?)
  - **QUESTION:** Paid sessions - how far in advance minimum? Same day? 24 hours?
- ✅ **Future booking limit:** Not specified - **Recommend: 90 days max**
- ✅ **Duration:** 30 minutes (all sessions)

**8. Cancellation policy?**
- ✅ **Free session:** No penalty
- ✅ **Paid session:**
  - 48-hour advance notice required
  - One free reschedule allowed
  - After first reschedule: 50% fee for subsequent reschedules or cancellations
  - **QUESTION:** How to collect 50% penalty? Charge original payment method? Require upfront for next booking?

**9. Video conferencing?**
- ✅ **Phone call only**
  - No video, Zoom, or WhatsApp
  - Calendar invite includes phone number to call
  - **QUESTION:** Display your phone number in invite? Or user provides their number and you call them?

**10. Notifications?**
- ✅ **User choice:**
  - Email (Google Calendar default)
  - In-app notification (WIMD platform)
  - SMS (optional)
  - User selects preferences during booking or in settings

### Pricing (New Requirement)

**Free Sessions:**
- Requires promo code
- 30 minutes
- 25 total available (first-come, first-served)

**Paid Sessions:**
- **Single session:**
  - $150 USD (US customers)
  - $150 CAD (Canadian customers)
  - 30 minutes
- **Package (3 sessions):**
  - $500 USD (outside Canada)
  - $500 CAD (Canada)
  - 3 x 30-minute sessions
- **Payment required:** Advance payment before session(s)

**CRITICAL NEW REQUIREMENT:** Payment integration (Stripe recommended)

### Technical (11-12)

**11. Authentication approach?**
- ⚠️ **User deferred to SSE:** "you tell me"
- **SSE Recommendation:** **Service Account** (simpler for MVP)
  - Backend creates events on coach's Google Calendar using service account
  - No OAuth consent flow for users (better UX)
  - Coach (Damian) grants service account access to calendar once
  - User doesn't need Google Calendar (just coach does)
  - Alternative: OAuth if you want users to also add event to their calendar (adds complexity)

**12. Which calendar(s)?**
- ⚠️ **User asked:** "Shared calendar? User and coach? What is ideal? What is easier for me? Privacy issues, I do not want other users to see what is in my calendar."
- **SSE Recommendation:** **Coach calendar only, NO sharing with users**
  - Create event on coach's (Damian's) Google Calendar
  - Users see their own booked appointments in WIMD dashboard (stored in PostgreSQL)
  - Users do NOT see coach's full calendar (privacy maintained)
  - Optional: Send calendar invite to user's email (they can add to their own calendar if they want)
  - Benefits: Privacy, simplicity, coach controls availability

---

## Implementation Decisions (SSE Recommendations)

### UI Design: Modal Overlay ✅

**Rationale:**
- Better UX (no page navigation)
- Keeps user in coaching context
- Mobile-friendly
- Modern, professional feel

**Flow:**
1. User clicks "Schedule Coaching Session" button in chat or guide
2. Modal overlay appears with:
   - Session type selector (Free with code / Paid single / Paid package)
   - Promo code input (if free selected)
   - Calendar picker (next 90 days, blocked dates grayed out)
   - Primary time slot selection
   - Backup time slot selection
   - Phone number input (who coach calls)
   - Notification preferences
   - Payment (if paid session selected)
3. User confirms
4. Payment processed (if paid)
5. Appointment created on coach's calendar
6. Confirmation screen with:
   - Appointment details
   - Preparation instructions
   - Cancellation policy
   - Email confirmation sent

### Authentication: Service Account ✅

**Rationale:**
- Simpler for MVP (no OAuth consent flow)
- Better UX (users don't need Google account)
- Coach grants access once, works forever
- Sufficient for single coach use case

**Setup Required:**
1. Create Google Cloud project
2. Enable Google Calendar API
3. Create service account
4. Download service account key (JSON)
5. Share coach's calendar with service account email
6. Store service account key in Railway environment variable

### Calendar Strategy: Coach Only ✅

**Rationale:**
- Privacy (users can't see coach's full calendar)
- Simplicity (one source of truth)
- User sees their appointments in WIMD dashboard
- Optional: Send email invite to user (they can add to their own calendar)

**Database Schema:**
```sql
CREATE TABLE appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  google_event_id VARCHAR(255) UNIQUE NOT NULL,
  session_type VARCHAR(50) NOT NULL, -- 'free', 'paid_single', 'paid_package'
  promo_code VARCHAR(50), -- if free session
  scheduled_datetime TIMESTAMPTZ NOT NULL,
  backup_datetime TIMESTAMPTZ, -- user's backup slot
  duration_minutes INTEGER DEFAULT 30,
  user_phone VARCHAR(20) NOT NULL,
  status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'completed', 'cancelled', 'no_show'
  payment_status VARCHAR(50), -- 'pending', 'paid', 'refunded', 'partial_refund'
  payment_amount DECIMAL(10,2),
  payment_currency VARCHAR(3),
  stripe_payment_id VARCHAR(255),
  reschedule_count INTEGER DEFAULT 0,
  cancellation_fee_applied BOOLEAN DEFAULT FALSE,
  notification_preferences JSONB, -- {email: true, inapp: true, sms: false}
  preparation_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE promo_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(50) UNIQUE NOT NULL,
  max_uses INTEGER DEFAULT 25,
  current_uses INTEGER DEFAULT 0,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE coach_availability (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  day_of_week INTEGER NOT NULL, -- 0=Sunday, 1=Monday, etc.
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  timezone VARCHAR(50) DEFAULT 'America/Toronto',
  active BOOLEAN DEFAULT TRUE
);

CREATE TABLE blocked_dates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL,
  reason VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE session_packages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  package_type VARCHAR(50) NOT NULL, -- 'three_pack'
  sessions_purchased INTEGER NOT NULL,
  sessions_used INTEGER DEFAULT 0,
  purchase_date TIMESTAMPTZ DEFAULT NOW(),
  stripe_payment_id VARCHAR(255),
  amount_paid DECIMAL(10,2),
  currency VARCHAR(3)
);
```

### Payment Integration: Stripe ✅

**Rationale:**
- Industry standard
- Simple integration
- Supports USD and CAD
- Handles refunds (for 50% penalty)
- PCI compliant (don't store card details)

**Flow:**
1. User selects paid session
2. Stripe Checkout modal appears
3. User enters card details (Stripe handles)
4. Payment processed
5. On success: create appointment
6. On failure: show error, don't create appointment

**Required:**
- Stripe account
- Stripe API keys (publishable + secret)
- Stripe Python SDK

---

## Clarifying Questions (Still Needed)

### 1. Paid Session Advance Notice
**Question:** Paid sessions can book closer than 2 days. How close?
- [ ] Same-day booking allowed?
- [ ] 24-hour minimum?
- [ ] 12-hour minimum?

**Recommendation:** 24 hours minimum (gives you buffer)

### 2. Phone Call Direction
**Question:** Who calls whom?
- [ ] Coach calls user (user provides phone number in booking)
- [ ] User calls coach (coach's number shown in calendar invite)

**Recommendation:** Coach calls user (more professional, user comfort)

### 3. Cancellation Fee Collection
**Question:** How to collect 50% penalty for late cancellation?
- [ ] Charge original payment method automatically?
- [ ] Require prepayment for next booking?
- [ ] Manual invoice?

**Recommendation:** Charge original payment method (automatic, enforceable)

### 4. SMS Notifications
**Question:** Implement SMS reminders?
- [ ] Yes (requires Twilio integration)
- [ ] No (email + in-app sufficient for MVP)

**Recommendation:** Skip for MVP (adds complexity, cost)

### 5. Free Session Code Distribution
**Question:** How do users get promo code?
- [ ] Single code shared publicly ("FREESESSION25")
- [ ] Unique codes per user (prevents sharing)
- [ ] Generated after trial completion

**Recommendation:** Single shared code for MVP, track by user ID to prevent reuse

### 6. Backup Slot Handling
**Question:** If coach cancels, what happens?
- [ ] Automatically reschedule to user's backup slot?
- [ ] Email user to manually reschedule?
- [ ] Coach manually contacts user?

**Recommendation:** Email user with backup slot + option to reschedule

### 7. Package Session Scheduling
**Question:** User bought 3-session package. How do they book subsequent sessions?
- [ ] Book all 3 upfront?
- [ ] Book 1 at a time (track sessions remaining)?

**Recommendation:** Book 1 at a time, show "Sessions remaining: X/3" in UI

---

## Blast Radius - Updated Estimate

### New Files (8-12 files)
- `/api/booking.py` - Booking API endpoints
- `/api/google_calendar_service.py` - Google Calendar integration
- `/api/stripe_service.py` - Stripe payment integration
- `/api/notifications.py` - Email/SMS/in-app notifications
- `/mosaic_ui/booking-modal.js` - Booking modal logic
- `/mosaic_ui/booking-modal.css` - Modal styling
- `/data/migrations/add_booking_tables.sql` - Database schema
- `/data/migrations/seed_promo_codes.sql` - Promo code setup
- `/data/migrations/seed_coach_availability.sql` - Default availability

### Modified Files (4-6 files)
- `/mosaic_ui/index.html` - Add booking button + modal container
- `/api/index.py` - Register booking routes
- `/requirements.txt` - Add dependencies:
  - `google-api-python-client`
  - `google-auth`
  - `stripe`
  - `twilio` (optional, if SMS)
- `/api/storage.py` - May need booking-related queries
- `/.env` - Add environment variables (service account key, Stripe keys)

### Environment Variables Needed
```bash
# Google Calendar
GOOGLE_SERVICE_ACCOUNT_KEY='{...json...}'  # Service account credentials
COACH_GOOGLE_CALENDAR_ID='primary'  # Or specific calendar ID
COACH_PHONE_NUMBER='+1234567890'  # For calendar invites

# Stripe
STRIPE_PUBLISHABLE_KEY='pk_live_...'
STRIPE_SECRET_KEY='sk_live_...'

# Notifications (optional)
TWILIO_ACCOUNT_SID='...'
TWILIO_AUTH_TOKEN='...'
TWILIO_PHONE_NUMBER='+1...'
```

### Updated Blast Radius: 12-18 files

### Updated Implementation Time: 8-12 hours
- Google Calendar integration: 2-3 hours
- Stripe payment integration: 2-3 hours
- Database schema + migrations: 1 hour
- Frontend modal UI: 2-3 hours
- Backend API endpoints: 2-3 hours
- Testing + debugging: 2-3 hours

**Complexity Factors:**
- Payment integration adds significant complexity
- Multiple pricing tiers (free, single, package)
- Cancellation/rescheduling logic
- Notification preferences
- Promo code validation

---

## Recommended Phased Implementation

### Phase 1: Core Booking (MVP - 4 hours)
- Google Calendar service account setup
- Basic booking API (no payment)
- Simple modal UI
- Database schema
- Free sessions with promo code

**Deliverable:** Users can book free coaching sessions with code

### Phase 2: Payment Integration (3-4 hours)
- Stripe integration
- Paid single session booking
- 3-session package purchase
- Payment validation before booking

**Deliverable:** Users can purchase and book paid sessions

### Phase 3: Advanced Features (3-4 hours)
- Cancellation/rescheduling UI
- Backup slot handling
- Reschedule penalty enforcement
- Coach admin dashboard (view bookings, block dates)

**Deliverable:** Full lifecycle management

### Phase 4: Notifications & Polish (2-3 hours)
- Email notifications (via existing email service when ready)
- In-app notifications
- SMS (optional)
- UI polish and mobile responsiveness

**Deliverable:** Production-ready system

---

## Next Actions

### Immediate (Awaiting User Clarification)
1. Answer 7 clarifying questions above
2. Approve phased implementation approach
3. Confirm UI recommendation (modal overlay)

### Once Confirmed
1. Set up Google Cloud project + service account
2. Set up Stripe account + get API keys
3. Implement Phase 1 (core booking)
4. Test with real Google Calendar
5. Deploy Phase 1 to staging
6. User acceptance testing
7. Proceed with Phase 2-4

---

## Recommendation Summary

**SSE Decision:** Proceed with phased implementation, starting with Phase 1 (core booking, free sessions only).

**Rationale:**
- De-risks payment integration complexity
- Allows user testing of booking UX before money involved
- Can launch free sessions immediately (25 slots)
- Payment integration follows after core flow validated

**User Approval Needed:**
1. Confirm phased approach (Phase 1 → 2 → 3 → 4)
2. Answer 7 clarifying questions
3. Provide Stripe account details (or create account)
4. Provide Google account for service account setup

---

**END OF FINALIZED REQUIREMENTS - READY FOR PHASE 1 IMPLEMENTATION**
