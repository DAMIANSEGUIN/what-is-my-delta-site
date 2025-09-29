# DNS Configuration for whatismydelta.com

## Current Setup
- **Domain:** whatismydelta.com
- **Current Provider:** Netlify
- **Current Target:** resonant-crostata-90b706.netlify.app
- **New Target:** Railway deployment

## Railway Domain Setup (CORRECT METHOD)

### Step 1: Add Custom Domain in Railway
1. Go to Railway dashboard → **"Settings"** → **"Domains"**
2. Add **www.whatismydelta.com** 
3. Add **whatismydelta.com** (bare domain)
4. Railway will show a **verification TXT record**

### Step 2: Create Verification Record in Netlify
1. Log into Netlify DNS panel
2. Add the **TXT record** Railway shows (name/value exactly)
3. This lets Railway issue the SSL certificate

### Step 3: Point the Apex Domain
**Option A (Recommended):**
- Create **ANAME/ALIAS** record for `whatismydelta.com` 
- Point to: `what-is-my-delta-site-production.up.railway.app`

**Option B (Alternative):**
- Keep apex on Netlify
- Add redirect rule: `whatismydelta.com` → `www.whatismydelta.com`

### Step 4: Wait for Railway Verification
- Railway will show domain as **"Ready"** (green)
- If stuck in "Pending", check TXT record spelling

### Step 5: Verify Propagation
```bash
dig +short www.whatismydelta.com
curl https://www.whatismydelta.com/health
```

## Test Commands
```bash
# Test domain
curl https://whatismydelta.com/health

# Test Railway URL (backup)
curl https://what-is-my-delta-site-production.up.railway.app/health
```

## Railway Configuration
- **Service:** what-is-my-delta-site
- **Project:** wimd-career-coaching
- **Environment:** production
- **Custom Domain:** whatismydelta.com
- **Railway Target:** igv415qp.up.railway.app

## Last Updated
2025-09-25 - DNS configuration for Railway deployment
