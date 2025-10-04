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

### 2. SerpApi
- **Status**: ✅ Approved  
- **Type**: Search API aggregator
- **Rate Limit**: 100 requests/minute
- **Coverage**: Google Jobs, LinkedIn, Indeed, etc.
- **API Key Required**: Yes
- **Implementation**: `api/job_sources/serpapi.py`

### 3. Reddit
- **Status**: ✅ Approved
- **Type**: Forum scraping
- **Rate Limit**: 60 requests/minute
- **Coverage**: r/forhire, r/remotejs, r/jobs
- **API Key Required**: No
- **Implementation**: `api/job_sources/reddit.py`

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

## Future Enhancements

1. **Machine Learning**: Job matching based on user profile
2. **Real-time Updates**: WebSocket connections for live job feeds
3. **Geographic Filtering**: Location-based job filtering
4. **Skill Matching**: AI-powered skill requirement analysis
5. **Salary Analysis**: Market rate analysis and recommendations

## Monitoring

- **Health Checks**: Each source provides health status
- **Rate Limit Monitoring**: Track usage across all sources
- **Error Tracking**: Log and monitor API failures
- **Performance Metrics**: Response times and success rates

---

**Last Updated**: 2025-10-03
**Version**: 1.0
**Status**: Active
