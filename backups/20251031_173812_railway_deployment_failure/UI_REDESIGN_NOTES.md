# UI Redesign Notes - Mosaic Coaching Console

**Date**: 2025-10-02  
**Focus**: Interface Simplification - Coaching Console Design  
**Status**: Prototype Complete

---

## **DESIGN PRINCIPLES**

### **Core Philosophy**
Think "coaching console" instead of dashboard sprawl—three zones, nothing else.

### **Visual References**
- **Linear.app's task pane**: Clean, focused task management
- **Superhuman's focus mode**: Minimal distractions, clear actions
- **Notion's toggle cards**: Collapsible content, organized hierarchy

### **Design System**
- **Accent colors**: Keep existing brand colors but use sparingly
- **Whitespace**: Primary design element for segmentation
- **Typography**: Hierarchy through font weights and sizes, not colors
- **No embedded forms**: Single text input + optional dropdown
- **Avoid tables**: Use bullet tiles and card layouts

---

## **THREE-ZONE ARCHITECTURE**

### **Zone 1: Prompt Stream**
**Purpose**: Chat interface with coach interaction and metrics display

**Components**:
- **Chat Pane**: User prompts and coach replies (CSV/AI responses)
- **Metrics Bar**: Key MOSAIC metrics (Clarity, Action, Momentum)
- **Input Area**: Single text box + focus dropdown + send button

**Design Rules**:
- No embedded forms or complex UI elements
- Clear message threading (user vs coach)
- Metrics always visible but unobtrusive
- Focus dropdown for context (General, Build, Buy, Signal)

### **Zone 2: Opportunity Snapshot**
**Purpose**: Top 3 opportunities with signal tags and confidence scores

**Components**:
- **Opportunity Cards**: Role title, confidence badge, signal tags
- **Actions**: Save/Ignore buttons for each opportunity
- **Collapsible Panel**: Can be minimized to save space

**Design Rules**:
- One card per track (Build, Buy, Signal)
- Confidence scoring with color coding
- Signal tags for quick categorization
- Simple save/ignore actions

### **Zone 3: Action Ledger**
**Purpose**: Minimal list of next steps and actionable items

**Components**:
- **Action Items**: Icon + title + description + link
- **Categories**: Resume, Research, Contact, Portfolio
- **Collapsible Panel**: Can be minimized to save space

**Design Rules**:
- Avoid tables, use bullet tiles
- Clear action hierarchy
- Direct links to next steps
- Minimal visual noise

---

## **TECHNICAL IMPLEMENTATION**

### **Layout System**
```css
.console {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
    max-width: 1400px;
    margin: 0 auto;
    padding: 24px;
}
```

### **Responsive Behavior**
- **Desktop**: Three-column layout
- **Tablet/Mobile**: Single column stack
- **Collapsible panels**: Can be minimized independently

### **Color System**
```css
/* Primary Colors */
--background: #fafafa;
--surface: #ffffff;
--border: #e5e5e5;

/* Text Colors */
--text-primary: #1a1a1a;
--text-secondary: #6b7280;

/* Accent Colors */
--accent-blue: #2563eb;
--accent-green: #166534;
--accent-yellow: #92400e;
--accent-red: #991b1b;
```

### **Typography Scale**
```css
/* Headers */
.zone-header { font-size: 14px; font-weight: 600; text-transform: uppercase; }

/* Body Text */
.message { font-size: 14px; line-height: 1.5; }

/* Small Text */
.signal-tag { font-size: 11px; }
.action-description { font-size: 13px; }
```

---

## **INTERACTION PATTERNS**

### **Chat Interface**
- **Enter key**: Send message
- **Focus dropdown**: Context selection (General, Build, Buy, Signal)
- **Auto-scroll**: New messages appear at bottom
- **Message threading**: Clear user vs coach distinction

### **Opportunity Management**
- **Save/Ignore**: Simple binary actions
- **Confidence scoring**: Visual indicators (High/Medium/Low)
- **Signal tags**: Quick categorization
- **Collapsible**: Can minimize to focus on other zones

### **Action Tracking**
- **Direct links**: Each action has a clear next step
- **Icon system**: Visual categorization (Resume, Research, Contact, Portfolio)
- **Progress indication**: Clear action hierarchy
- **Collapsible**: Can minimize to focus on other zones

---

## **BACKEND INTEGRATION REQUIREMENTS**

### **API Endpoints Needed**
```javascript
// Chat Interface
POST /wimd                    // Send message, get coach response
GET  /wimd/metrics           // Get current MOSAIC metrics

// Opportunity Management
GET  /ob/opportunities       // Get top 3 opportunities
POST /ob/save                // Save opportunity
POST /ob/ignore              // Ignore opportunity

// Action Tracking
GET  /actions/ledger          // Get action items
POST /actions/complete        // Mark action as complete
POST /actions/create          // Create new action
```

### **Data Flow**
```
User Input → Coach Response → Metrics Update → Opportunity Refresh → Action Update
     ↓              ↓              ↓              ↓              ↓
Chat Pane → Coach Reply → Metrics Bar → Opportunity Cards → Action Items
```

---

## **FUTURE ENHANCEMENTS**

### **Phase 1: Core Functionality**
- [ ] Wire chat interface to `/wimd` endpoint
- [ ] Connect metrics to `/wimd/metrics` endpoint
- [ ] Implement opportunity save/ignore actions
- [ ] Add action item creation and completion

### **Phase 2: Advanced Features**
- [ ] Real-time updates via WebSocket
- [ ] Drag-and-drop opportunity reordering
- [ ] Action item due dates and reminders
- [ ] Export functionality for opportunities and actions

### **Phase 3: Personalization**
- [ ] Customizable zone layouts
- [ ] Saved focus preferences
- [ ] Personal coaching style settings
- [ ] Advanced filtering and search

---

## **PROTOTYPE STATUS**

### **Completed**
- ✅ Three-zone layout implementation
- ✅ Responsive design system
- ✅ Collapsible panel functionality
- ✅ Chat interface mockup
- ✅ Opportunity card design
- ✅ Action ledger layout

### **Next Steps**
1. **Backend Integration**: Wire to actual API endpoints
2. **Data Binding**: Connect to real MOSAIC metrics and opportunities
3. **User Testing**: Validate the simplified interface approach
4. **Performance**: Optimize for real-time updates

---

## **DESIGN VALIDATION**

### **User Experience Goals**
- **Clarity**: No confusion about what to do next
- **Focus**: Minimal distractions, clear priorities
- **Efficiency**: Quick access to key information and actions
- **Progress**: Clear sense of forward momentum

### **Success Metrics**
- **Time to first action**: < 30 seconds
- **Task completion rate**: > 80%
- **User satisfaction**: > 4.5/5
- **Interface comprehension**: > 90% without training

---

**Last Updated**: 2025-10-02  
**Next Review**: After backend integration  
**Maintained By**: UI/UX Team

