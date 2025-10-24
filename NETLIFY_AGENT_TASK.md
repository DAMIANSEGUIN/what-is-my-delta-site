# Netlify Agent Task: Implement Draggable Windows & Booking

## Task Summary

Implement two features for the Mosaic platform:

1. **Draggable/Resizable Windows** - Make UI panels moveable and resizable by users
2. **Google Calendar Appointment Booking** - Add booking link for coaching sessions

---

## File Locations

**Implementation specs**:
- `docs/specs/mosaic_draggable_windows_spec.md` - Complete spec for draggable windows
- `docs/specs/mosaic_appointment_booking_spec.md` - Complete spec for booking integration
- `docs/HANDOFF_TO_BROWSER_2025-10-22.md` - Full handoff document with context

**Dependencies already installed**:
- `react-draggable` ✅
- `re-resizable` ✅

See `package.json` for confirmation.

---

## Task 1: Draggable/Resizable Windows

**Goal**: Allow users to drag and resize windows/panels on the Mosaic site.

**Implementation**:

1. Create new component: `src/components/DraggableWindow.jsx`
   - Full code provided in `docs/specs/mosaic_draggable_windows_spec.md`
   - Import `react-draggable` and `re-resizable`

2. Wrap PS101 coaching steps in `<DraggableWindow>` component
   - Find existing PS101 step components
   - Wrap each step in the new DraggableWindow component
   - Set appropriate default positions and sizes

3. Add features:
   - Z-index management (clicked window comes to front)
   - Mobile detection (disable dragging on screens <768px)
   - Minimum window sizes (300px × 200px)
   - Bounded dragging (windows stay within viewport)

**Test**:
- Windows drag smoothly when clicking header
- Windows resize from corners
- Windows don't disappear off-screen
- Works on desktop browsers
- Gracefully disabled on mobile

---

## Task 2: Google Calendar Booking Integration

**Goal**: Add appointment booking link for users to schedule coaching sessions.

**Booking URL**: `https://calendar.app.google/EAnDSz2CcTtH849x6`

**Implementation** (choose one):

### Option A: Simple Link (Recommended for Phase 1)
Add a button/link that opens booking page in new tab.

**Where to add**:
- PS101 results page (after completing coaching flow)
- User dashboard (if exists)

**Code**:
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

### Option B: Embedded iframe (Better UX)
Embed booking directly in the site.

**Code**:
```jsx
<iframe
  src="https://calendar.app.google/EAnDSz2CcTtH849x6"
  width="100%"
  height="600px"
  frameBorder="0"
  title="Book a Coaching Session"
/>
```

**Test**:
- Link opens to Google Calendar appointment page
- User can successfully book appointment
- No console errors

---

## Success Criteria

### Draggable Windows:
- [ ] Windows can be dragged by clicking header
- [ ] Windows can be resized from corners
- [ ] Windows stay within viewport bounds
- [ ] Works in Chrome, Firefox, Safari
- [ ] Disabled or adapted for mobile devices

### Booking:
- [ ] Booking link accessible from Mosaic site
- [ ] Link opens to correct Google Calendar page
- [ ] User can complete booking flow

---

## Implementation Notes

- **Packages already installed** - no need to run npm install
- **Branch**: `feature/draggable-windows-and-booking`
- **Full specs available** in `docs/specs/` folder
- **Deploy when complete** - push to branch, will auto-deploy via Railway/Netlify

---

## Expected Deliverables

1. New file: `src/components/DraggableWindow.jsx`
2. Modified files: PS101 step components (wrapped in DraggableWindow)
3. Modified files: PS101 results page or dashboard (with booking button/link)
4. All tests passing
5. Ready to merge to main branch

---

**Read the full specs in `docs/specs/` for complete implementation details.**
