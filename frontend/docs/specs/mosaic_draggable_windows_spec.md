# Mosaic Feature Spec: Draggable & Resizable Windows
**Date**: 2025-10-22
**Status**: Ready for Browser Implementation
**Priority**: Medium-High (UX enhancement)

---

## Feature Request

Make Mosaic site windows/panels **moveable (draggable)** and **resizable** by the user.

---

## User Story

**As a user**, I want to:
- Drag windows/panels around the screen to organize my workspace
- Resize windows to see more/less content
- Customize my layout based on my workflow

**So that**: I have control over my interface and can work efficiently.

---

## Technical Approach

### Recommended Library: **react-draggable** + **re-resizable**

Both are lightweight, well-maintained React libraries:

1. **react-draggable**: Makes components draggable
   - npm: `react-draggable`
   - Size: ~12KB
   - Docs: https://github.com/react-grid-layout/react-draggable

2. **re-resizable**: Makes components resizable
   - npm: `re-resizable`
   - Size: ~20KB
   - Docs: https://github.com/bokuweb/re-resizable

---

## Implementation Plan

### Step 1: Install Dependencies

```bash
npm install react-draggable re-resizable
```

### Step 2: Create Wrapper Component

**File**: `src/components/DraggableWindow.jsx`

```jsx
import React from 'react';
import Draggable from 'react-draggable';
import { Resizable } from 're-resizable';

const DraggableWindow = ({
  children,
  title,
  defaultWidth = 400,
  defaultHeight = 300,
  defaultPosition = { x: 0, y: 0 }
}) => {
  return (
    <Draggable
      handle=".window-header"
      defaultPosition={defaultPosition}
      bounds="parent"
    >
      <Resizable
        defaultSize={{
          width: defaultWidth,
          height: defaultHeight,
        }}
        minWidth={300}
        minHeight={200}
        style={{
          border: '1px solid #ccc',
          borderRadius: '8px',
          backgroundColor: 'white',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          position: 'absolute',
        }}
      >
        <div className="window-header" style={{
          padding: '12px',
          background: '#f5f5f5',
          borderBottom: '1px solid #ddd',
          cursor: 'move',
          borderTopLeftRadius: '8px',
          borderTopRightRadius: '8px',
        }}>
          <h3>{title}</h3>
        </div>
        <div className="window-content" style={{
          padding: '16px',
          overflowY: 'auto',
          height: 'calc(100% - 48px)',
        }}>
          {children}
        </div>
      </Resizable>
    </Draggable>
  );
};

export default DraggableWindow;
```

### Step 3: Wrap Existing Components

**Example**: Wrap PS101 coaching flow steps in draggable windows

**Before**:
```jsx
<div className="ps101-step">
  <h2>What Is My Delta?</h2>
  <textarea placeholder="Describe your situation..." />
</div>
```

**After**:
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

## Which Components to Make Draggable?

### Priority 1 (Core UX):
- **PS101 Coaching Steps**: Each step in its own window
- **Job Matches Panel** (OpportunityBridge results)
- **Resume Preview Panel**
- **User Dashboard Widgets**

### Priority 2 (Nice-to-Have):
- **Settings Panel**
- **Help/Documentation Panel**
- **Notifications Panel**

---

## User Preferences (Optional Phase 2)

Save window positions/sizes to user preferences:

```jsx
// Save to localStorage or database
const saveLayout = () => {
  const layout = {
    ps101Step1: { x: 50, y: 50, width: 500, height: 400 },
    jobMatches: { x: 600, y: 50, width: 400, height: 600 },
  };
  localStorage.setItem('mosaicLayout', JSON.stringify(layout));
};

// Load on mount
const loadLayout = () => {
  const saved = localStorage.getItem('mosaicLayout');
  return saved ? JSON.parse(saved) : defaultLayout;
};
```

---

## Design Considerations

### Minimize/Maximize/Close Buttons?
Add window controls to header:

```jsx
<div className="window-header">
  <h3>{title}</h3>
  <div className="window-controls">
    <button onClick={onMinimize}>_</button>
    <button onClick={onMaximize}>□</button>
    <button onClick={onClose}>✕</button>
  </div>
</div>
```

### Mobile Responsiveness?
- Disable dragging on mobile (too finicky on touch)
- Use standard stacked layout on small screens
- Only enable draggable windows on desktop (>768px width)

```jsx
const isMobile = window.innerWidth < 768;

{isMobile ? (
  <div>{children}</div>
) : (
  <DraggableWindow>{children}</DraggableWindow>
)}
```

---

## Testing Checklist

- [ ] Windows can be dragged by header (not by content area)
- [ ] Windows can be resized from all corners/edges
- [ ] Windows stay within viewport bounds (don't disappear off-screen)
- [ ] Min/max size constraints work
- [ ] Multiple windows don't overlap confusingly (z-index management)
- [ ] Performance acceptable with 3-5 open windows
- [ ] Works in Chrome, Firefox, Safari
- [ ] Disabled on mobile (or acceptable touch experience)

---

## Potential Issues & Solutions

### Issue 1: Windows overlap/stack messily
**Solution**: Implement z-index management (clicked window comes to front)

```jsx
const [zIndex, setZIndex] = useState(1);

const bringToFront = () => {
  setZIndex(prevMax => prevMax + 1);
};

<div style={{ zIndex }} onClick={bringToFront}>
  {/* window content */}
</div>
```

### Issue 2: Performance with many windows
**Solution**: Limit max open windows (3-5), or virtualize off-screen windows

### Issue 3: User loses window off-screen
**Solution**: Add "Reset Layout" button to restore default positions

---

## Acceptance Criteria

- [ ] User can drag windows by clicking header
- [ ] User can resize windows from corners
- [ ] Windows have minimum size (don't collapse to nothing)
- [ ] Windows stay within viewport (bounded)
- [ ] Dragging is smooth (no lag)
- [ ] Works on desktop (Chrome, Firefox, Safari)
- [ ] Disabled or adapted for mobile (<768px)

---

## For Browser (Developer Agent)

**Task**: Implement draggable/resizable windows in Mosaic

**Steps**:
1. `npm install react-draggable re-resizable`
2. Create `DraggableWindow.jsx` component
3. Wrap PS101 steps (or other key UI elements) in `<DraggableWindow>`
4. Test locally (drag, resize, bounds)
5. Add z-index management (windows come to front when clicked)
6. Add mobile detection (disable on small screens)
7. Deploy to Netlify
8. Test on production

**Estimated effort**: 2-4 hours (depending on how many components to wrap)

---

## Alternative: react-grid-layout

If you want a more structured grid system (like a dashboard):

- **Library**: `react-grid-layout`
- **Docs**: https://github.com/react-grid-layout/react-grid-layout
- **Use case**: Dashboard with widgets that snap to grid
- **Trade-off**: More structured, less freeform than draggable windows

---

**Ready for Browser to implement.**
