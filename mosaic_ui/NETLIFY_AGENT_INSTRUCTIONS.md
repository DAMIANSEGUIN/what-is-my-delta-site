# Instructions for Netlify Agent

## Task Overview

Implement two features for the Mosaic platform:

1. **Draggable & Resizable Windows** - Allow users to move and resize UI panels
2. **Google Calendar Appointment Booking** - Add booking link for coaching sessions

## File Locations (In This Directory)

All files are located in the `mosaic_ui/` directory where you are currently working:

- **Main task file**: `NETLIFY_AGENT_TASK.md` (in this directory)
- **Detailed specifications**:
  - `docs/specs/mosaic_draggable_windows_spec.md`
  - `docs/specs/mosaic_appointment_booking_spec.md`
- **Context document**: `docs/HANDOFF_TO_BROWSER_2025-10-22.md`

## npm Packages Already Installed

The required packages have been installed in the parent repository:
- `react-draggable` ✅
- `re-resizable` ✅

You may need to install them locally if they're not accessible from `mosaic_ui/`.

## Implementation Summary

### Feature 1: Draggable Windows
**Goal**: Make UI windows moveable and resizable

**What to do**:
1. Read the full spec in `docs/specs/mosaic_draggable_windows_spec.md`
2. Create new component using the code provided in the spec
3. Wrap PS101 coaching steps (or other UI elements) in the draggable component
4. Add z-index management and mobile detection

**Key files to modify**:
- Create: Component for draggable windows (exact code in spec)
- Modify: `index.html` or relevant JavaScript to use the new component

### Feature 2: Appointment Booking
**Goal**: Add Google Calendar booking link

**What to do**:
1. Read the full spec in `docs/specs/mosaic_appointment_booking_spec.md`
2. Add a button/link that opens: `https://calendar.app.google/EAnDSz2CcTtH849x6`
3. Place it on the PS101 results page or user dashboard

**Implementation options**:
- **Simple link** (fastest): Opens booking page in new tab
- **Embedded iframe** (better UX): Embeds booking directly on site

**Key files to modify**:
- Modify: `index.html` to add booking button/link

## Repository Information

- **Repository**: `https://github.com/DAMIANSEGUIN/what-is-my-delta-site`
- **Branch**: `main`
- **Netlify Base Directory**: `mosaic_ui` (this directory)
- **Deployment**: Auto-deploys to `https://www.whatismydelta.com`

## Success Criteria

### Draggable Windows:
- [ ] Windows can be dragged by header
- [ ] Windows can be resized from corners
- [ ] Windows stay within viewport bounds
- [ ] Works on desktop browsers
- [ ] Gracefully disabled on mobile (<768px)

### Booking:
- [ ] Booking link accessible from Mosaic
- [ ] Opens to correct Google Calendar page
- [ ] User can complete booking flow

## Next Steps

1. Read `NETLIFY_AGENT_TASK.md` in this directory
2. Read the detailed specs in `docs/specs/`
3. Implement both features
4. Test locally if possible
5. Commit and push to trigger deployment

---

**All required files are in the `mosaic_ui/` directory. You should be able to access them now.**
