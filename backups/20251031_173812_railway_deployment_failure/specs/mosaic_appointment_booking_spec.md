# Mosaic Feature Spec: Appointment Booking Integration
**Date**: 2025-10-22
**Status**: Ready for Browser Implementation
**Priority**: Medium

---

## Feature Request

Add Google Calendar appointment booking to Mosaic for Coach in Residence and premium coaching sessions.

---

## Booking URL

**Google Calendar Appointment Link**:
```
https://calendar.app.google/EAnDSz2CcTtH849x6
```

---

## Implementation Options

### Option 1: Simple Link (Fastest)
Add a "Book a Session" button/link that opens the booking page in a new tab.

**Where to add**:
- PS101 results page (after user completes coaching flow)
- User dashboard (if exists)
- Marketing landing page

**Code** (example):
```jsx
<a
  href="https://calendar.app.google/EAnDSz2CcTtH849x6"
  target="_blank"
  rel="noopener noreferrer"
  className="book-session-button"
>
  Book a Coaching Session
</a>
```

**Pros**:
- 2 minutes to implement
- Zero maintenance
- Never breaks

**Cons**:
- Leaves Mosaic site (external page)

---

### Option 2: Embedded iframe (Better UX)
Embed the Google Calendar booking page directly in Mosaic.

**Code** (example):
```jsx
<iframe
  src="https://calendar.app.google/EAnDSz2CcTtH849x6"
  width="100%"
  height="600px"
  frameBorder="0"
  title="Book a Coaching Session"
/>
```

**Where to add**:
- Dedicated `/book` route
- Modal popup after PS101 completion
- User dashboard section

**Pros**:
- User stays on Mosaic site
- Cleaner experience

**Cons**:
- May have iframe restrictions (test first)
- Slightly more complex

---

## Recommended Implementation

**Phase 1** (Now): Simple link on PS101 results page
- Fast to implement
- Validates demand
- Zero risk

**Phase 2** (Later): Embedded iframe if users prefer staying on site
- Better UX
- Requires testing for iframe compatibility

---

## Copy/Messaging

**Button text options**:
- "Book a 1-on-1 Session"
- "Schedule a Coaching Call"
- "Talk to a Coach"
- "Get Personal Guidance"

**Context text** (before button):
> "Want personalized guidance? Book a 30-minute coaching session to dive deeper into your career challenges."

---

## Acceptance Criteria

- [ ] User can access booking link from Mosaic site
- [ ] Link opens to Google Calendar appointment page
- [ ] User can successfully book appointment
- [ ] Booking confirmation sent to user email (automatic via Google Calendar)
- [ ] You (coach) receive booking notification

---

## For Browser (Developer Agent)

**Task**: Add appointment booking to Mosaic frontend

**Files to modify** (likely):
- `src/components/PS101Results.jsx` (or similar)
- `src/pages/Dashboard.jsx` (if exists)
- `src/components/BookingButton.jsx` (new component, optional)

**Steps**:
1. Choose implementation (link vs iframe)
2. Add to appropriate page/component
3. Test locally (does link work? does iframe load?)
4. Deploy to Netlify
5. Verify on production

**Booking URL to use**:
```
https://calendar.app.google/EAnDSz2CcTtH849x6
```

---

## Notes

- No API integration needed (Google Calendar handles everything)
- No authentication required (public booking link)
- No database changes needed
- Zero maintenance (Google manages availability, reminders, confirmations)

---

**Ready for Browser to implement.**
