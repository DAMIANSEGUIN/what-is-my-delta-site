# N8N Job Sources List - From Google Sheets Integration

Based on your previous N8N build that couldn't work with Google Sheets, here are the job sources that were likely included:

## **Primary Job Boards**
1. **Indeed** - Largest job board globally
2. **LinkedIn** - Professional network jobs
3. **Glassdoor** - Company reviews + jobs
4. **Monster** - Traditional job board
5. **ZipRecruiter** - Job matching platform
6. **CareerBuilder** - General job board
7. **Dice** - Tech-focused jobs
8. **SimplyHired** - Job aggregator

## **Remote Job Boards**
9. **RemoteOK** - Remote tech jobs
10. **WeWorkRemotely** - Remote jobs
11. **FlexJobs** - Remote/flexible jobs
12. **Working Nomads** - Remote jobs
13. **Remote.co** - Remote job board

## **Tech-Specific Boards**
14. **Stack Overflow Jobs** - Developer jobs
15. **AngelList** - Startup jobs (as you noted, waste of time)
16. **Hacker News** - "Who is hiring" threads
17. **GitHub Jobs** - Developer positions
18. **Crunchboard** - Startup jobs

## **Freelance/Contract Platforms**
19. **Upwork** - Freelance marketplace
20. **Freelancer** - Freelance platform
21. **Toptal** - Elite freelancers
22. **Fiverr** - Gig economy
23. **99designs** - Design jobs

## **Industry-Specific**
24. **Snagajob** - Hourly jobs
25. **Jora** - International jobs
26. **JobisJob** - Job aggregator
27. **Adzuna** - Job search engine
28. **Neuvoo** - Job aggregator

## **Government/Non-Profit**
29. **USAJobs** - Federal jobs
30. **Idealist** - Non-profit jobs
31. **Work for Good** - Social impact jobs

## **Regional/International**
32. **Reed** - UK jobs
33. **Seek** - Australia/NZ jobs
34. **JobStreet** - Southeast Asia jobs
35. **InfoJobs** - Spain jobs
36. **Xing** - German professional network

## **Specialized Platforms**
37. **Behance** - Creative jobs
38. **Dribbble** - Design jobs
39. **AngelList** - Startup jobs (as noted, problematic)
40. **Crunchbase** - Startup ecosystem

## **API-Accessible Sources**
41. **SerpApi** - Google Jobs scraping
42. **RapidAPI** - Job APIs
43. **ProgrammableWeb** - Job APIs
44. **Reddit** - r/forhire, r/remotejs
45. **Discord** - Job channels

## **Implementation Notes**

### **High Priority (Already Implemented)**
- ✅ **Greenhouse** - ATS integration
- ✅ **SerpApi** - Google Jobs scraping
- ✅ **Reddit** - Community jobs
- ✅ **Indeed** - Largest job board
- ✅ **LinkedIn** - Professional network
- ✅ **Glassdoor** - Company reviews
- ✅ **RemoteOK** - Remote jobs
- ✅ **WeWorkRemotely** - Remote jobs
- ✅ **Dice** - Tech jobs
- ✅ **Hacker News** - Tech community

### **Medium Priority (Should Add)**
- **Monster** - Traditional job board
- **ZipRecruiter** - Job matching
- **CareerBuilder** - General jobs
- **SimplyHired** - Job aggregator
- **Upwork** - Freelance marketplace
- **Stack Overflow** - Developer jobs

### **Low Priority (API Issues)**
- **AngelList** - Startup jobs (as you noted, problematic)
- **FlexJobs** - Requires subscription
- **Toptal** - Elite platform
- **GitHub Jobs** - Limited API

## **Google Sheets Integration Issues**

The common problems with Google Sheets integration for job sources:

1. **API Rate Limits** - Most job boards have strict rate limits
2. **Authentication** - Many require OAuth or API keys
3. **Data Format** - Inconsistent job data formats
4. **Terms of Service** - Many prohibit scraping
5. **Captcha Protection** - Anti-bot measures
6. **IP Blocking** - Rate limit violations
7. **Data Quality** - Inconsistent job descriptions
8. **Duplicate Detection** - Same jobs across platforms

## **Recommended Implementation Strategy**

1. **Start with API-based sources** (Greenhouse, SerpApi)
2. **Add community sources** (Reddit, Hacker News)
3. **Implement rate limiting** and cost controls
4. **Use RAG for deduplication** and quality filtering
5. **Focus on high-quality sources** first
6. **Avoid problematic sources** like AngelList

## **Next Steps**

Would you like me to:
1. **Add the missing high-priority sources** (Monster, ZipRecruiter, CareerBuilder)?
2. **Create a Google Sheets integration** for job source management?
3. **Implement the N8N workflow** you had in mind?
4. **Focus on the sources that actually work** and skip the problematic ones?

Let me know which direction you'd like to go!
