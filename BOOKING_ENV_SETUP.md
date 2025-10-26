# Booking System - Environment Variables Setup
**Status:** Ready for deployment after credentials added
**Date:** 2025-10-25

---

## Required Environment Variables

Add these to **Railway Dashboard** → Your Project → **Variables** tab:

### Google Calendar API (Required)

```bash
# Service Account Credentials (entire JSON file content)
GOOGLE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"jobleadsmastertracker",...}'

# Calendar ID (use 'primary' for your main calendar, or specific calendar ID)
COACH_GOOGLE_CALENDAR_ID='primary'

# Coach Contact Information (appears in calendar invites)
COACH_EMAIL='your@email.com'
COACH_PHONE_NUMBER='+1234567890'
```

**How to get `GOOGLE_SERVICE_ACCOUNT_KEY`:**
1. Copy contents of your `client_secrets.json` file
2. Paste the entire JSON object as the value (keep single quotes around it)
3. **CRITICAL:** Make sure you've shared your Google Calendar with: `jobleadsmastertracker@jobleadsmastertracker.iam.gserviceaccount.com`

---

### PayPal API (Required)

```bash
# PayPal Credentials
PAYPAL_CLIENT_ID='your_client_id_here'
PAYPAL_CLIENT_SECRET='your_client_secret_here'

# Mode: 'sandbox' for testing, 'live' for production
PAYPAL_MODE='live'

# Return URLs (update with your domain)
PAYPAL_RETURN_URL='https://whatismydelta.com/booking/success'
PAYPAL_CANCEL_URL='https://whatismydelta.com/booking/cancel'
```

**How to get PayPal credentials:**
1. Go to https://developer.paypal.com/dashboard
2. Click "Apps & Credentials"
3. Select "Live" (for production) or "Sandbox" (for testing)
4. Copy **Client ID** and **Secret**

---

### Email Notifications (Optional - for later)

```bash
# SendGrid (recommended) or AWS SES
SENDGRID_API_KEY='SG.xxxx'
SENDGRID_FROM_EMAIL='noreply@whatismydelta.com'
```

---

### SMS Notifications (Optional - wire but disable for 2 weeks)

```bash
# Twilio
TWILIO_ACCOUNT_SID='ACxxxx'
TWILIO_AUTH_TOKEN='xxxx'
TWILIO_PHONE_NUMBER='+1234567890'
TWILIO_SMS_ENABLED='false'  # Set to 'true' when ready to enable
```

---

## Already Set (Verify These Exist)

These should already be in your Railway environment:

```bash
DATABASE_URL=postgresql://...railway.internal...
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...
```

---

## How to Add Variables to Railway

### Method 1: Railway Dashboard (Recommended)

1. Go to https://railway.app
2. Select your project: `what-is-my-delta-site`
3. Click "Variables" tab
4. Click "New Variable"
5. Enter variable name and value
6. Click "Add"
7. Repeat for all variables
8. Railway will automatically redeploy with new variables

### Method 2: Railway CLI (Faster for Multiple Variables)

```bash
# Set one variable
railway variables set PAYPAL_CLIENT_ID='your_value'

# Set from file
railway variables set GOOGLE_SERVICE_ACCOUNT_KEY="$(cat client_secrets.json)"
```

---

## Verification Checklist

After adding all variables, verify:

```bash
# Check all variables are set (from Railway dashboard or CLI)
railway variables

# Should see:
✅ GOOGLE_SERVICE_ACCOUNT_KEY
✅ COACH_GOOGLE_CALENDAR_ID
✅ COACH_EMAIL
✅ COACH_PHONE_NUMBER
✅ PAYPAL_CLIENT_ID
✅ PAYPAL_CLIENT_SECRET
✅ PAYPAL_MODE
✅ PAYPAL_RETURN_URL
✅ PAYPAL_CANCEL_URL
```

---

## Testing the Integration

### Test Google Calendar Service (Mock Mode)

Before adding credentials, the service runs in **mock mode**:
- Returns fake event IDs like `mock_event_1234567890`
- Logs warnings: "Calendar service not initialized"
- **Does NOT create real calendar events**

After adding credentials:
- Creates real Google Calendar events
- Sends email invites to users
- Logs: "Google Calendar service initialized successfully"

### Test PayPal Service (Mock Mode)

Before adding credentials:
- Returns fake order IDs like `ORDER_MOCK_single_session_USD`
- Logs warnings: "PayPal not initialized"
- **Does NOT charge real money**

After adding credentials:
- Creates real PayPal orders
- Redirects users to PayPal for payment
- Captures real payments

### Health Check Endpoint

After deployment, check:

```bash
curl https://what-is-my-delta-site-production.up.railway.app/health

# Should show:
{
  "ok": true,
  "services": {
    "google_calendar": "initialized",  # or "mock_mode"
    "paypal": "initialized"             # or "mock_mode"
  }
}
```

---

## Security Notes

### ✅ SAFE to commit to git:
- `BOOKING_ENV_SETUP.md` (this file)
- `.env.example` (template with fake values)

### ❌ NEVER commit to git:
- `.env` (local development file with real credentials)
- `client_secrets.json` (Google service account key)
- Any file with real API keys

### Railway Security:
- Environment variables are encrypted at rest
- Only visible to project collaborators
- Not exposed in logs or error messages
- Rotated variables take effect on next deployment

---

## Next Steps After Adding Variables

1. **Verify variables are set** in Railway dashboard
2. **Redeploy** (Railway auto-deploys when you add variables)
3. **Check deployment logs** for initialization messages:
   ```
   [INFO] Google Calendar service initialized successfully
   [INFO] PayPal payment service initialized successfully (live mode)
   ```
4. **Test health endpoint** (see above)
5. **Share Google Calendar** with service account email
6. **Test booking flow** (see testing plan in BOOKING_IMPLEMENTATION_PLAN.md)

---

## Troubleshooting

### Google Calendar errors:

**Error:** "Calendar service not initialized"
- **Fix:** Add `GOOGLE_SERVICE_ACCOUNT_KEY` to Railway variables

**Error:** "403 Forbidden" when creating events
- **Fix:** Share your Google Calendar with `jobleadsmastertracker@jobleadsmastertracker.iam.gserviceaccount.com`
- Permission: "Make changes to events"

**Error:** "Invalid JSON in GOOGLE_SERVICE_ACCOUNT_KEY"
- **Fix:** Ensure you copied entire JSON object, including outer `{}`
- Wrap in single quotes in Railway UI

### PayPal errors:

**Error:** "Failed to get PayPal access token"
- **Fix:** Verify `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` are correct
- Check `PAYPAL_MODE` matches your credentials (sandbox vs live)

**Error:** "PayPal API error creating order"
- **Fix:** Check PayPal dashboard for API status
- Verify your PayPal account is active and verified

---

## Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_KEY` | Yes | None | Full JSON service account credentials |
| `COACH_GOOGLE_CALENDAR_ID` | No | `'primary'` | Calendar ID to create events in |
| `COACH_EMAIL` | Yes | None | Coach email for calendar invites |
| `COACH_PHONE_NUMBER` | Yes | None | Coach phone number (format: +1234567890) |
| `PAYPAL_CLIENT_ID` | Yes | None | PayPal app client ID |
| `PAYPAL_CLIENT_SECRET` | Yes | None | PayPal app secret |
| `PAYPAL_MODE` | No | `'sandbox'` | `'sandbox'` or `'live'` |
| `PAYPAL_RETURN_URL` | No | Auto-generated | URL after successful payment |
| `PAYPAL_CANCEL_URL` | No | Auto-generated | URL if user cancels payment |
| `SENDGRID_API_KEY` | No | None | SendGrid API key (for email notifications) |
| `TWILIO_SMS_ENABLED` | No | `'false'` | Enable SMS notifications |

---

**Ready to deploy?** Add the required variables above to Railway, then proceed with deployment!
