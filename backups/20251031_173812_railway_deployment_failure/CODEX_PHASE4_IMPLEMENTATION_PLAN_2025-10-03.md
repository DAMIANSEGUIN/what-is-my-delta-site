# CODEX PHASE 4 IMPLEMENTATION PLAN - 2025-10-03
## RAG Baseline + Job Feeds Integration

**Prepared by**: Implementation SSE (Claude in Cursor)  
**For Review by**: CODEX (Systematic Planning Engineer)  
**Date**: 2025-10-03  
**Status**: Awaiting CODEX Review and Approval  

---

## 🎯 **EXECUTIVE SUMMARY**

### **Phase 4 Objectives**
- Implement RAG (Retrieval-Augmented Generation) baseline for intelligent job matching
- Integrate multiple job data sources (Greenhouse, SerpApi, Reddit)
- Enable "Find Jobs" functionality currently disabled in production
- Provide AI-enhanced job recommendations based on user profile and experiments

### **Business Impact**
- **User Experience**: Enable job discovery and application workflow
- **System Capability**: Intelligent job matching using user's learning data
- **Data Integration**: Connect experiments/learning evidence to job recommendations
- **Production Ready**: Complete the Mosaic 2.0 feature set

### **Timeline**
- **Estimated Duration**: 6 hours (per acceleration plan)
- **Dependencies**: Phase 3 complete ✅
- **Risk Level**: Medium (new AI integrations, external APIs)

---

## 📋 **DETAILED IMPLEMENTATION PLAN**

### **Task 1: RAG Engine Implementation (2 hours)**

#### **1.1 Embedding Pipeline**
- **File**: `api/rag_engine.py` (already started)
- **Components**:
  - OpenAI ADA-002 embedding integration
  - Batch processing with rate limiting
  - Caching system for performance
  - Error handling and retries
- **Dependencies**: OpenAI API key, database storage
- **Testing**: Unit tests for embedding computation

#### **1.2 Retrieval Wrapper**
- **Components**:
  - Cosine similarity calculation
  - Confidence threshold logic (0.7 default)
  - Fallback to AI when retrieval fails
  - Performance monitoring
- **Integration**: Connect to existing prompt selector system
- **Testing**: Similarity accuracy, fallback behavior

#### **1.3 Database Schema**
- **Migration**: `004_add_rag_tables.sql` (already created)
- **Tables**:
  - `embeddings` - Store text embeddings
  - `job_postings` - Cache job data
  - `job_search_cache` - Performance optimization
  - `rag_usage` - Usage tracking
- **Indexes**: Performance optimization for queries

### **Task 2: Job Sources Integration (2 hours)**

#### **2.1 Job Sources Interface**
- **Files**: `api/job_sources/` (already started)
- **Sources**:
  - **Greenhouse**: Tech jobs, startups
  - **SerpApi**: Google Jobs, LinkedIn, Indeed
  - **Reddit**: r/forhire, r/remotejs
- **Standardization**: Common job posting format
- **Rate Limiting**: Per-source and global limits

#### **2.2 Job Sources Catalog**
- **File**: `docs/job_sources_catalog.md` (already created)
- **Content**: Approved sources, rate limits, implementation status
- **Governance**: Review process for new sources
- **Monitoring**: Health checks and error tracking

#### **2.3 API Integration**
- **Endpoints**: `/jobs/search`, `/jobs/{job_id}`
- **Features**:
  - Multi-source job search
  - Deduplication across sources
  - Detailed job information
  - Caching for performance
- **Error Handling**: Graceful degradation on API failures

### **Task 3: Coach Integration (1 hour)**

#### **3.1 Context Enhancement**
- **Integration**: Include experiments/learning evidence in coach context
- **Data Sources**:
  - User's experiment history
  - Learning data and confidence scores
  - Self-efficacy metrics
  - Skill development patterns
- **Implementation**: Update coach prompt generation

#### **3.2 Job Matching Logic**
- **Algorithm**: Match jobs based on user profile
- **Factors**:
  - Skills from experiments
  - Learning velocity and confidence
  - Experience level preferences
  - Location and remote preferences
- **Scoring**: Weighted job relevance scoring

### **Task 4: Frontend Integration (1 hour)**

#### **4.1 Job Search UI**
- **Location**: `mosaic_ui/index.html`
- **Components**:
  - Job search form
  - Results display
  - Job detail modal
  - Apply button integration
- **Design**: Consistent with existing UI

#### **4.2 Opportunity Cards**
- **Integration**: Connect to existing opportunity system
- **Features**:
  - Live job data population
  - AI-enhanced recommendations
  - User preference learning
- **Performance**: Lazy loading and caching

---

## 🔧 **TECHNICAL SPECIFICATIONS**

### **RAG Engine Architecture**
```
User Query → Embedding → Similarity Search → Confidence Check → Response
     ↓              ↓              ↓              ↓
   Cache        Database        Threshold      AI Fallback
```

### **Job Sources Data Flow**
```
User Search → Multi-Source Query → Deduplication → Relevance Scoring → Ranked Results
```

### **Database Schema**
- **embeddings**: text_hash, text, embedding, model, metadata, created_at
- **job_postings**: id, title, company, location, description, url, source, metadata
- **job_search_cache**: query_hash, query, location, results, expires_at
- **rag_usage**: session_id, operation, query_text, confidence, response_time

---

## 🚨 **RISK ASSESSMENT**

### **High Risk**
- **External API Dependencies**: Job sources may be unreliable
- **Rate Limiting**: Multiple APIs with different limits
- **Data Quality**: Inconsistent job data formats

### **Medium Risk**
- **Performance**: Embedding computation can be slow
- **Cost**: OpenAI API usage for embeddings
- **Integration**: Complex data flow between systems

### **Low Risk**
- **Database**: Standard SQLite operations
- **Frontend**: Simple UI updates
- **Testing**: Well-defined interfaces

### **Mitigation Strategies**
- **Fallback Systems**: Graceful degradation on API failures
- **Caching**: Reduce API calls and improve performance
- **Monitoring**: Health checks and error tracking
- **Rate Limiting**: Respectful API usage

---

## 📊 **SUCCESS CRITERIA**

### **Functional Requirements**
- [ ] RAG engine computes embeddings successfully
- [ ] Job search returns results from multiple sources
- [ ] Coach integration includes user context
- [ ] Frontend displays job results correctly
- [ ] Apply button functionality works

### **Performance Requirements**
- [ ] Embedding computation < 2 seconds
- [ ] Job search < 5 seconds
- [ ] Database queries optimized
- [ ] API rate limits respected

### **Quality Requirements**
- [ ] Error handling for all failure modes
- [ ] Logging and monitoring implemented
- [ ] Unit tests for core functionality
- [ ] Integration tests for end-to-end flow

---

## 🚀 **IMPLEMENTATION TIMELINE**

### **Hour 1-2: RAG Engine**
- Complete embedding pipeline
- Implement retrieval wrapper
- Add database migrations
- Test core functionality

### **Hour 3-4: Job Sources**
- Complete job sources interface
- Implement API integrations
- Add caching and error handling
- Test multi-source search

### **Hour 5: Coach Integration**
- Update coach context with user data
- Implement job matching logic
- Test integration with existing systems

### **Hour 6: Frontend Integration**
- Update UI for job search
- Connect to backend APIs
- Test complete user flow
- Performance optimization

---

## 🔄 **INTEGRATION POINTS**

### **With Phase 3 (Self-Efficacy)**
- Use experiment data for job matching
- Include confidence scores in recommendations
- Leverage learning velocity for job suggestions

### **With Phase 1 (Prompt Selector)**
- Integrate RAG with existing prompt system
- Maintain CSV fallback when RAG fails
- Use AI fallback for enhanced responses

### **With Existing Systems**
- Connect to user authentication
- Integrate with session management
- Use existing database connections

---

## 📋 **DEPLOYMENT REQUIREMENTS**

### **Environment Variables**
- `OPENAI_API_KEY` - For embedding computation
- `SERPAPI_API_KEY` - For job search
- `GREENHOUSE_API_KEY` - For Greenhouse jobs
- `RAG_BASELINE` - Feature flag for RAG functionality

### **Database Changes**
- Run migration `004_add_rag_tables.sql`
- Verify table creation and indexes
- Test data insertion and queries

### **API Endpoints**
- `/rag/embed` - Compute embeddings
- `/rag/retrieve` - Similarity search
- `/rag/query` - RAG responses
- `/jobs/search` - Job search
- `/jobs/{job_id}` - Job details
- `/health/rag` - Health check

---

## 🎯 **APPROVAL REQUEST**

### **CODEX Review Required**
1. **Technical Approach**: Is the RAG implementation approach sound?
2. **Job Sources**: Are the selected sources appropriate?
3. **Integration**: Will this integrate well with existing systems?
4. **Timeline**: Is 6 hours realistic for this scope?
5. **Risks**: Are the identified risks acceptable?

### **Questions for CODEX**
1. Should we prioritize certain job sources over others?
2. What confidence threshold is appropriate for RAG responses?
3. How should we handle API rate limiting across multiple sources?
4. Should we implement real-time job updates or batch processing?
5. What monitoring and alerting should we implement?

---

## 📞 **NEXT STEPS**

### **Upon CODEX Approval**
1. **Begin Implementation**: Start with RAG engine
2. **Regular Updates**: Provide progress updates every 2 hours
3. **Testing**: Continuous testing throughout implementation
4. **Documentation**: Update all documentation as changes are made

### **Upon CODEX Rejection**
1. **Address Concerns**: Modify plan based on CODEX feedback
2. **Resubmit**: Updated implementation plan for review
3. **Iterate**: Continue until approval is granted

---

## 📝 **REVISION 1 - CODEX FEEDBACK ADDRESSED**

### **Data Store Strategy**
- **Embedding Storage**: Cap stored vectors to 500 entries per category (recent first)
- **Purge Strategy**: Daily cleanup job removes embeddings older than 30 days
- **Compaction**: Weekly SQLite VACUUM to maintain performance
- **Size Monitoring**: Alert if database exceeds 100MB

### **Rate/Cost Guardrails**
- **OpenAI Limits**: 60 requests/minute, $0.0001/1K tokens (ADA-002)
- **SerpApi Limits**: 100 requests/month (free tier), $50/month (paid)
- **Caching TTL**: Embeddings cached 24 hours, job results cached 1 hour
- **Cost Monitoring**: Daily usage tracking, alert at $10/day threshold

### **Job Source Compliance**
- **SerpApi**: Paid service ($50/month), ToS compliance required
- **Reddit**: Free API, respect rate limits and User-Agent requirements
- **Greenhouse**: Free tier available, respect rate limits
- **Legal Notes**: Update `docs/job_sources_catalog.md` with ToS requirements
- **Key Management**: Human gatekeeper manages API keys and billing

### **Testing Plan**
- **Unit Tests**: `tests/test_rag_engine.py`, `tests/test_job_sources.py`
- **Integration Tests**: `tests/test_job_search_integration.py`
- **Smoke Script**: `scripts/test_phase4_endpoints.sh`
- **Full Check**: Extend `scripts/full_check.sh` to include Phase 4 tests
- **Coverage**: Embedding computation, job search, RAG responses, error handling

### **Fallback Order (Explicit)**
1. **CSV Match**: Check prompts CSV with threshold 0.55
2. **RAG Retrieval**: If RAG_BASELINE enabled and confidence ≥ 0.7
3. **AI Fallback**: If RAG fails or confidence < 0.7
4. **Metrics Fallback**: Final fallback using user metrics

### **Monitoring Hooks**
- **Logging**: `rag_usage` table tracks all RAG operations
- **Job Source Monitoring**: Track API failures and rate limits
- **Health Checks**: `/health/rag` endpoint checked every 5 minutes
- **Alert Thresholds**: >5% error rate, >$10/day cost, >100MB database
- **Metrics**: Response times, confidence scores, fallback usage

---

**Status**: Updated per CODEX feedback - Ready for re-review  
**Timeline**: 6 hours estimated upon approval  
**Confidence**: High - all gaps addressed  
**Dependencies**: CODEX re-review and formal approval required  

---

**Prepared by**: Implementation SSE (Claude in Cursor)  
**Date**: 2025-10-03  
**Revision**: 1 - CODEX feedback addressed  
**Next**: CODEX re-review and formal approval
