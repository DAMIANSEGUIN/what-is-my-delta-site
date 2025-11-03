# Handoff to Browser (Developer Agent)
**From**: Claude Code CLI (Senior Systems Engineer)
**To**: Claude Code Browser (Senior Developer)
**Date**: 2025-10-22
**Priority**: Medium-High

---

## Task Summary

Implement two new features for Mosaic platform:

1. **Draggable/Resizable Windows** - Make UI panels moveable and resizable
2. **Google Calendar Appointment Booking** - Add booking link for coaching sessions

---

## What CLI Already Did

✅ **Packages installed** in `~/projects/mosaic-platform`:
- `react-draggable` (11 packages added)
- `re-resizable`

✅ **Specs created**:
- `~/Downloads/Planning/strategy_desktop/project_briefs/mosaic_draggable_windows_spec.md`
- `~/Downloads/Planning/strategy_desktop/project_briefs/mosaic_appointment_booking_spec.md`

✅ **Repository location**: `~/projects/mosaic-platform`
- Remote: `https://github.com/DAMIANSEGUIN/what-is-my-delta-site.git`
- Branch: `main`

---

## Your Tasks (Browser)

### Task 1: Implement Draggable/Resizable Windows

**Read full spec**: `mosaic_draggable_windows_spec.md`

**Quick version**:
1. Create `src/components/DraggableWindow.jsx` (code in spec)
2. Wrap PS101 coaching steps (or other key UI) in `<DraggableWindow>`
3. Add z-index management (clicked window comes to front)
4. Add mobile detection (disable dragging on <768px screens)
5. Test locally
6. Deploy to Netlify

**Packages already installed**:
- `react-draggable`
- `re-resizable`

**Example usage** (from spec):
```jsx
<DraggableWindow
  title="What Is My Delta?"
  defaultWidth={500}
  defaultHeight={400}
  defaultPosition={{ x: 50, y: 50 }}
>
  <textarea placeholder="Describe your situation..." />
</DraggableWindow>
```

---

### Task 2: Add Google Calendar Booking

**Read full spec**: `mosaic_appointment_booking_spec.md`

**Quick version**:
1. Add booking button/link to PS101 results page (or user dashboard)
2. Use this URL: `https://calendar.app.google/EAnDSz2CcTtH849x6`
3. Choose implementation:
   - **Simple link** (fastest): Opens in new tab
   - **Embedded iframe** (better UX): Stays on site
4. Test locally
5. Deploy to Netlify

**Recommended Phase 1**: Simple link (2 minutes)
**Phase 2**: Embedded iframe (if desired)

**Example code** (from spec):
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

---

## Repository Info

**Location**: `~/projects/mosaic-platform`

**Current deployment**:
- **Backend**: Railway (`what-is-my-delta-site-production.up.railway.app`)
- **Frontend**: Netlify (`www.whatismydelta.com`)
- **Auto-deploy**: Push to `main` branch triggers deploy

**Environment**:
- Node.js project (React frontend, FastAPI backend)
- Frontend in `src/` or similar
- Already has PS101 coaching flow implemented

---

## Deployment Checklist (After Implementation)

- [ ] Test locally (`npm run dev` or similar)
- [ ] Draggable windows work (drag, resize, stay in bounds)
- [ ] Booking link/iframe works
- [ ] Mobile responsive (dragging disabled on small screens)
- [ ] Git commit with descriptive message
- [ ] Push to `main` branch (triggers auto-deploy)
- [ ] Verify on production (`www.whatismydelta.com`)
- [ ] Test live site (all features work)

---

## Files You'll Likely Modify

**For draggable windows**:
- `src/components/DraggableWindow.jsx` (NEW - create this)
- `src/components/PS101Results.jsx` or similar (wrap in DraggableWindow)
- `src/pages/Dashboard.jsx` or similar (if exists)

**For booking**:
- `src/components/PS101Results.jsx` or similar (add button)
- `src/pages/Dashboard.jsx` or similar (if exists)
- `src/components/BookingButton.jsx` (NEW - optional)

---

## Questions/Blockers?

If you encounter issues:
1. Check the full specs in `~/Downloads/Planning/strategy_desktop/project_briefs/`
2. Check infrastructure docs: `~/Downloads/Planning/systems_cli/INFRASTRUCTURE_CONFIG.md`
3. Ask CLI (me) for help with:
   - Git operations
   - Deployment issues
   - Environment variables
   - System-level problems

---

## Success Criteria

### Draggable Windows:
- [ ] Windows can be dragged by header
- [ ] Windows can be resized
- [ ] Windows stay in viewport bounds
- [ ] Works on desktop (Chrome, Firefox, Safari)
- [ ] Disabled/adapted for mobile

### Booking:
- [ ] User can access booking link from Mosaic
- [ ] Link opens Google Calendar appointment page
- [ ] User can successfully book appointment

---

## Estimated Effort

- **Draggable windows**: 2-4 hours
- **Booking link**: 15-30 minutes
- **Total**: 2.5-4.5 hours

---

**Good luck! Let CLI know when you're done so we can verify deployment.**

---

**END OF HANDOFF**
