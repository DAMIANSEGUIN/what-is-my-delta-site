# **MOSAIC PLATFORM ARCHITECTURE**

## **COMPLETE SYSTEM OVERVIEW**

### **Platform Components**
- **Mosaic**: Umbrella product name
- **WIMD (What Is My Delta)**: Delta analysis service (deployed)
- **Opportunity Bridge (OB)**: Job matching and application system
- **Resume Rewrite Tool**: AI-powered resume optimization
- **Mosaic UI**: Frontend interface (Vercel deployment)

### **Current Status**
- **Backend**: FastAPI deployed on Railway (`https://what-is-my-delta-site-production.up.railway.app`)
- **Frontend**: Mosaic UI demo (needs production deployment)
- **Database**: SQLite with auto-cleanup (30-day expiry)
- **Storage**: Railway Pro (8GB limit)

---

## **UPDATED SITE ARCHITECTURE DIAGRAM**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MOSAIC PLATFORM ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER          │    │   MOSAIC UI     │    │   FASTAPI API   │    │   DATABASE      │
│   (Browser)     │◄──►│   (Vercel)      │◄──►│   (Railway)     │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │    │                 │
│ • whatismydelta.com │    │ • index.html    │    │ • WIMD endpoints │    │ • Sessions      │
│ • Chat interface │    │ • Chat UI        │    │ • OB endpoints  │    │ • WIMD outputs  │
│ • Upload modal  │    │ • Upload modal   │    │ • Resume tools  │    │ • Resume versions│
│ • Job matching  │    │ • Job matching   │    │ • File storage  │    │ • Job matches   │
│ • Resume rewrite│    │ • Resume rewrite │    │ • Auto-cleanup  │    │ • Auto-expiry   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────────┘

User Input → Mosaic UI → FastAPI → Database
     ↓           ↓         ↓         ↓
Session Data → Auto-Expire → User Export → No Permanent Storage

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              API ENDPOINTS ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────────┘

WIMD Service:                    OB Service:                     Resume Service:
├── POST /wimd                  ├── GET /ob/opportunities        ├── POST /resume/rewrite
├── POST /wimd/upload           ├── POST /ob/apply               ├── POST /resume/customize
├── GET /wimd/analysis          ├── GET /ob/matches             ├── POST /resume/feedback
└── GET /wimd/metrics          └── GET /ob/status               └── GET /resume/versions

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STORAGE ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────────┘

Railway Storage (8GB Pro):      User Data (30-day expiry):      Export/Import:
├── SQLite database             ├── Session data                ├── Project folder
├── File uploads                ├── WIMD outputs                ├── Resume versions
├── Resume versions             ├── Job matches                 ├── User preferences
└── Auto-cleanup job            └── Feedback data               └── Analysis results
```

---

## **DETAILED USER EXPERIENCE FLOW**

### **Phase 1: Landing & Onboarding**
```
1. User visits whatismydelta.com
   ↓
2. Mosaic UI loads (Vercel)
   ↓
3. Welcome screen: "Fast Track or Discovery?"
   ↓
4. Coach chat opens automatically: "hi — prefer fast track or discovery?"
   ↓
5. User chooses path
```

### **Phase 2: WIMD Analysis**
```
6. Chat with coach (POST /wimd)
   ├── Values exploration
   ├── Goals clarification
   ├── Skills assessment
   └── Challenges identification
   ↓
7. Upload files (POST /wimd/upload)
   ├── Resume
   ├── Documents
   ├── Audio/Video
   └── Analysis materials
   ↓
8. WIMD processes data
   ├── AI analysis
   ├── Delta calculation
   ├── Store results
   └── Generate metrics
   ↓
9. Show metrics dashboard
   ├── Clarity: 75%
   ├── Action: 45%
   ├── Momentum: 32%
   └── [Explore Opportunities] button
```

### **Phase 3: Opportunity Bridge**
```
10. User clicks "Explore Opportunities"
    ↓
11. Loading screen: "Finding your opportunities..."
    ↓
12. OB processes WIMD output
    ├── Match skills to jobs
    ├── Match values to companies
    ├── Match goals to roles
    └── Calculate fit scores
    ↓
13. Show job matches
    ├── Job title, company, location
    ├── Fit score (92%, 88%, etc.)
    ├── Skills match indicators
    ├── Values alignment
    └── [View Details] [Apply Now] buttons
```

### **Phase 4: Resume Rewrite**
```
14. User selects job to apply for
    ↓
15. Resume Rewrite tool opens
    ├── Upload current resume OR use WIMD-generated
    ├── Create canonical resume
    ├── Customize for specific job
    └── Feedback loop for improvements
    ↓
16. User iterates on resume
    ├── Tool suggests improvements
    ├── User makes edits
    ├── Get feedback on changes
    └── Save version
    ↓
17. Final resume ready
    ├── Job-optimized content
    ├── Skills highlighted
    ├── Values aligned
    └── Ready for application
```

### **Phase 5: Application & Follow-up**
```
18. User applies with optimized resume
    ↓
19. System tracks application
    ├── Status updates
    ├── Follow-up reminders
    ├── Additional opportunities
    └── Continue analysis
    ↓
20. User can continue journey
    ├── Apply to more jobs
    ├── Refine analysis
    ├── Update resume
    └── Export project data
```

---

## **ARCHITECTURE SUPPORT FOR USER EXPERIENCE**

### **Frontend (Mosaic UI)**
- **Single-page application** (no page reloads)
- **Progressive disclosure** (reveal complexity gradually)
- **Auto-save** (prevent data loss)
- **Error handling** (graceful failures)
- **Loading states** (clear feedback)

### **Backend (FastAPI)**
- **Session-based authentication** (no login required)
- **Auto-cleanup** (30-day expiry)
- **File handling** (upload, process, store)
- **AI integration** (OpenAI, Anthropic)
- **Job matching** (skills, values, goals)

### **Database (SQLite)**
- **Minimal schema** (sessions, data, files)
- **Auto-expiry** (privacy protection)
- **Export functionality** (user control)
- **Performance optimization** (indexed queries)

### **Storage (Railway)**
- **File uploads** (resumes, documents)
- **Version control** (resume iterations)
- **Cleanup jobs** (storage management)
- **Monitoring** (usage alerts)

---

## **TECHNICAL IMPLEMENTATION SPECIFICATIONS**

### **API Endpoints Required**

#### **WIMD Service**
```python
POST /wimd                    # Chat endpoint for coach interactions
POST /wimd/upload             # File upload handling (resumes, documents)
GET  /wimd/analysis          # Get WIMD analysis results
GET  /wimd/metrics           # Get user metrics (clarity, action, momentum)
```

#### **Opportunity Bridge Service**
```python
GET  /ob/opportunities        # Get job matches based on WIMD output
POST /ob/apply               # Submit job application
GET  /ob/matches             # Get user's job matches
GET  /ob/status              # Get application status
```

#### **Resume Rewrite Service**
```python
POST /resume/rewrite         # Create canonical resume from WIMD data
POST /resume/customize       # Customize resume for specific job
POST /resume/feedback        # Get improvement suggestions
GET  /resume/versions        # List and manage resume versions
```

### **Database Schema (SQLite)**

```sql
-- Sessions table
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    user_data JSON
);

-- WIMD analysis outputs
CREATE TABLE wimd_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    analysis_data JSON,
    metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Job matches from Opportunity Bridge
CREATE TABLE job_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    job_id TEXT,
    company TEXT,
    role TEXT,
    fit_score REAL,
    skills_match JSON,
    values_match JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Resume versions
CREATE TABLE resume_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    job_id TEXT,
    version_name TEXT,
    content TEXT,
    feedback JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- File uploads
CREATE TABLE file_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    filename TEXT,
    file_path TEXT,
    file_type TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### **Frontend Integration Points**

#### **Mosaic UI Updates Required**
```javascript
// Update askCoach function
async function askCoach(prompt) {
    const res = await fetch('https://what-is-my-delta-site-production.up.railway.app/wimd', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt })
    });
    const data = await res.json();
    return data?.result?.message || '(no response)';
}

// Add file upload functionality
document.getElementById('filePick').addEventListener('change', async (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const form = new FormData();
    form.append('file', f);
    const res = await fetch('https://what-is-my-delta-site-production.up.railway.app/wimd/upload', {
        method: 'POST',
        body: form
    });
    const data = await res.json();
    // Handle response
});

// Add job matching functionality
async function getOpportunities() {
    const res = await fetch('https://what-is-my-delta-site-production.up.railway.app/ob/opportunities');
    const data = await res.json();
    return data.opportunities;
}

// Add resume rewrite functionality
async function rewriteResume(jobId) {
    const res = await fetch('https://what-is-my-delta-site-production.up.railway.app/resume/rewrite', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ job_id: jobId })
    });
    const data = await res.json();
    return data.resume;
}
```

---

## **PRIVACY & STORAGE STRATEGY**

### **Privacy-First Approach**
- **No permanent user data** (30-day auto-expiry)
- **Session-based only** (no accounts required)
- **User-controlled data** (export/import functionality)
- **No behavioral tracking** (privacy-focused)

### **Storage Management**
- **Railway Pro**: 8GB storage limit
- **Auto-cleanup**: Daily cleanup of expired sessions
- **File compression**: Optimize stored data
- **Monitoring**: Alert when approaching limits

### **Data Flow**
```
User Input → Session Storage → Auto-Expiry (30 days) → User Export
     ↓              ↓              ↓              ↓
WIMD Analysis → Database → Cleanup Job → Project Folder
```

---

## **SUCCESS METRICS**

### **User Experience Success**
- **Completes WIMD analysis** (chat + upload)
- **Sees relevant job matches** (OB integration)
- **Creates optimized resume** (Resume Rewrite tool)
- **Takes action** (applies to jobs)

### **Technical Success**
- **All endpoints respond** < 2 seconds
- **File uploads complete** < 30 seconds
- **Database queries** < 1 second
- **Storage usage** < 8GB
- **Auto-cleanup working** effectively

### **Business Success**
- **Users complete journey** (analysis → jobs)
- **Users apply to jobs** (real outcomes)
- **Users return** (engagement)
- **Users recommend** (growth)

---

## **IMPLEMENTATION ROADMAP**

### **Phase 1: Backend Extensions**
- Implement missing API endpoints
- Add SQLite database schema
- Add error handling and validation
- Add storage management and cleanup
- Add session management

### **Phase 2: Frontend Integration**
- Update Mosaic UI with real API calls
- Add job matching interface
- Add resume rewrite functionality
- Add error handling and loading states
- Add user feedback mechanisms

### **Phase 3: Testing & Deployment**
- Create comprehensive integration tests
- Deploy frontend to Vercel
- Test complete user journey
- Performance optimization
- Storage monitoring

### **Phase 4: Maintenance & Scaling**
- Monitor storage usage and cleanup
- Handle user feedback and improvements
- Scale system as needed
- Maintain system health

---

## **ERROR HANDLING & RECOVERY**

### **User Experience Errors**
- **Chat timeout** → Retry button + error message
- **Upload fails** → Clear error + retry option
- **No jobs found** → Alternative suggestions
- **Session lost** → Auto-recovery + export option

### **Technical Errors**
- **API 404** → Fallback UI + contact support
- **Database error** → Graceful degradation
- **Rate limit** → Queue system + user notification
- **CORS issues** → Preflight handling

### **Recovery Actions**
- **Retry mechanisms** for failed operations
- **Fallback options** for critical features
- **User notification** for system issues
- **Support contact** for unresolved problems

---

## **DEPLOYMENT ARCHITECTURE**

### **Current Deployment**
- **Backend**: Railway (`what-is-my-delta-site-production.up.railway.app`)
- **Frontend**: Mosaic UI demo (needs Vercel deployment)
- **Domain**: `whatismydelta.com` (custom domain setup)
- **Database**: SQLite (Railway filesystem)

### **Target Deployment**
- **Backend**: Railway Pro (8GB storage)
- **Frontend**: Vercel (static hosting)
- **Domain**: `whatismydelta.com` (custom domain)
- **Database**: SQLite with auto-cleanup
- **Storage**: Railway + external if needed

---

## **MONITORING & MAINTENANCE**

### **System Monitoring**
- **Storage usage** (alert at 80% capacity)
- **Response times** (alert if > 2 seconds)
- **Error rates** (alert if > 5%)
- **User sessions** (track active users)

### **Maintenance Tasks**
- **Daily cleanup** (expired sessions)
- **Weekly optimization** (database maintenance)
- **Monthly review** (performance analysis)
- **Quarterly scaling** (capacity planning)

---

## **SECURITY CONSIDERATIONS**

### **Data Protection**
- **No permanent storage** (30-day expiry)
- **Session-based authentication** (no passwords)
- **File upload validation** (type, size limits)
- **CORS configuration** (domain restrictions)

### **Privacy Compliance**
- **GDPR compliance** (data minimization)
- **User control** (export/delete rights)
- **Transparent processing** (clear data usage)
- **No third-party sharing** (local processing only)

---

## **SCALING STRATEGY**

### **Current Capacity**
- **Railway Free**: 1GB storage, 512MB RAM
- **Target**: Railway Pro (8GB storage, 8GB RAM)
- **Users**: 100-1000 concurrent sessions
- **Storage**: 20-85MB per user session

### **Future Scaling**
- **External storage** (S3/Cloudinary) if needed
- **Database optimization** (indexing, queries)
- **CDN integration** (static assets)
- **Load balancing** (multiple instances)

---

## **INTEGRATION POINTS**

### **WIMD → OB Handoff**
```python
# Data flow from WIMD to Opportunity Bridge
wimd_data = {
    "skills": ["Python", "AI", "Leadership"],
    "values": ["Innovation", "Growth", "Impact"],
    "goals": ["Senior Developer", "Product Management"],
    "experience": "5 years",
    "location": "San Francisco",
    "salary_range": "$120k-$150k"
}

# OB processes WIMD output
def find_opportunities(wimd_data):
    # Match skills to job requirements
    # Match values to company culture
    # Match goals to role level
    # Calculate fit scores
    return job_matches
```

### **OB → Resume Rewrite Handoff**
```python
# Data flow from OB to Resume Rewrite
job_requirements = {
    "role": "Senior Python Developer",
    "company": "TechCorp",
    "skills_required": ["Python", "AI", "Leadership"],
    "values_alignment": ["Innovation", "Growth"],
    "experience_level": "Senior"
}

# Resume Rewrite processes job requirements
def create_customized_resume(wimd_data, job_requirements):
    # Combine WIMD analysis with job requirements
    # Generate job-specific resume
    # Return optimized resume
    return customized_resume
```

---

## **TESTING STRATEGY**

### **Unit Testing**
- **API endpoints** (individual function testing)
- **Database operations** (CRUD operations)
- **File handling** (upload, processing, storage)
- **Error scenarios** (failure handling)

### **Integration Testing**
- **End-to-end user journey** (WIMD → OB → Resume)
- **API integration** (frontend ↔ backend)
- **Database integration** (data persistence)
- **File processing** (upload → analysis → storage)

### **Performance Testing**
- **Response times** (API endpoints)
- **File uploads** (large file handling)
- **Database queries** (query optimization)
- **Concurrent users** (load testing)

### **User Experience Testing**
- **Interface functionality** (UI interactions)
- **Error handling** (graceful failures)
- **Loading states** (user feedback)
- **Data persistence** (session management)

---

## **DOCUMENTATION REQUIREMENTS**

### **Technical Documentation**
- **API specifications** (endpoint documentation)
- **Database schema** (table relationships)
- **Deployment guide** (setup instructions)
- **Troubleshooting guide** (common issues)

### **User Documentation**
- **User guide** (how to use the platform)
- **FAQ** (common questions)
- **Support contact** (help resources)
- **Privacy policy** (data handling)

---

## **CONCLUSION**

This architecture provides a complete, scalable, and privacy-focused platform for the Mosaic system. The implementation follows a clear roadmap with specific deliverables, success criteria, and maintenance requirements. The system is designed to be simple for users while providing powerful functionality for career development and job matching.

The three-AI collaboration system (Codex, Claude Code, Human) ensures proper implementation, debugging, and oversight throughout the development process.
