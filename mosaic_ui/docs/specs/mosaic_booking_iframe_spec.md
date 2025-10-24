# Mosaic Google Calendar Booking (Iframe) Specification

**Feature**: Embed Google Calendar appointment booking directly in the site
**Status**: Enhancement to existing booking link
**Complexity**: Low
**Implementation**: Frontend only (HTML + JavaScript)

---

## Overview

Replace the external link to Google Calendar with an embedded iframe that allows users to book coaching sessions without leaving the Mosaic platform.

**Current**: Link opens `https://calendar.app.google/EAnDSz2CcTtH849x6` in new tab
**Enhanced**: Iframe embeds booking directly on site with modal or sidebar display

---

## Requirements

### Functional Requirements
1. **Embedded booking interface** - Users book sessions without leaving site
2. **Modal display** - Booking appears in a modal overlay
3. **Responsive design** - Works on desktop and mobile
4. **Fallback behavior** - If iframe blocked/fails, show link instead
5. **Close functionality** - Easy way to dismiss booking interface
6. **Deep integration** - Triggered from multiple UI locations (coach chat, results page, dashboard)

### Non-Functional Requirements
- Fast loading (<2s)
- No CORS issues
- Mobile-friendly (responsive iframe)
- Accessible (keyboard navigation, screen readers)

---

## Implementation Options

### Option 1: Modal Iframe (Recommended)

**Pros**:
- Overlay keeps user in context
- Easy to dismiss
- Professional appearance
- Works on mobile

**Cons**:
- Google Calendar may not allow iframe embedding (CORS/X-Frame-Options)
- Requires fallback logic

### Option 2: Inline Iframe

**Pros**:
- Always visible (no modal management)
- Simpler implementation

**Cons**:
- Takes up permanent screen space
- Less flexible placement

### Option 3: Sidebar Iframe (Draggable Window)

**Pros**:
- Combines with draggable windows feature
- User can position as needed
- Multi-task friendly

**Cons**:
- More complex
- May obscure content

**Recommendation**: Use **Option 1 (Modal)** with fallback to external link if iframe blocked.

---

## HTML Implementation

### Modal Iframe

```html
<!-- BOOKING MODAL (add to index.html) -->
<div id="bookingModal" class="modal" style="display:none">
  <div class="booking-panel" style="
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 6px;
    box-shadow: 0 8px 30px rgba(0,0,0,.12);
    max-width: 95vw;
    max-height: 95vh;
    width: 800px;
    height: 700px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  ">
    <!-- Header -->
    <div class="booking-header" style="
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 16px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
    ">
      <span style="font-size: 11px; text-transform: uppercase; letter-spacing: .08em; font-weight: 600;">
        book a coaching session
      </span>
      <button id="closeBooking" class="quiet" style="padding: 4px 8px; font-size: 10px;" title="Close">✕</button>
    </div>

    <!-- Iframe Container -->
    <div class="booking-content" style="flex: 1; position: relative; overflow: hidden;">
      <iframe
        id="bookingIframe"
        src="https://calendar.app.google/EAnDSz2CcTtH849x6"
        style="
          width: 100%;
          height: 100%;
          border: none;
          display: block;
        "
        title="Book Coaching Session"
        allow="payment"
        loading="lazy"
      ></iframe>

      <!-- Loading state -->
      <div id="bookingLoading" style="
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
        z-index: 1;
      ">
        <div style="text-align: center;">
          <div style="
            width: 40px;
            height: 40px;
            border: 3px solid var(--line);
            border-top-color: var(--hair);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 12px;
          "></div>
          <p style="font-size: 11px; color: var(--muted);">loading booking calendar...</p>
        </div>
      </div>

      <!-- Error/Fallback state -->
      <div id="bookingError" style="
        position: absolute;
        inset: 0;
        display: none;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
        padding: 40px;
        text-align: center;
        z-index: 1;
      ">
        <p style="font-size: 13px; margin-bottom: 16px; color: var(--fg);">
          unable to load booking calendar
        </p>
        <p style="font-size: 11px; color: var(--muted); margin-bottom: 24px;">
          please use the direct link to schedule your session
        </p>
        <a
          href="https://calendar.app.google/EAnDSz2CcTtH849x6"
          target="_blank"
          rel="noopener noreferrer"
          class="quiet"
          style="
            padding: 10px 20px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: .08em;
            background: var(--hair);
            color: #fff;
            border: 1px solid var(--hair);
            text-decoration: none;
            display: inline-block;
          "
        >
          open booking page
        </a>
      </div>
    </div>
  </div>
</div>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Mobile responsive */
@media (max-width: 860px) {
  .booking-panel {
    width: 100% !important;
    height: 100% !important;
    max-width: 100vw !important;
    max-height: 100vh !important;
    border-radius: 0 !important;
  }
}
</style>
```

---

## JavaScript Implementation

### Basic Functionality

```javascript
(function() {
  'use strict';

  const bookingModal = document.getElementById('bookingModal');
  const bookingIframe = document.getElementById('bookingIframe');
  const bookingLoading = document.getElementById('bookingLoading');
  const bookingError = document.getElementById('bookingError');
  const closeBookingBtn = document.getElementById('closeBooking');

  let iframeLoaded = false;
  let loadTimeout;

  // Open booking modal
  function openBookingModal() {
    bookingModal.style.display = 'flex';
    bookingLoading.style.display = 'flex';
    bookingError.style.display = 'none';

    // Set timeout for loading (10 seconds)
    loadTimeout = setTimeout(() => {
      if (!iframeLoaded) {
        showBookingError();
      }
    }, 10000);
  }

  // Close booking modal
  function closeBookingModal() {
    bookingModal.style.display = 'none';
    clearTimeout(loadTimeout);
  }

  // Iframe loaded successfully
  function onIframeLoad() {
    iframeLoaded = true;
    clearTimeout(loadTimeout);

    // Hide loading state
    setTimeout(() => {
      bookingLoading.style.display = 'none';
    }, 500);
  }

  // Iframe failed to load or blocked
  function showBookingError() {
    console.warn('Booking iframe failed to load or was blocked');
    bookingLoading.style.display = 'none';
    bookingError.style.display = 'flex';
  }

  // Event listeners
  if (bookingIframe) {
    bookingIframe.addEventListener('load', onIframeLoad);

    // Detect iframe blocking (X-Frame-Options)
    bookingIframe.addEventListener('error', showBookingError);
  }

  if (closeBookingBtn) {
    closeBookingBtn.addEventListener('click', closeBookingModal);
  }

  // Close on backdrop click
  if (bookingModal) {
    bookingModal.addEventListener('click', (e) => {
      if (e.target === bookingModal) {
        closeBookingModal();
      }
    });
  }

  // Escape key to close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && bookingModal.style.display === 'flex') {
      closeBookingModal();
    }
  });

  // Expose global function to open booking
  window.openBooking = openBookingModal;

  // INTEGRATION POINTS:
  // Add booking buttons throughout the UI

  // 1. Add to coach chat
  const chatContent = document.querySelector('.chat main');
  if (chatContent) {
    const bookingBtn = document.createElement('button');
    bookingBtn.className = 'quiet';
    bookingBtn.textContent = 'book a session';
    bookingBtn.style.cssText = 'width:100%;margin-top:12px;padding:8px;font-size:10px;text-transform:uppercase;letter-spacing:.08em';
    bookingBtn.addEventListener('click', openBookingModal);

    // Add to chat footer or content area
    const chatFooter = document.querySelector('.chat footer');
    if (chatFooter) {
      chatFooter.insertAdjacentElement('beforebegin', bookingBtn);
    }
  }

  // 2. Add to PS101 completion
  function showBookingAfterPS101() {
    const completionMsg = document.createElement('div');
    completionMsg.innerHTML = `
      <p style="margin:16px 0 12px;font-size:11px;color:var(--muted);">
        ready for personalized guidance?
      </p>
      <button class="quiet" onclick="openBooking()" style="width:100%;padding:10px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;background:var(--hair);color:#fff;border:1px solid var(--hair)">
        schedule 1-on-1 coaching
      </button>
    `;

    // Add to appropriate location (e.g., after PS101 step 10)
    const ps101Container = document.getElementById('ps101-container');
    if (ps101Container) {
      ps101Container.appendChild(completionMsg);
    }
  }

  // 3. Add to user dashboard
  const welcomeSection = document.getElementById('welcome');
  if (welcomeSection) {
    const bookingCTA = document.createElement('div');
    bookingCTA.style.cssText = 'margin-top:24px;text-align:center';
    bookingCTA.innerHTML = `
      <p style="font-size:11px;color:var(--muted);margin-bottom:12px">
        need help navigating your transition?
      </p>
      <button class="quiet" onclick="openBooking()" style="padding:10px 24px;font-size:11px;text-transform:uppercase;letter-spacing:.08em">
        book a coaching session
      </button>
    `;

    welcomeSection.appendChild(bookingCTA);
  }

  // 4. Add to navigation (optional)
  const nav = document.querySelector('.nav');
  if (nav) {
    const bookingLink = document.createElement('a');
    bookingLink.href = '#';
    bookingLink.textContent = 'book session';
    bookingLink.title = 'Schedule a 1-on-1 coaching session';
    bookingLink.addEventListener('click', (e) => {
      e.preventDefault();
      openBookingModal();
    });

    nav.appendChild(bookingLink);
  }

})();
```

---

## Alternative: Draggable Booking Window

If you want the booking to be a draggable window (consistent with window enhancements spec):

```javascript
// Create booking as draggable window
const bookingWindow = new DraggableWindow({
  id: 'booking_window',
  title: 'Book Coaching Session',
  content: `
    <iframe
      src="https://calendar.app.google/EAnDSz2CcTtH849x6"
      style="width:100%;height:100%;border:none"
      title="Book Coaching Session"
      allow="payment"
    ></iframe>
  `,
  defaultX: 200,
  defaultY: 100,
  defaultWidth: 700,
  defaultHeight: 600
});

// Open booking window
function openBooking() {
  bookingWindow.show();
}
```

---

## Google Calendar Iframe Considerations

### X-Frame-Options Header

Google Calendar **may** block iframe embedding with `X-Frame-Options: DENY` or `SAMEORIGIN`.

**Detection**:
```javascript
// Check if iframe is blocked
bookingIframe.addEventListener('error', () => {
  console.error('Iframe blocked by X-Frame-Options');
  showBookingError(); // Show fallback link
});
```

**Workaround**:
- If blocked, automatically show fallback external link
- Test with actual Google Calendar URL to confirm behavior

### CORS Issues

Google Calendar iframes typically work without CORS issues since you're embedding, not making fetch requests.

### Performance

- Use `loading="lazy"` attribute to defer iframe load until visible
- Show loading spinner while iframe initializes
- Set reasonable timeout (10s) before showing fallback

---

## Testing Checklist

### Functionality
- [ ] Modal opens when clicking booking button
- [ ] Iframe loads Google Calendar interface
- [ ] User can complete booking within iframe
- [ ] Modal closes on close button click
- [ ] Modal closes on backdrop click
- [ ] Modal closes on Escape key
- [ ] Fallback link shown if iframe blocked

### Responsive Design
- [ ] Modal scales on mobile (<768px)
- [ ] Iframe is scrollable on small screens
- [ ] Buttons remain accessible
- [ ] No horizontal overflow

### Integration Points
- [ ] Booking button in coach chat works
- [ ] Booking CTA on dashboard works
- [ ] Booking link in navigation works
- [ ] PS101 completion shows booking option

### Accessibility
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Screen readers announce modal correctly
- [ ] Focus trapped within modal when open
- [ ] Fallback link accessible

### Performance
- [ ] Loading spinner appears immediately
- [ ] Iframe loads within 10 seconds
- [ ] No layout shift when iframe loads
- [ ] Modal animations smooth (60fps)

---

## Placement Recommendations

### High-Priority Locations (Implement First)
1. **Coach chat footer** - User already engaged with coaching
2. **PS101 completion** - Natural next step after assessment
3. **User dashboard** - Prominent CTA for new users

### Medium-Priority Locations
4. **Navigation bar** - Always accessible
5. **Job search results** - Offer help when stuck
6. **Resume feedback page** - Transition point

### Low-Priority Locations
7. **Settings page** - Administrative area
8. **Help/Guide modal** - Support context

---

## Fallback Behavior

If iframe embedding fails (X-Frame-Options blocked):

```javascript
// Fallback UI (already shown in HTML above)
<div id="bookingError">
  <p>Unable to load booking calendar</p>
  <p>Please use the direct link to schedule your session</p>
  <a href="https://calendar.app.google/EAnDSz2CcTtH849x6" target="_blank">
    Open Booking Page
  </a>
</div>
```

This ensures users can always book sessions even if iframe is blocked.

---

## Future Enhancements

- [ ] Calendar API integration (show available slots inline)
- [ ] Multi-coach selection (if expanding team)
- [ ] Session type selection (30min/60min/initial consult)
- [ ] Pre-fill user info from profile
- [ ] Confirmation email integration
- [ ] Booking history in user dashboard
- [ ] Calendar sync (add to user's calendar)
- [ ] Reminders/notifications

---

## Analytics Tracking

```javascript
// Track booking modal interactions
function trackBookingEvent(action) {
  // Google Analytics (if implemented)
  if (window.gtag) {
    gtag('event', action, {
      'event_category': 'booking',
      'event_label': 'coaching_session'
    });
  }

  // Or custom analytics
  fetch(`${API_BASE}/analytics/track`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event: 'booking',
      action: action,
      timestamp: Date.now()
    })
  });
}

// Usage
function openBookingModal() {
  trackBookingEvent('modal_opened');
  // ... rest of open logic
}

function closeBookingModal() {
  trackBookingEvent('modal_closed');
  // ... rest of close logic
}

bookingIframe.addEventListener('load', () => {
  trackBookingEvent('iframe_loaded');
  onIframeLoad();
});
```

---

## Deployment Steps

1. **Add HTML** - Insert booking modal HTML into `index.html`
2. **Add JavaScript** - Add booking logic to main JavaScript section
3. **Add CSS** - Include loading spinner animation
4. **Test iframe** - Verify Google Calendar allows embedding
5. **Add integration points** - Place booking buttons in coach chat, dashboard, etc.
6. **Test fallback** - Confirm external link works if iframe blocked
7. **Deploy to Netlify** - Push changes
8. **Verify production** - Test booking flow on live site

---

## Rollback Plan

If booking iframe causes issues:

1. **Immediate**: Hide booking modal with CSS (`#bookingModal { display: none !important; }`)
2. **Revert**: Remove booking buttons from UI
3. **Restore**: Keep original external link approach
4. **Debug**: Test iframe in different browsers/environments
5. **Fix**: Address blocking issues or CORS errors
6. **Redeploy**: Once fixed, re-enable booking modal

---

## Summary

**Complexity**: Low
**Files to modify**: 1 (`mosaic_ui/index.html`)
**Breaking changes**: None (additive feature)
**Fallback**: External link if iframe blocked
**User benefit**: Book coaching sessions without leaving site

**Implementation time**: ~2 hours
**Testing time**: ~1 hour
**Total effort**: Low

---

**END OF SPECIFICATION**
