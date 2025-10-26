# Netlify Agent Task - Fix Railway Booking Routes
**Date:** 2025-10-26
**Priority:** HIGH - Production Issue
**Task Type:** Diagnose and Fix

---

## Problem

Railway deployment successful but booking routes NOT loading:
- ❌ `/booking/promo/WIMD25` returns 404 (should be 401 auth required)
- ❌ Booking routes missing from `/openapi.json` spec
- ✅ API health works: `/health`
- ✅ Other routes work: `/wimd`, `/ob`, `/resume`

**Railway Service:** https://what-is-my-delta-site-production.up.railway.app

---

## Files Deployed

```
api/booking.py - Booking endpoints
api/google_calendar_service.py - Google Calendar integration
api/paypal_service.py - PayPal payments
api/run_migrations.py - Auto-migrations
data/migrations/001_add_booking_tables.sql
data/migrations/002_seed_booking_data.sql
```

Router registered in `api/index.py` lines 106-113:
```python
try:
    from api.booking import router as booking_router
    app.include_router(booking_router)
    logger.info("✅ Booking routes registered successfully")
except Exception as e:
    logger.error(f"❌ Failed to register booking routes: {e}")
```

---

## Environment Variables Set

- `GOOGLE_SERVICE_ACCOUNT_KEY` ✅
- `COACH_GOOGLE_CALENDAR_ID='primary'` ✅
- `COACH_EMAIL` ✅
- `PAYPAL_CLIENT_ID` ✅
- `PAYPAL_CLIENT_SECRET` ✅
- `PAYPAL_MODE='live'` ✅
- `DATABASE_URL` ✅

---

## Diagnosis Steps

1. Check Railway logs for import errors
2. Verify dependencies in requirements.txt
3. Test if migrations created booking tables
4. Check for circular imports
5. Verify router registration executed

---

## Expected Fix

After fix:
- `/booking/promo/WIMD25` returns 401, NOT 404
- Booking routes in `/openapi.json`
- Migrations log shows tables created
- No import errors in Railway logs

---

## Repository

**Path:** `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project`

**Latest commit:** `fa95c45` - Added error logging for booking router

**Last deploy:** 2025-10-26T14:37:25Z

---

## Your Task

1. Diagnose root cause of router not loading
2. Fix the issue
3. Verify routes now work
4. Report back what was wrong and how you fixed it

**Ready for Netlify Agent Runner to diagnose and fix.**
