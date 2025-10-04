# Job Sources Catalog - Mosaic 2.0

This document catalogs approved job data sources for the Mosaic platform.

## Approved Sources

### 1. Greenhouse
- **Status**: ✅ Approved
- **Type**: Job board API
- **Rate Limit**: 60 requests/minute
- **Coverage**: Tech jobs, startups, mid-size companies
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/greenhouse.py`
- **Compliance**: ✅ Production-ready (API key available)

### 2. SerpApi
- **Status**: ✅ Approved  
- **Type**: Search API aggregator
- **Rate Limit**: 100 requests/minute
- **Coverage**: Google Jobs, LinkedIn, Indeed, etc.
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/serpapi.py`
- **Compliance**: ✅ Production-ready (API key available)

### 3. Reddit
- **Status**: ✅ Approved
- **Type**: Forum scraping
- **Rate Limit**: 60 requests/minute
- **Coverage**: r/forhire, r/remotejs, r/jobs
- **API Key Required**: No
- **Implementation**: `api/job_sources/reddit.py`
- **Compliance**: ✅ Production-ready (no API key required)

### 4. Indeed
- **Status**: ✅ Approved
- **Type**: Job board API
- **Rate Limit**: 100 requests/minute
- **Coverage**: Corporate jobs, all industries
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/indeed.py`

### 5. LinkedIn
- **Status**: ✅ Approved
- **Type**: Professional network API
- **Rate Limit**: 100 requests/minute
- **Coverage**: Professional jobs, corporate positions
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/linkedin.py`

### 6. Glassdoor
- **Status**: ✅ Approved
- **Type**: Job board API
- **Rate Limit**: 100 requests/minute
- **Coverage**: Company reviews, salary data, jobs
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/glassdoor.py`

### 7. RemoteOK
- **Status**: ✅ Approved
- **Type**: Remote job board
- **Rate Limit**: 60 requests/minute
- **Coverage**: Remote jobs, tech positions
- **API Key Required**: No
- **Implementation**: `api/job_sources/remoteok.py`
- **Compliance**: ✅ Production-ready (no API key required)

### 8. WeWorkRemotely
- **Status**: ✅ Approved
- **Type**: Remote job board
- **Rate Limit**: 60 requests/minute
- **Coverage**: Remote jobs, all industries
- **API Key Required**: No
- **Implementation**: `api/job_sources/weworkremotely.py`
- **Compliance**: ✅ Production-ready (no API key required)

### 9. Dice
- **Status**: ✅ Approved
- **Type**: Tech job board
- **Rate Limit**: 100 requests/minute
- **Coverage**: Tech jobs, engineering positions
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/dice.py`
- **Compliance**: ⚠️ API key needed

### 10. Monster
- **Status**: ✅ Approved
- **Type**: Traditional job board
- **Rate Limit**: 100 requests/minute
- **Coverage**: General jobs, all industries
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/monster.py`
- **Compliance**: ⚠️ API key needed

### 11. ZipRecruiter
- **Status**: ✅ Approved
- **Type**: Job matching platform
- **Rate Limit**: 100 requests/minute
- **Coverage**: Job matching, all industries
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/ziprecruiter.py`
- **Compliance**: ⚠️ API key needed

### 12. CareerBuilder
- **Status**: ✅ Approved
- **Type**: General job board
- **Rate Limit**: 100 requests/minute
- **Coverage**: General jobs, all industries
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/careerbuilder.py`
- **Compliance**: ⚠️ API key needed

### 13. Hacker News
- **Status**: ✅ Approved
- **Type**: Community forum
- **Rate Limit**: 60 requests/minute
- **Coverage**: "Who is hiring" threads, tech jobs
- **API Key Required**: No
- **Implementation**: `api/job_sources/hackernews.py`
- **Compliance**: ✅ Production-ready (no API key required)

## Compliance Status

### Production-Ready Sources
- **Greenhouse**: ✅ API key available
- **SerpApi**: ✅ API key available  
- **Reddit**: ✅ No API key required
- **RemoteOK**: ✅ No API key required
- **WeWorkRemotely**: ✅ No API key required
- **Hacker News**: ✅ No API key required

### Stubbed Sources (Require API Keys)
- **Indeed**: ⚠️ API key needed
- **LinkedIn**: ⚠️ API key needed
- **Glassdoor**: ⚠️ API key needed
- **Dice**: ⚠️ API key needed
- **Monster**: ⚠️ API key needed
- **ZipRecruiter**: ⚠️ API key needed
- **CareerBuilder**: ⚠️ API key needed

### Licensing Requirements
- **Greenhouse**: Standard API terms
- **SerpApi**: Standard API terms
- **Reddit**: Public API (no special licensing)
- **Hacker News**: Public API (no special licensing)
- **Indeed**: Requires API agreement
- **LinkedIn**: Requires API partnership
- **Glassdoor**: Requires API agreement
- **AngelList**: Requires API agreement

## Pending Review

### 4. Hacker News
- **Status**: ⏳ Pending Review
- **Type**: Forum API
- **Rate Limit**: TBD
- **Coverage**: "Who is hiring" threads
- **API Key Required**: No
- **Implementation**: `api/job_sources/hackernews.py` (planned)

### 5. AngelList
- **Status**: ⏳ Pending Review
- **Type**: Job board API
- **Rate Limit**: TBD
- **Coverage**: Startup jobs
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/angelist.py` (planned)

## Rejected Sources

### 6. Indeed (Direct)
- **Status**: ❌ Rejected
- **Reason**: Rate limiting and ToS restrictions
- **Alternative**: Use SerpApi for Indeed data

### 7. LinkedIn (Direct)
- **Status**: ❌ Rejected
- **Reason**: API restrictions and ToS
- **Alternative**: Use SerpApi for LinkedIn data

## Implementation Status

- ✅ **Base Interface**: `api/job_sources/base.py`
- ✅ **Greenhouse**: Implemented with mock data
- ✅ **SerpApi**: Implemented with mock data  
- ✅ **Reddit**: Implemented with mock data
- ⏳ **Hacker News**: Planned
- ⏳ **AngelList**: Planned

## Usage Guidelines

### Rate Limiting
- Each source has its own rate limit
- Global rate limiting across all sources
- Exponential backoff on rate limit hits

### Data Quality
- Standardized job posting format
- Required fields: id, title, company, location, description, url
- Optional fields: salary_range, job_type, remote, skills, experience_level

### Error Handling
- Graceful degradation on API failures
- Fallback to alternative sources
- Logging of errors for monitoring

## RAG-Powered Dynamic Source Discovery

### **Intelligent Source Selection**
- **RAG Analysis**: Uses RAG to analyze job queries and select optimal sources
- **Context-Aware**: Considers job type, location, and industry to choose best sources
- **Dynamic Integration**: Automatically discovers and integrates new sources
- **Performance Optimization**: Selects sources based on historical performance

### **Source Discovery Process**
1. **Query Analysis**: RAG analyzes user query for job requirements
2. **Source Matching**: Matches query characteristics to optimal sources
3. **Confidence Scoring**: Assigns confidence scores to source recommendations
4. **Dynamic Integration**: Integrates new sources based on confidence thresholds
5. **Performance Tracking**: Monitors source performance and adjusts selections

### **API Endpoints**
- **`/sources/discover`**: Discover optimal sources for a query
- **`/sources/analytics`**: Get analytics on source discovery and performance
- **`/jobs/search/rag`**: RAG-powered job search with dynamic source selection

### **Benefits**
- **Intelligent Selection**: Automatically chooses best sources for each query
- **Self-Expanding**: System learns and adds new sources over time
- **Performance Optimized**: Uses historical data to improve source selection
- **Context-Aware**: Adapts to different job types and locations

## Future Enhancements

1. **Machine Learning**: Job matching based on user profile
2. **Real-time Updates**: WebSocket connections for live job feeds
3. **Geographic Filtering**: Location-based job filtering
4. **Skill Matching**: AI-powered skill requirement analysis
5. **Salary Analysis**: Market rate analysis and recommendations
6. **RAG Enhancement**: Improved source discovery and integration
7. **Performance Learning**: Machine learning for source optimization

## Cost Controls and Resource Management

### **Cost Limits**
- **Daily Limit**: $10.00 per day
- **Monthly Limit**: $100.00 per month
- **Per-Request Limit**: $0.01 per request
- **Emergency Stop**: $50.00 (automatic shutdown)

### **Resource Limits**
- **Per Minute**: 60 requests
- **Per Hour**: 1,000 requests
- **Per Day**: 10,000 requests
- **Embeddings**: 100 per day
- **Job Searches**: 500 per day

### **Cost Control Features**
- **Automatic Limits**: Prevents runaway costs
- **Usage Tracking**: Real-time cost monitoring
- **Emergency Stop**: Automatic shutdown at $50
- **Resource Throttling**: Prevents system overload
- **Cache Optimization**: Reduces API calls and costs

### **API Endpoints**
- **`/cost/analytics`**: Get cost and usage analytics
- **`/cost/limits`**: Get current limits and usage
- **`/health/cost`**: Cost control health status

## Monitoring

- **Health Checks**: Each source provides health status
- **Rate Limit Monitoring**: Track usage across all sources
- **Cost Monitoring**: Real-time cost tracking and alerts
- **Resource Monitoring**: System resource usage tracking
- **Error Tracking**: Log and monitor API failures
- **Performance Metrics**: Response times and success rates

---

**Last Updated**: 2025-10-03
**Version**: 1.0
**Status**: Active
