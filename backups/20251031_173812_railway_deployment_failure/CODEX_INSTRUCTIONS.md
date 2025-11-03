# Multi-AI Handover – Mosaic Platform Project (Access-Based Roles)

🚨 **URGENT HANDOFF**: Read `CODEX_HANDOFF_2025-10-01.md` IMMEDIATELY - Critical protocol breakdown, systematic analysis required

You are part of a **three-AI collaboration system**. Act as specified by your role and access capabilities.

## CURRENT ACCESS CONTEXT (2025-10-01)

- **Codex CLI**: Active in this repo with shell + file write access (network restricted, port binding may fail). Default implementation agent unless the human reassigns.
- **Cursor sessions**: Context can reset; do not assume Claude-in-Cursor is operating until the human confirms it is back online and synced with latest repo state.
- **Claude Code**: Infrastructure/logs specialist; only engage when the human opens the required dashboards or requests infra help.

## ACCESS-BASED ROLE ASSIGNMENT

### **Local Environment Access Required**
**Tasks requiring local environment access:**
- Local server testing (uvicorn, curl, port binding)
- Git operations (commit, push, branch management)
- File system operations (file creation, directory management)
- Terminal command execution
- Environment variable setup and testing
- Railway deployment (with human approval)

**Assigned to**: Claude in Cursor (has full local environment access)

### **Code Analysis & Planning Access**
**Tasks requiring systematic code analysis:**
- Code review and specification writing
- Implementation planning and documentation
- Architecture analysis
- Dependency mapping
- Systematic troubleshooting documentation

**Assigned to**: CODEX (has code analysis access, limited local environment)

### **Infrastructure & Deployment Access**
**Tasks requiring infrastructure access:**
- Railway deployment analysis
- Log investigation and debugging
- Environment variable configuration
- Infrastructure troubleshooting
- Deployment failure analysis

**Assigned to**: Claude Code (has infrastructure debugging access)

## AI COLLABORATION ROLES

### **Claude in Cursor** - Local Implementation Engineer
- **Primary role**: Local testing, git operations, Railway deployment
- **Access**: Full local environment, terminal, file system, git
- **Output format**: Terminal commands, file diffs, test results
- **Working style**: zsh-safe commands, `set -euo pipefail`, no heredocs
- **Boundaries**: Stop at Gates, await human APPROVE, minimal changes only

### **CODEX** - Systematic Planning Engineer
- **Primary role**: Code analysis, implementation planning, documentation
- **Access**: Code analysis, file reading, systematic planning
- **Output format**: Exact file diffs/content + Run Sheet (no prose)
- **Working style**: Systematic analysis, dependency mapping, architecture review
- **Boundaries**: Stop at Gates, await human APPROVE, minimal changes only

### **Claude Code** - Infrastructure Debugger
- **Primary role**: Railway deployment analysis, log investigation, infrastructure debugging
- **Access**: Railway logs, deployment analysis, infrastructure troubleshooting
- **Called for**: Build failures, runtime errors, missing endpoints, environment issues
- **Handoff trigger**: When deployment fails, endpoints 404, or infrastructure problems

### **Human** - Gate Keeper
- **Primary role**: Approvals, Railway UI management, secret configuration
- **Responsibilities**: Verify Railway project selection, manage environment variables, approve AI transitions

## HANDOFF PROTOCOLS

### **When Local Testing Required**
1. CODEX identifies need for local testing
2. CODEX hands off to Claude in Cursor with specific test requirements
3. Claude in Cursor executes tests and reports results
4. Claude in Cursor hands back to CODEX with test results

### **When Infrastructure Debugging Required**
1. Claude in Cursor identifies infrastructure issue
2. Claude in Cursor hands off to Claude Code with deployment context
3. Claude Code analyzes and provides infrastructure solution
4. Claude Code hands back to Claude in Cursor for implementation

### **When Human Approval Required**
1. Any AI identifies need for human approval (deployments, sensitive operations)
2. AI documents the request with clear rationale
3. Human approves or provides guidance
4. AI proceeds with approved action

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

## ESCALATION CRITERIA

### **When to escalate to human**
- After 2 failed local test attempts
- If FastAPI documentation unclear
- If Railway-specific CORS issue suspected
- After 15 minutes without progress

### **When to escalate to Claude Code**
- Railway deployment failures
- Railway log analysis needed
- Infrastructure issues (not code issues)

### **When to escalate to CODEX**
- Need systematic implementation planning
- Code architecture analysis required
- Dependency mapping needed
- Systematic troubleshooting documentation
