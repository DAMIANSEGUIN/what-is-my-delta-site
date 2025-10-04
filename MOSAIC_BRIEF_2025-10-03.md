# **MOSAIC BRIEF - What is Mosaic and How It Works**
**Date**: 2025-10-03  
**Version**: 2.0  
**Status**: Production Ready

## 🎯 **What is Mosaic?**

Mosaic is an AI-powered career coaching platform that helps professionals navigate career transitions, overcome burnout, and discover their next career move through personalized guidance and real-time job matching.

### **Core Value Proposition**
- **Personalized Career Coaching**: AI-powered guidance tailored to individual career challenges
- **Real-Time Job Matching**: Intelligent job discovery across 13+ job sources
- **Burnout Recovery**: Specialized support for professionals experiencing career fatigue
- **Career Transition Support**: Structured guidance for career pivots and changes

## 🏗️ **How Mosaic Works**

### **User Experience Flow**
1. **Assessment**: Users complete a brief assessment of their current career state
2. **AI Analysis**: Mosaic analyzes responses using RAG-powered intelligence
3. **Personalized Guidance**: Users receive tailored career coaching recommendations
4. **Job Matching**: System suggests relevant job opportunities from multiple sources
5. **Progress Tracking**: Users track their career development journey

### **Key Features**
- **AI Coach**: Personalized career guidance using advanced prompt engineering
- **Job Discovery**: Real-time job matching across 13+ job sources
- **Self-Efficacy Metrics**: Track career confidence and progress
- **Experiment Engine**: Test new career directions safely
- **Resume Optimization**: AI-powered resume customization for specific roles

## 🏛️ **Architecture Overview**

### **Frontend (Netlify)**
- **Technology**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Modern, responsive interface with focus on user experience
- **Features**: Real-time job search, career coaching interface, progress tracking
- **URL**: https://whatismydelta.com

### **Backend (Railway)**
- **Technology**: FastAPI (Python)
- **Database**: SQLite with migration framework
- **Features**: AI coaching, job search, user management, analytics
- **URL**: https://what-is-my-delta-site-production.up.railway.app

### **AI Integration**
- **RAG Engine**: Retrieval-Augmented Generation for intelligent responses
- **Job Sources**: 13+ integrated job boards and APIs
- **Cost Controls**: Comprehensive cost management and rate limiting
- **Feature Flags**: Safe rollout of new functionality

## 📊 **Technical Architecture**

### **Database Schema**
- **Users**: Authentication and profile management
- **Sessions**: User interaction tracking
- **Experiments**: Career testing and learning data
- **Job Postings**: Cached job opportunities
- **Analytics**: Usage tracking and cost management

### **API Endpoints**
- **Core**: `/wimd`, `/health`, `/config`
- **Jobs**: `/jobs/search`, `/jobs/search/rag`
- **RAG**: `/rag/embed`, `/rag/query`, `/rag/retrieve`
- **Analytics**: `/cost/analytics`, `/sources/analytics`
- **Experiments**: `/experiments/*`, `/self-efficacy/*`

### **Job Sources Integration**
- **Production-Ready**: Greenhouse, SerpApi, Reddit, RemoteOK, WeWorkRemotely, Hacker News
- **Stubbed**: Indeed, LinkedIn, Glassdoor, Dice, Monster, ZipRecruiter, CareerBuilder
- **Cost Controls**: Daily/monthly limits, emergency stops, rate limiting

## 🎨 **User Experience Design**

### **Interface Philosophy**
- **Minimalist Design**: Clean, distraction-free interface
- **Progressive Disclosure**: Information revealed as needed
- **Mobile-First**: Responsive design for all devices
- **Accessibility**: WCAG 2.1 AA compliance

### **User Journey**
1. **Landing**: Clear value proposition and call-to-action
2. **Assessment**: Intuitive career state evaluation
3. **Coaching**: Personalized AI guidance and recommendations
4. **Job Search**: Seamless job discovery and application
5. **Tracking**: Progress monitoring and goal achievement

## 📈 **Marketing Plan**

### **Target Audience**
- **Primary**: Mid-career professionals (30-50) experiencing career transitions
- **Secondary**: Recent graduates and career changers
- **Tertiary**: Burnout recovery and career optimization seekers

### **Value Propositions**
- **"Find Your Next Career Move"**: Clear path forward for career transitions
- **"Overcome Career Burnout"**: Specialized support for professional fatigue
- **"AI-Powered Career Guidance"**: Cutting-edge technology for career development
- **"Real-Time Job Matching"**: Immediate access to relevant opportunities

### **Marketing Channels**
- **Content Marketing**: Career transition guides, burnout recovery resources
- **SEO**: Career coaching, job search, burnout recovery keywords
- **Social Media**: LinkedIn, Twitter, professional communities
- **Partnerships**: Career coaches, HR professionals, recruitment agencies
- **Referral Program**: User-generated content and testimonials

### **Content Strategy**
- **Blog Posts**: Career transition stories, burnout recovery guides
- **Case Studies**: Success stories and user testimonials
- **Webinars**: Career coaching sessions and job search workshops
- **Social Proof**: User reviews and success metrics

### **Growth Metrics**
- **User Acquisition**: Monthly active users, sign-up conversion
- **Engagement**: Session duration, feature usage, return visits
- **Success**: Career transitions, job placements, user satisfaction
- **Revenue**: Premium features, coaching services, job placement fees

## 🚀 **Deployment Status**

### **Current State**
- ✅ **Frontend**: Deployed on Netlify (https://whatismydelta.com)
- ✅ **Backend**: Deployed on Railway (https://what-is-my-delta-site-production.up.railway.app)
- ✅ **Database**: SQLite with migration framework
- ✅ **AI Integration**: RAG engine with cost controls
- ✅ **Job Sources**: 13 sources integrated (6 production-ready)

### **Feature Flags**
- **Phase 1**: AI Fallback (disabled)
- **Phase 2**: Experiments (disabled)
- **Phase 3**: Self-Efficacy Metrics (enabled)
- **Phase 4**: RAG Baseline (disabled)
- **Phase 5**: New UI Elements (disabled)
- **Job Sources**: Stubbed sources (disabled)

## 🔧 **Technical Requirements**

### **Environment Variables**
```bash
# AI Services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Job Sources (Production-Ready)
SERPAPI_API_KEY=your_serpapi_key
GREENHOUSE_API_KEY=your_greenhouse_key

# Job Sources (Stubbed - Need API Keys)
INDEED_API_KEY=your_indeed_key
LINKEDIN_API_KEY=your_linkedin_key
GLASSDOOR_API_KEY=your_glassdoor_key
DICE_API_KEY=your_dice_key
MONSTER_API_KEY=your_monster_key
ZIPRECRUITER_API_KEY=your_ziprecruiter_key
CAREERBUILDER_API_KEY=your_careerbuilder_key
```

### **Cost Controls**
- **Daily Limit**: $10.00 per day
- **Monthly Limit**: $100.00 per month
- **Emergency Stop**: $50.00 (automatic shutdown)
- **Resource Limits**: 60/min, 1000/hour, 10000/day

## 📋 **Next Steps for Claude Code**

### **Immediate Actions**
1. **Deploy Database Migrations**: Run migrations 004, 005, 006
2. **Enable Feature Flags**: Activate RAG_BASELINE and job sources
3. **Configure API Keys**: Set up production-ready job sources
4. **Test Cost Controls**: Verify cost management and rate limiting
5. **Monitor Performance**: Track usage and optimize as needed

### **API Key Requirements**
- **Human Reminder**: Get API keys for stubbed job sources (Indeed, LinkedIn, Glassdoor, Dice, Monster, ZipRecruiter, CareerBuilder)
- **Priority Order**: Indeed → LinkedIn → Glassdoor → Dice → Monster → ZipRecruiter → CareerBuilder
- **Cost Management**: Monitor API usage and costs closely

### **Success Metrics**
- **User Engagement**: Session duration, feature usage
- **Job Matching**: Successful job placements
- **Cost Control**: Stay within daily/monthly limits
- **Performance**: Response times, error rates
- **User Satisfaction**: Feedback and testimonials

---

**Status**: Ready for Claude Code deployment with comprehensive cost safeguards and production-ready job sources integration.
