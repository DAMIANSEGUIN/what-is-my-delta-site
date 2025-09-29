# WIMD Railway Deploy Project - Operations Manual

**Project**: WIMD (What Is My Delta) - Mosaic Platform
**Infrastructure**: Railway (Backend) + Netlify (Frontend)
**Created**: 2025-09-29
**Version**: 1.0

---

## **TABLE OF CONTENTS**

1. [System Architecture](#system-architecture)
2. [Deployment Procedures](#deployment-procedures)
3. [Troubleshooting](#troubleshooting)
4. [Environment Management](#environment-management)
5. [Cache Management](#cache-management)
6. [Monitoring & Health Checks](#monitoring--health-checks)
7. [Emergency Procedures](#emergency-procedures)
8. [Maintenance Tasks](#maintenance-tasks)

---

## **SYSTEM ARCHITECTURE**

### **Infrastructure Overview**
- **Backend API**: Railway service (`what-is-my-delta-site-production`)
- **Frontend UI**: Netlify deployment (`resonant-crostata-90b706`)
- **Domain**: `https://whatismydelta.com` (apex + www)
- **Repository**: `https://github.com/DAMIANSEGUIN/what-is-my-delta-site`

### **Key Components**
- **FastAPI Application**: 449-line implementation with complete endpoints
- **Database**: SQLite with auto-cleanup (30-day session expiry)
- **API Endpoints**: `/health`, `/config`, `/prompts/active`, `/wimd/*`, `/ob/*`, `/resume/*`
- **Environment Variables**: API keys, domain configuration

---

## **DEPLOYMENT PROCEDURES**

### **Standard Deployment**
```bash
# 1. Commit changes
git add .
git commit -m "Deployment description"

# 2. Push to trigger auto-deploy
git push origin main
```

### **Force Deployment (Cache Issues)**
```bash
# 1. Make trivial change to force rebuild
echo "# Cache bust: $(date +%s)" >> README.md
git add README.md
git commit -m "Cache bust: $(date +%s)"
git push origin main
```

---

## **TROUBLESHOOTING**

### **Common Issues**

#### **Issue**: API Endpoints Return 404
**Symptoms**: `/config`, `/prompts/active` return `{"detail":"Not Found"}`
**Cause**: Railway cache serving old code
**Solution**: [Railway Cache Clearing](#railway-cache-clearing)

#### **Issue**: Railway Shows "Hello World" Instead of Full API
**Symptoms**: Root endpoint returns basic message instead of Mosaic API
**Cause**: Wrong Procfile or incomplete code deployment
**Solution**:
1. Verify Procfile points to `api.index:app`
2. Check repository has complete 449-line `api/index.py`
3. Clear Railway cache

#### **Issue**: Environment Variables Not Loading
**Symptoms**: API key errors, startup failures
**Solution**:
1. Verify variables in Railway dashboard → Variables tab
2. Ensure variables are marked "Available during deploy"
3. Check local `.env` file matches production requirements

---

## **ENVIRONMENT MANAGEMENT**

### **Required Environment Variables**
```bash
# API Keys (Production - Railway Variables)
OPENAI_API_KEY=sk-proj-...
CLAUDE_API_KEY=sk-ant-api03-...

# Domain Configuration
PUBLIC_SITE_ORIGIN=https://whatismydelta.com
PUBLIC_API_BASE=https://what-is-my-delta-site-production.up.railway.app

# Application Configuration
APP_SCHEMA_VERSION=v1
```

### **Critical Dependencies**
```bash
# requirements.txt MUST include:
python-multipart  # CRITICAL: FastAPI file upload support
fastapi           # Web framework
uvicorn           # ASGI server
pydantic          # Data validation
pydantic-settings # Settings management
```

### **RESOLVED ISSUE (2025-09-29): Missing python-multipart**
**Problem**: Railway showed successful build but served "Hello World" instead of complete API
**Root Cause**: Missing `python-multipart` dependency caused FastAPI startup failure
**Solution**: Added `python-multipart` to requirements.txt
**Result**: Railway now serves complete 449-line FastAPI implementation

### **API Key Rotation Procedure**
1. **Generate new keys** in OpenAI/Anthropic dashboards
2. **Update Railway variables** in Variables tab
3. **Update local `.env` file**
4. **Revoke old keys** in provider dashboards
5. **Test deployment** with new keys

---

## **CACHE MANAGEMENT**

### **Railway Cache Clearing**
**When to use**: API showing old code despite successful deployments

#### **Method 1: Disable Build Cache (Recommended)**
1. Go to Railway Dashboard → Service → Variables
2. Add new variable:
   - **Name**: `RAILWAY_DISABLE_BUILD_CACHE`
   - **Value**: `true`
3. Force redeploy using Method 2

#### **Method 2: Force Fresh Deployment**
**Option A - Command Palette:**
1. Press `CMD + K` in Railway dashboard
2. Type "Deploy Latest Commit"
3. Execute command

**Option B - Manual Redeploy:**
1. Go to Railway → Deployments tab
2. Find latest deployment
3. Click three dots (...) → "Redeploy"

#### **Method 3: Cache-Busting Commit (Script)**
```bash
# Execute cache-busting script
./clear_railway_cache.sh
```

### **CDN Cache Issues**
**Symptoms**: Domain shows old content despite Railway updates
**Solutions**:
1. Hard refresh browser (Ctrl+Shift+R)
2. Test in incognito mode
3. Check Railway CDN status
4. Contact Railway support for manual cache purge

---

## **MONITORING & HEALTH CHECKS**

### **Health Check Commands**
```bash
# Backend Health
curl https://what-is-my-delta-site-production.up.railway.app/health

# Configuration Check
curl https://what-is-my-delta-site-production.up.railway.app/config

# Prompts Status
curl https://what-is-my-delta-site-production.up.railway.app/prompts/active

# Domain Health (after Netlify rewrite)
curl https://whatismydelta.com/health
```

### **Expected Responses**
```json
// /health
{"ok": true, "timestamp": "2025-09-29T..."}

// /config
{"apiBase": "https://...", "schemaVersion": "v1"}

// /prompts/active
{"active": "..."}
```

### **Verification Script**
```bash
# Run comprehensive deployment verification
./scripts/verify_deploy.sh https://whatismydelta.com
```

---

## **EMERGENCY PROCEDURES**

### **Service Down**
1. **Check Railway status**: Railway dashboard → Service status
2. **View logs**: Railway → Deployments → Click latest → View logs
3. **Test direct Railway URL**: `https://what-is-my-delta-site-production.up.railway.app/health`
4. **Check environment variables**: Ensure all required vars are set
5. **Force redeploy**: Use cache clearing procedures

### **Data Loss/Corruption**
1. **Check SQLite database**: Railway → Run `ls -la data/`
2. **Verify session cleanup**: Ensure auto-cleanup is functioning
3. **Check storage limits**: Railway storage usage
4. **Restore from backup**: If available
5. **Reinitialize database**: Via startup checks

### **Security Breach**
1. **Rotate API keys immediately**: Use API key rotation procedure
2. **Check access logs**: Railway logs for suspicious activity
3. **Review environment variables**: Ensure no secrets exposed
4. **Update documentation**: Record incident and response

---

## **MAINTENANCE TASKS**

### **Weekly**
- [ ] Check Railway storage usage
- [ ] Review deployment logs for errors
- [ ] Test all API endpoints
- [ ] Verify SSL certificates

### **Monthly**
- [ ] Review and rotate API keys
- [ ] Check database cleanup operations
- [ ] Update dependencies in requirements.txt
- [ ] Review and update documentation

### **Quarterly**
- [ ] Full security audit
- [ ] Performance optimization review
- [ ] Backup strategy verification
- [ ] Disaster recovery testing

---

## **SCRIPTS & AUTOMATION**

### **Available Scripts**
```bash
# API Key Management
./update_api_keys_web.sh          # Interactive API key rotation

# Deployment Management
./fix_deployment.sh               # Fix Procfile and deploy
./deploy_complete_api.sh          # Deploy complete API implementation
./force_redeploy.sh               # Force cache-busting deployment

# Cache Management
./clear_railway_cache.sh          # Railway cache clearing guide

# Verification
./scripts/verify_deploy.sh        # Deployment verification
./scripts/predeploy_sanity.sh     # Pre-deployment checks
```

---

## **TROUBLESHOOTING DECISION TREE**

```
Deployment Issue?
├── API 404 Errors?
│   ├── Check Railway cache → Clear cache
│   └── Verify complete code in repository
├── Environment Variable Issues?
│   ├── Check Railway Variables tab
│   └── Verify "Available during deploy" setting
├── Service Won't Start?
│   ├── Check Procfile configuration
│   ├── Review startup logs
│   └── Verify requirements.txt
└── Domain Issues?
    ├── Test Railway direct URL
    ├── Check Netlify configuration
    └── Verify DNS settings
```

---

## **CONTACT & ESCALATION**

### **Support Channels**
- **Railway Support**: Railway dashboard → Help
- **GitHub Issues**: Repository issues tab
- **Documentation**: Railway docs, FastAPI docs

### **Escalation Criteria**
- Service down > 15 minutes
- Data loss or corruption
- Security breach detected
- Cache issues persisting > 1 hour

---

**Last Updated**: 2025-09-29
**Next Review**: 2025-10-29
**Maintained By**: Claude Code (Senior Debugger)