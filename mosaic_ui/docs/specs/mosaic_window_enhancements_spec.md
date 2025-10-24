# Mosaic Window Enhancements Specification

**Feature**: Draggable/resizable window improvements (persistent layouts, maximize, snap-to-grid)
**Status**: Enhancement to existing draggable windows feature
**Complexity**: Low-Medium
**Implementation**: Frontend only (vanilla JavaScript)

---

## Overview

Enhance the draggable/resizable windows system with:
1. **Persistent layouts** - Save window positions/sizes to localStorage
2. **Window maximize/fullscreen** - Expand windows to fill viewport
3. **Snap-to-grid positioning** - Round positions to grid increments for cleaner alignment

---

## 1. Persistent Layouts (localStorage)

### Requirement
Save window positions, sizes, and states so they restore on page reload.

### Implementation

```javascript
// Window state manager
const WindowStateManager = {
  STORAGE_KEY: 'mosaic_window_states',

  // Save window state
  save(windowId, state) {
    const allStates = this.loadAll();
    allStates[windowId] = {
      ...state,
      timestamp: Date.now()
    };

    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(allStates));
    } catch (e) {
      console.warn('Failed to save window state:', e);
    }
  },

  // Load all window states
  loadAll() {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      return stored ? JSON.parse(stored) : {};
    } catch (e) {
      console.warn('Failed to load window states:', e);
      return {};
    }
  },

  // Load specific window state
  load(windowId) {
    const allStates = this.loadAll();
    return allStates[windowId] || null;
  },

  // Clear all saved states
  clearAll() {
    localStorage.removeItem(this.STORAGE_KEY);
  },

  // Clear old states (older than 30 days)
  cleanup() {
    const allStates = this.loadAll();
    const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);

    Object.keys(allStates).forEach(windowId => {
      if (allStates[windowId].timestamp < thirtyDaysAgo) {
        delete allStates[windowId];
      }
    });

    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(allStates));
    } catch (e) {
      console.warn('Failed to cleanup window states:', e);
    }
  }
};

// Enhanced DraggableWindow component with persistence
class DraggableWindow {
  constructor(config) {
    this.id = config.id || `window_${Date.now()}`;
    this.title = config.title || 'Window';
    this.content = config.content || '';

    // Try to restore saved state
    const savedState = WindowStateManager.load(this.id);

    this.state = {
      x: savedState?.x || config.defaultX || 100,
      y: savedState?.y || config.defaultY || 100,
      width: savedState?.width || config.defaultWidth || 400,
      height: savedState?.height || config.defaultHeight || 300,
      isMaximized: savedState?.isMaximized || false,
      zIndex: config.zIndex || 1000
    };

    this.element = this.create();
    this.attachEventListeners();
  }

  create() {
    const win = document.createElement('div');
    win.className = 'draggable-window';
    win.id = this.id;
    win.style.cssText = `
      position: fixed;
      left: ${this.state.x}px;
      top: ${this.state.y}px;
      width: ${this.state.width}px;
      height: ${this.state.height}px;
      z-index: ${this.state.zIndex};
      background: #fff;
      border: 1px solid var(--line);
      box-shadow: 0 8px 30px rgba(0,0,0,.06);
      display: flex;
      flex-direction: column;
    `;

    win.innerHTML = `
      <div class="window-header" style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 10px;
        border-bottom: 1px solid var(--line);
        cursor: move;
        user-select: none;
      ">
        <span style="font-size: 11px; text-transform: uppercase; letter-spacing: .08em;">${this.title}</span>
        <div class="window-controls" style="display: flex; gap: 6px;">
          <button class="window-maximize quiet" style="padding: 2px 6px; font-size: 10px;" title="Maximize">▭</button>
          <button class="window-close quiet" style="padding: 2px 6px; font-size: 10px;" title="Close">✕</button>
        </div>
      </div>
      <div class="window-content" style="
        flex: 1;
        padding: 12px;
        overflow: auto;
      ">${this.content}</div>
      <div class="resize-handle" style="
        position: absolute;
        bottom: 0;
        right: 0;
        width: 16px;
        height: 16px;
        cursor: se-resize;
        background: linear-gradient(135deg, transparent 50%, var(--line) 50%);
      "></div>
    `;

    return win;
  }

  attachEventListeners() {
    // Dragging
    const header = this.element.querySelector('.window-header');
    let isDragging = false;
    let dragStartX, dragStartY, windowStartX, windowStartY;

    header.addEventListener('mousedown', (e) => {
      if (e.target.closest('.window-controls')) return; // Don't drag when clicking controls

      isDragging = true;
      dragStartX = e.clientX;
      dragStartY = e.clientY;
      windowStartX = this.state.x;
      windowStartY = this.state.y;

      this.bringToFront();
      e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging || this.state.isMaximized) return;

      const deltaX = e.clientX - dragStartX;
      const deltaY = e.clientY - dragStartY;

      this.state.x = windowStartX + deltaX;
      this.state.y = windowStartY + deltaY;

      // Keep within viewport bounds
      this.state.x = Math.max(0, Math.min(this.state.x, window.innerWidth - this.state.width));
      this.state.y = Math.max(0, Math.min(this.state.y, window.innerHeight - 40)); // Keep header visible

      this.updatePosition();
    });

    document.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        this.saveState();
      }
    });

    // Resizing
    const resizeHandle = this.element.querySelector('.resize-handle');
    let isResizing = false;
    let resizeStartX, resizeStartY, windowStartWidth, windowStartHeight;

    resizeHandle.addEventListener('mousedown', (e) => {
      isResizing = true;
      resizeStartX = e.clientX;
      resizeStartY = e.clientY;
      windowStartWidth = this.state.width;
      windowStartHeight = this.state.height;

      e.stopPropagation();
      e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
      if (!isResizing || this.state.isMaximized) return;

      const deltaX = e.clientX - resizeStartX;
      const deltaY = e.clientY - resizeStartY;

      this.state.width = Math.max(300, windowStartWidth + deltaX);
      this.state.height = Math.max(200, windowStartHeight + deltaY);

      this.updateSize();
    });

    document.addEventListener('mouseup', () => {
      if (isResizing) {
        isResizing = false;
        this.saveState();
      }
    });

    // Maximize button
    const maximizeBtn = this.element.querySelector('.window-maximize');
    maximizeBtn.addEventListener('click', () => {
      this.toggleMaximize();
    });

    // Close button
    const closeBtn = this.element.querySelector('.window-close');
    closeBtn.addEventListener('click', () => {
      this.close();
    });

    // Bring to front on click
    this.element.addEventListener('mousedown', () => {
      this.bringToFront();
    });
  }

  updatePosition() {
    this.element.style.left = `${this.state.x}px`;
    this.element.style.top = `${this.state.y}px`;
  }

  updateSize() {
    this.element.style.width = `${this.state.width}px`;
    this.element.style.height = `${this.state.height}px`;
  }

  bringToFront() {
    // Get highest z-index
    const allWindows = document.querySelectorAll('.draggable-window');
    let maxZ = 1000;
    allWindows.forEach(win => {
      const z = parseInt(window.getComputedStyle(win).zIndex) || 0;
      if (z > maxZ) maxZ = z;
    });

    this.state.zIndex = maxZ + 1;
    this.element.style.zIndex = this.state.zIndex;
  }

  toggleMaximize() {
    if (this.state.isMaximized) {
      // Restore
      this.state.isMaximized = false;
      this.element.style.left = `${this.state.x}px`;
      this.element.style.top = `${this.state.y}px`;
      this.element.style.width = `${this.state.width}px`;
      this.element.style.height = `${this.state.height}px`;
      this.element.querySelector('.window-maximize').textContent = '▭';
    } else {
      // Maximize
      this.state.isMaximized = true;
      this.element.style.left = '0';
      this.element.style.top = '0';
      this.element.style.width = '100vw';
      this.element.style.height = '100vh';
      this.element.querySelector('.window-maximize').textContent = '❐';
    }

    this.saveState();
  }

  close() {
    this.element.remove();
    // Optionally clear saved state
    // WindowStateManager.save(this.id, null);
  }

  saveState() {
    WindowStateManager.save(this.id, {
      x: this.state.x,
      y: this.state.y,
      width: this.state.width,
      height: this.state.height,
      isMaximized: this.state.isMaximized
    });
  }

  show() {
    document.body.appendChild(this.element);
    this.bringToFront();
  }
}

// Cleanup old states on page load
WindowStateManager.cleanup();
```

### Usage Example

```javascript
// Create a window with persistence
const coachWindow = new DraggableWindow({
  id: 'coach_window', // Unique ID for persistence
  title: 'Career Coach',
  content: '<p>Coaching content here...</p>',
  defaultX: 100,
  defaultY: 100,
  defaultWidth: 400,
  defaultHeight: 500
});

coachWindow.show();

// Reset all window positions (admin/debug)
// WindowStateManager.clearAll();
```

---

## 2. Window Maximize/Fullscreen

### Requirement
Allow windows to expand to fill the entire viewport with a maximize button.

### Features
- **Maximize button** in window header (▭ icon)
- **Toggle behavior**: Click once to maximize, click again to restore
- **Preserved state**: Original position/size remembered when maximized
- **Icon change**: ▭ (maximize) ↔ ❐ (restore) when toggled
- **Disable dragging/resizing** when maximized

### Implementation
Already included in the `DraggableWindow` class above (see `toggleMaximize()` method).

### CSS Enhancements

```css
/* Smooth maximize transitions */
.draggable-window {
  transition: left 0.2s ease, top 0.2s ease, width 0.2s ease, height 0.2s ease;
}

/* Hide resize handle when maximized */
.draggable-window.maximized .resize-handle {
  display: none;
}

/* Maximize button hover effect */
.window-maximize:hover {
  background: linear-gradient(145deg, #f0f0f0 0%, #e8e8e8 100%);
}
```

---

## 3. Snap-to-Grid Positioning

### Requirement
Round window positions to a grid (e.g., 20px increments) for cleaner alignment.

### Configuration

```javascript
const GRID_SIZE = 20; // Snap to 20px grid

// Snap function
function snapToGrid(value, gridSize = GRID_SIZE) {
  return Math.round(value / gridSize) * gridSize;
}
```

### Enhanced DraggableWindow with Snap-to-Grid

```javascript
// Add snap-to-grid to the mousemove handler
document.addEventListener('mousemove', (e) => {
  if (!isDragging || this.state.isMaximized) return;

  const deltaX = e.clientX - dragStartX;
  const deltaY = e.clientY - dragStartY;

  // Calculate new position
  let newX = windowStartX + deltaX;
  let newY = windowStartY + deltaY;

  // Snap to grid
  newX = snapToGrid(newX);
  newY = snapToGrid(newY);

  // Keep within viewport bounds
  this.state.x = Math.max(0, Math.min(newX, window.innerWidth - this.state.width));
  this.state.y = Math.max(0, Math.min(newY, window.innerHeight - 40));

  this.updatePosition();
});

// Also snap resize dimensions
document.addEventListener('mousemove', (e) => {
  if (!isResizing || this.state.isMaximized) return;

  const deltaX = e.clientX - resizeStartX;
  const deltaY = e.clientY - resizeStartY;

  // Snap width/height to grid
  this.state.width = Math.max(300, snapToGrid(windowStartWidth + deltaX));
  this.state.height = Math.max(200, snapToGrid(windowStartHeight + deltaY));

  this.updateSize();
});
```

### Optional: Visual Grid Overlay

```javascript
// Show grid when dragging (optional visual aid)
function showGrid() {
  let gridOverlay = document.getElementById('grid-overlay');

  if (!gridOverlay) {
    gridOverlay = document.createElement('div');
    gridOverlay.id = 'grid-overlay';
    gridOverlay.style.cssText = `
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 999;
      background-image:
        repeating-linear-gradient(0deg, transparent, transparent ${GRID_SIZE - 1}px, rgba(0,0,0,0.03) ${GRID_SIZE - 1}px, rgba(0,0,0,0.03) ${GRID_SIZE}px),
        repeating-linear-gradient(90deg, transparent, transparent ${GRID_SIZE - 1}px, rgba(0,0,0,0.03) ${GRID_SIZE - 1}px, rgba(0,0,0,0.03) ${GRID_SIZE}px);
      opacity: 0;
      transition: opacity 0.2s;
    `;
    document.body.appendChild(gridOverlay);
  }

  gridOverlay.style.opacity = '1';
}

function hideGrid() {
  const gridOverlay = document.getElementById('grid-overlay');
  if (gridOverlay) {
    gridOverlay.style.opacity = '0';
  }
}

// Show grid when dragging starts
header.addEventListener('mousedown', (e) => {
  if (e.target.closest('.window-controls')) return;
  isDragging = true;
  showGrid(); // Show grid overlay
  // ... rest of drag logic
});

// Hide grid when dragging ends
document.addEventListener('mouseup', () => {
  if (isDragging) {
    isDragging = false;
    hideGrid(); // Hide grid overlay
    this.saveState();
  }
});
```

---

## 4. Mobile Responsiveness

### Requirement
Gracefully disable dragging/resizing on mobile devices (<768px width).

### Implementation

```javascript
// Detect mobile
function isMobileDevice() {
  return window.innerWidth < 768 ||
         /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// Modified DraggableWindow constructor
class DraggableWindow {
  constructor(config) {
    this.id = config.id || `window_${Date.now()}`;
    this.isMobile = isMobileDevice();

    // ... rest of constructor

    this.element = this.create();

    if (!this.isMobile) {
      this.attachEventListeners(); // Only attach drag/resize on desktop
    } else {
      this.makeMobileFriendly(); // Convert to static modal on mobile
    }
  }

  makeMobileFriendly() {
    // On mobile, make windows full-screen modals
    this.element.style.cssText = `
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: ${this.state.zIndex};
      background: #fff;
      display: flex;
      flex-direction: column;
    `;

    // Remove resize handle
    const resizeHandle = this.element.querySelector('.resize-handle');
    if (resizeHandle) resizeHandle.remove();

    // Maximize button does nothing on mobile
    const maximizeBtn = this.element.querySelector('.window-maximize');
    if (maximizeBtn) maximizeBtn.style.display = 'none';

    // Close button still works
    const closeBtn = this.element.querySelector('.window-close');
    closeBtn.addEventListener('click', () => {
      this.close();
    });
  }
}

// Re-check on window resize
window.addEventListener('resize', () => {
  const wasMobile = window.innerWidth < 768;
  // Reload page if switching between mobile/desktop (optional)
  if (wasMobile !== isMobileDevice()) {
    location.reload();
  }
});
```

---

## Testing Checklist

### Persistent Layouts
- [ ] Window position saved to localStorage on drag end
- [ ] Window size saved to localStorage on resize end
- [ ] Window state restored on page reload
- [ ] Maximized state persists across reloads
- [ ] Old states (>30 days) cleaned up on page load
- [ ] Works with multiple windows simultaneously
- [ ] localStorage quota exceeded handled gracefully

### Maximize/Fullscreen
- [ ] Maximize button expands window to viewport
- [ ] Restore button returns to original position/size
- [ ] Icon toggles between ▭ and ❐
- [ ] Dragging disabled when maximized
- [ ] Resizing disabled when maximized
- [ ] Maximized state saved and restored

### Snap-to-Grid
- [ ] Window positions snap to 20px grid
- [ ] Window sizes snap to 20px increments
- [ ] Snapping feels natural (not jarring)
- [ ] Grid overlay appears when dragging (optional)
- [ ] Grid overlay disappears when drag ends

### Mobile Responsiveness
- [ ] Draggable windows disabled on <768px
- [ ] Windows become full-screen modals on mobile
- [ ] Resize handles hidden on mobile
- [ ] Maximize button hidden on mobile
- [ ] Close button still functional on mobile

---

## Integration with Existing Mosaic UI

### Replace Chat Window Implementation

```javascript
// Old chat window (static)
const chatEl = document.getElementById('chat');

// New draggable chat window
const chatWindow = new DraggableWindow({
  id: 'chat_window',
  title: 'Career Coach',
  content: document.getElementById('chat').innerHTML,
  defaultX: window.innerWidth - 340,
  defaultY: 20,
  defaultWidth: 320,
  defaultHeight: 400
});

// Show chat when clicking "chat" link
document.getElementById('openChat')?.addEventListener('click', (e) => {
  e.preventDefault();
  chatWindow.show();
});
```

### PS101 Flow as Draggable Window

```javascript
// Convert PS101 steps to draggable windows
function showPS101Step(stepNumber) {
  const stepWindow = new DraggableWindow({
    id: `ps101_step_${stepNumber}`,
    title: `PS101 Step ${stepNumber}`,
    content: `<div id="ps101-content">${stepContent}</div>`,
    defaultX: 200,
    defaultY: 100,
    defaultWidth: 500,
    defaultHeight: 400
  });

  stepWindow.show();
}
```

---

## Performance Considerations

### Throttle localStorage Writes

```javascript
// Debounce save state to avoid excessive writes
let saveTimeout;

saveState() {
  clearTimeout(saveTimeout);
  saveTimeout = setTimeout(() => {
    WindowStateManager.save(this.id, {
      x: this.state.x,
      y: this.state.y,
      width: this.state.width,
      height: this.state.height,
      isMaximized: this.state.isMaximized
    });
  }, 300); // Save 300ms after last change
}
```

### Limit Saved Windows

```javascript
// Only save last 10 windows
save(windowId, state) {
  const allStates = this.loadAll();
  allStates[windowId] = { ...state, timestamp: Date.now() };

  // Keep only last 10 windows (by timestamp)
  const entries = Object.entries(allStates);
  if (entries.length > 10) {
    entries.sort((a, b) => b[1].timestamp - a[1].timestamp);
    const kept = Object.fromEntries(entries.slice(0, 10));
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(kept));
  } else {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(allStates));
  }
}
```

---

## Admin/Debug Tools

### Reset All Windows Button

```html
<button id="resetWindowStates" class="quiet" style="position:fixed;bottom:10px;left:10px;z-index:9999;font-size:9px;padding:4px 8px;">
  reset window layouts
</button>

<script>
document.getElementById('resetWindowStates')?.addEventListener('click', () => {
  if (confirm('Reset all window positions and sizes?')) {
    WindowStateManager.clearAll();
    location.reload();
  }
});
</script>
```

### Show Saved States (Console)

```javascript
// Debug: Show all saved window states
console.table(WindowStateManager.loadAll());
```

---

## Future Enhancements

- [ ] Window minimize (collapse to taskbar)
- [ ] Window tiling (snap to edges, quarters)
- [ ] Keyboard shortcuts (Alt+F4 to close, Win+Up to maximize)
- [ ] Window groups (save/restore workspace layouts)
- [ ] Multi-monitor support
- [ ] Window animations (slide in/out, fade)
- [ ] Custom themes per window

---

**END OF SPECIFICATION**
