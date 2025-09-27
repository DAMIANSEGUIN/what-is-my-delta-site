# Multi-AI Handover – Mosaic Platform Project

You are part of a **three-AI collaboration system**. Act as specified by your role.

## AI COLLABORATION ROLES

### **Codex/Cursor** (You) - Implementation Engineer
- **Primary role**: File implementation, exact diffs, code changes
- **Output format**: Exact file diffs/content + Run Sheet (no prose)
- **Working style**: zsh-safe commands, `set -euo pipefail`, no heredocs
- **Boundaries**: Stop at Gates, await human APPROVE, minimal changes only

### **Claude Code** - Senior Debugger  
- **Primary role**: Railway deployment analysis, log investigation, infrastructure debugging
- **Called for**: Build failures, runtime errors, missing endpoints, environment issues
- **Handoff trigger**: When deployment fails, endpoints 404, or infrastructure problems

### **Human** - Gate Keeper
- **Primary role**: Approvals, Railway UI management, secret configuration
- **Responsibilities**: Verify Railway project selection, manage environment variables, approve AI transitions

## MOSAIC PLATFORM SCOPE

### **Complete Architecture**
- **WIMD (What Is My Delta)**: Delta analysis service (deployed)
- **Opportunity Bridge (OB)**: Job matching and application system
- **Resume Rewrite Tool**: AI-powered resume optimization
- **Mosaic UI**: Frontend interface (Vercel deployment)

### **Backend Extensions (Codex)**
- **POST /wimd**: Chat endpoint for coach interactions
- **POST /wimd/upload**: File upload handling (resumes, documents)
- **GET /ob/opportunities**: Job matching based on WIMD output
- **POST /ob/apply**: Job application submission
- **POST /resume/rewrite**: Create canonical resume from WIMD data
- **POST /resume/customize**: Customize resume for specific jobs
- **POST /resume/feedback**: Get improvement suggestions
- **GET /resume/versions**: List and manage resume versions

### **Frontend Integration (Codex)**
- **Update mosaic_ui/index.html**: Wire real API calls
- **Add job matching interface**: Display opportunities with fit scores
- **Add resume rewrite functionality**: User-friendly resume tool
- **Add error handling**: Graceful failure management
- **Add loading states**: Clear user feedback

### **Database Schema (Codex)**
- **SQLite with auto-expiry**: 30-day session cleanup
- **Sessions table**: User session management
- **WIMD outputs**: Analysis results and metrics
- **Job matches**: Opportunity Bridge results
- **Resume versions**: Resume iterations and feedback
- **Storage monitoring**: Usage tracking and cleanup

### **Testing Requirements (Codex)**
- **Integration tests**: End-to-end user journey
- **Error scenario testing**: Failure handling
- **Performance testing**: Response times and storage
- **User experience testing**: Interface functionality

## PROJECT PHASES

### **Phase 1: Backend Extensions (Codex)**
- Implement missing API endpoints
- Add SQLite database schema
- Add error handling and validation
- Add storage management and cleanup
- Add session management

### **Phase 2: Frontend Integration (Codex)**
- Update Mosaic UI with real API calls
- Add job matching interface
- Add resume rewrite functionality
- Add error handling and loading states
- Add user feedback mechanisms

### **Phase 3: Testing & Deployment (Codex)**
- Create comprehensive integration tests
- Deploy frontend to Vercel
- Test complete user journey
- Performance optimization
- Storage monitoring

### **Phase 4: Maintenance & Scaling (Codex)**
- Monitor storage usage and cleanup
- Handle user feedback and improvements
- Scale system as needed
- Maintain system health

## SUCCESS CRITERIA

### **Technical Requirements**
- All API endpoints implemented and functional
- Database schema created with auto-cleanup
- Frontend fully integrated with backend
- Error handling comprehensive
- Testing suite passing

### **User Experience Requirements**
- Seamless WIMD → OB → Resume flow
- Job matching accuracy and relevance
- Resume rewrite functionality
- Application tracking
- Data export/import capabilities

### **Performance Requirements**
- Response times < 2 seconds
- File uploads < 30 seconds
- Database queries < 1 second
- Storage usage < 8GB (Railway Pro)
- Auto-cleanup working effectively