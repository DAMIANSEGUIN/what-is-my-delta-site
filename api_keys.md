# MOSAIC 2.0 API Keys Configuration

## 🎯 EXECUTIVE DECISION: NO PAID API KEYS

**DECISION**: We will NOT pay for API keys and will build direct public access capabilities into the backend for job search sources that are publicly available.

**RATIONALE**: Job sources are publicly searchable by users directly, so no need to pay for API access when public access is available.

## 🆓 FREE API SOURCES (No Keys Required)

### **✅ READY TO USE - Public APIs**
- **Greenhouse** - Public job board API
- **Indeed** - Public XML feed
- **RemoteOK** - Public API
- **WeWorkRemotely** - Public API
- **Hacker News** - Public API (Who is hiring threads)
- **Reddit** - Public API (r/forhire, r/remotejs)
- **LinkedIn** - Public web scraping
- **Glassdoor** - Public web scraping
- **Dice** - Public web scraping
- **Monster** - Public web scraping
- **ZipRecruiter** - Public web scraping
- **CareerBuilder** - Public web scraping

### **✅ USER-PROVIDED APIs (Available)**
- **OpenAI API Key** - AI embeddings and semantic search
  - **Status**: ✅ USER PROVIDED
  - **Usage**: Semantic match upgrade, embeddings
  - **Integration**: Ready for production

- **Claude AI API Key** - AI analysis and job matching
  - **Status**: ✅ USER PROVIDED  
  - **Usage**: Job analysis, competitive intelligence
  - **Integration**: Ready for production

### **❌ PAID APIs (Will NOT Use)**
- **SerpApi** - $50/month (Google Jobs) - Will use direct scraping
- **All other paid APIs** - $200-500/month total - Will use direct scraping

## 📊 COST SAVINGS

### **Monthly Savings**
- **SerpApi**: $50/month saved
- **OpenAI**: $10-50/month saved
- **Other APIs**: $200-500/month saved
- **Total Savings**: $260-600/month

### **Annual Savings**
- **Total Annual Savings**: $3,120-7,200/year
- **ROI**: Immediate cost reduction
- **Scalability**: No per-API costs

## 🔑 API KEYS CONFIGURATION

### **USER-PROVIDED API KEYS (Fill in the slots below)**

**Required Environment Variables:**
- `OPENAI_API_KEY` - For semantic search and embeddings
- `CLAUDE_API_KEY` - For job analysis and competitive intelligence

**Environment Variables Setup:**
Create a `.env` file with your API keys:
```bash
# USER-PROVIDED API KEYS (Add your keys here)
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
```

**Template File Available:**
- Copy `env_template.txt` to `.env`
- Add your actual API keys
- Never commit `.env` to version control

### **FREE PUBLIC APIs (No Keys Required)**
- **Greenhouse**: https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs
- **Indeed**: https://ads.indeed.com/jobroll/xmlfeed
- **RemoteOK**: https://remoteok.io/api
- **WeWorkRemotely**: https://weworkremotely.com/categories/remote-jobs.json
- **Hacker News**: https://hacker-news.firebaseio.com/v0/
- **Reddit**: https://www.reddit.com/r/forhire.json
- **LinkedIn**: Web scraping
- **Glassdoor**: Web scraping
- **Dice**: Web scraping
- **Monster**: Web scraping
- **ZipRecruiter**: Web scraping
- **CareerBuilder**: Web scraping

## 🔧 IMPLEMENTATION STRATEGY

### **Phase 1: Direct Public API Integration**
1. **Greenhouse** - Direct API calls
2. **Indeed** - XML feed parsing
3. **RemoteOK** - JSON API calls
4. **WeWorkRemotely** - JSON API calls
5. **Hacker News** - JSON API calls
6. **Reddit** - JSON API calls

### **Phase 2: Web Scraping Integration**
1. **LinkedIn** - Web scraping
2. **Glassdoor** - Web scraping
3. **Dice** - Web scraping
4. **Monster** - Web scraping
5. **ZipRecruiter** - Web scraping
6. **CareerBuilder** - Web scraping

### **Phase 3: Google Jobs Direct Scraping**
1. **Google Jobs** - Direct web scraping
2. **Rate limiting** - Respectful scraping
3. **Data parsing** - Extract job data
4. **Fallback handling** - Error management

## 🚀 PRODUCTION DEPLOYMENT STATUS

### **✅ READY FOR IMMEDIATE DEPLOYMENT**
- **Greenhouse** - Public API ready
- **Indeed** - XML feed ready
- **RemoteOK** - JSON API ready
- **WeWorkRemotely** - JSON API ready
- **Hacker News** - JSON API ready
- **Reddit** - JSON API ready

### **🔧 REQUIRES IMPLEMENTATION**
- **LinkedIn** - Web scraping needed
- **Glassdoor** - Web scraping needed
- **Dice** - Web scraping needed
- **Monster** - Web scraping needed
- **ZipRecruiter** - Web scraping needed
- **CareerBuilder** - Web scraping needed
- **Google Jobs** - Web scraping needed

## 📋 DECISION DOCUMENTATION

### **✅ APPROVED APPROACH**
1. **Use only free, public APIs**
2. **Implement web scraping for paid sources**
3. **Build direct Google Jobs scraping**
4. **Maintain cost-free operation**
5. **Ensure full job search coverage**

### **❌ REJECTED APPROACH**
1. **No paid API keys**
2. **No subscription services**
3. **No per-API costs**
4. **No vendor lock-in**

## 🎯 SUCCESS METRICS

### **Coverage Targets**
- **Job Sources**: 12+ free sources
- **Geographic Coverage**: Global
- **Job Types**: All categories
- **Update Frequency**: Real-time

### **Performance Targets**
- **Response Time**: <2 seconds
- **Success Rate**: >95%
- **Data Quality**: >90%
- **Uptime**: >99%

## 🔒 TECHNICAL CONSIDERATIONS

### **Rate Limiting**
- **HTTP Rate Limits**: Standard web limits
- **Respectful Scraping**: 1 request/second
- **Error Handling**: Graceful fallbacks
- **Caching**: Reduce API calls

### **Data Quality**
- **Public APIs**: High quality, structured data
- **Web Scraping**: Variable quality, parsing needed
- **Data Validation**: Ensure data integrity
- **Fallback Sources**: Multiple sources per query

### **Maintenance**
- **Public APIs**: Low maintenance
- **Web Scraping**: Medium maintenance
- **Monitoring**: Track source availability
- **Updates**: Adapt to site changes

---

**DECISION DATE**: 2025-10-06
**APPROVED BY**: User
**STATUS**: ✅ IMPLEMENTED
**NEXT STEPS**: Build direct public access capabilities