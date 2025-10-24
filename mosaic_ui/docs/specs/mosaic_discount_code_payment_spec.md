# Mosaic Discount Code + Payment Infrastructure Specification

**Feature**: Access control via discount codes (beta) → Stripe subscriptions (production)
**Status**: New Feature (Phased Implementation)
**Complexity**: Medium
**Implementation**: Frontend + Backend + Database + Stripe Integration

---

## Overview

Build a unified access control system that:
1. **Phase 1 (Beta)**: Requires discount codes for platform access
2. **Phase 2 (Launch)**: Transitions to Stripe-powered paid subscriptions
3. **Architecture**: Designed from the start to support both, with feature flag toggle

---

## Architecture Principles

1. **Single source of truth**: User access determined by `subscription_tier` field
2. **Feature-flagged**: `PAYMENTS_ENABLED` flag controls which system is active
3. **Backward compatible**: Beta users with discount codes get permanent free access
4. **Graceful transition**: No breaking changes when enabling payments
5. **Test mode first**: Build and test Stripe integration in test mode during beta

---

## Database Schema

### Modified Table: `users`

```sql
-- Add subscription and payment tracking columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR(20) DEFAULT 'free';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS trial_end_date TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS discount_code VARCHAR(50) REFERENCES discount_codes(code);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_subscription ON users(subscription_tier, subscription_status);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer ON users(stripe_customer_id);
```

**Subscription Tiers**:
- `beta` - Beta users with discount codes (free forever)
- `free` - Free trial users (limited access/time)
- `basic` - Paid tier 1
- `pro` - Paid tier 2
- `enterprise` - Paid tier 3

**Subscription Status**:
- `active` - Full access
- `trialing` - In trial period
- `past_due` - Payment failed, grace period
- `canceled` - Subscription canceled
- `expired` - Trial or subscription ended

### New Table: `discount_codes`

```sql
CREATE TABLE IF NOT EXISTS discount_codes (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT,
    grants_tier VARCHAR(20) DEFAULT 'beta',  -- Which tier this code grants
    max_uses INTEGER DEFAULT NULL,  -- NULL = unlimited
    current_uses INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT NULL
);

-- Add initial beta codes
INSERT INTO discount_codes (code, description, grants_tier, max_uses) VALUES
    ('BETA2025', 'Initial beta access - lifetime free', 'beta', NULL),
    ('EARLYBIRD', 'Early adopter - lifetime free', 'beta', 100),
    ('FOUNDER', 'Founder tier - lifetime free', 'beta', 50);
```

### New Table: `payment_events`

```sql
CREATE TABLE IF NOT EXISTS payment_events (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    event_type VARCHAR(50) NOT NULL,  -- stripe event type
    stripe_event_id VARCHAR(100) UNIQUE,
    amount INTEGER,  -- in cents
    currency VARCHAR(10),
    status VARCHAR(20),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payment_events_user ON payment_events(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_events_type ON payment_events(event_type);
```

---

## Backend Implementation

### Settings: Feature Flags & Config

```python
# api/settings.py

class Settings(BaseSettings):
    # ... existing settings ...

    # Payment feature flags
    PAYMENTS_ENABLED: bool = False  # Toggle to enable Stripe payments
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Subscription pricing (Stripe Price IDs)
    STRIPE_PRICE_BASIC_MONTHLY: str = ""
    STRIPE_PRICE_BASIC_YEARLY: str = ""
    STRIPE_PRICE_PRO_MONTHLY: str = ""
    STRIPE_PRICE_PRO_YEARLY: str = ""

    # Trial settings
    FREE_TRIAL_DAYS: int = 14
    TRIAL_WITHOUT_PAYMENT: bool = True  # Allow trial without credit card
```

### Access Control Middleware

```python
# api/access_control.py

from datetime import datetime
from fastapi import HTTPException, Depends, Header
from typing import Optional

def get_user_access_level(user_id: str) -> dict:
    """Get user's current access level and limits"""

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT subscription_tier, subscription_status, trial_end_date,
                   discount_code, stripe_customer_id
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    tier, status, trial_end, discount_code, stripe_customer = result

    # Determine access
    has_access = False
    reason = None

    # Beta users (discount codes) always have access
    if tier == 'beta':
        has_access = True
        reason = "Beta access (lifetime)"

    # Active paid subscriptions
    elif status == 'active' and tier in ['basic', 'pro', 'enterprise']:
        has_access = True
        reason = f"Active {tier} subscription"

    # Trialing users
    elif status == 'trialing' and trial_end and datetime.now() < trial_end:
        has_access = True
        reason = f"Trial (ends {trial_end.date()})"

    # No access
    else:
        has_access = False
        reason = "No active subscription or trial"

    return {
        "user_id": user_id,
        "has_access": has_access,
        "subscription_tier": tier,
        "subscription_status": status,
        "reason": reason,
        "trial_end_date": trial_end.isoformat() if trial_end else None,
        "is_beta": tier == 'beta',
        "is_paid": tier in ['basic', 'pro', 'enterprise']
    }


def require_active_subscription(user_id: str = Depends(get_current_user_id)):
    """Dependency to require active subscription for protected endpoints"""
    access = get_user_access_level(user_id)

    if not access["has_access"]:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail={
                "error": "Subscription required",
                "message": "Your trial has ended. Please subscribe to continue.",
                "subscription_status": access["subscription_status"]
            }
        )

    return access
```

### Discount Code Endpoints

```python
# api/index.py

class DiscountCodeValidate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)

class DiscountCodeResponse(BaseModel):
    valid: bool
    message: str
    grants_tier: Optional[str] = None

@app.post("/auth/validate-code", response_model=DiscountCodeResponse)
async def validate_discount_code(payload: DiscountCodeValidate):
    """Validate a discount code"""
    code = payload.code.strip().upper()

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT code, grants_tier, max_uses, current_uses, active, expires_at
            FROM discount_codes
            WHERE UPPER(code) = %s
        """, (code,))
        result = cursor.fetchone()

    if not result:
        return DiscountCodeResponse(valid=False, message="Invalid discount code")

    code_value, grants_tier, max_uses, current_uses, active, expires_at = result

    # Check if active
    if not active:
        return DiscountCodeResponse(valid=False, message="This code is no longer active")

    # Check expiration
    if expires_at and datetime.now() > expires_at:
        return DiscountCodeResponse(valid=False, message="This code has expired")

    # Check usage limit
    if max_uses is not None and current_uses >= max_uses:
        return DiscountCodeResponse(valid=False, message="This code has reached its usage limit")

    return DiscountCodeResponse(
        valid=True,
        message=f"Code valid - grants {grants_tier} access",
        grants_tier=grants_tier
    )


class UserRegister(BaseModel):
    email: str
    password: str
    discount_code: Optional[str] = None  # Required if PAYMENTS_ENABLED=false

@app.post("/auth/register", response_model=UserResponse)
async def register_user(payload: UserRegister):
    """Register a new user with discount code or free trial"""

    settings = get_settings()
    subscription_tier = 'free'
    trial_end_date = None

    # If payments disabled, require discount code
    if not settings.PAYMENTS_ENABLED:
        if not payload.discount_code:
            raise HTTPException(
                status_code=400,
                detail="Discount code required during beta"
            )

        # Validate and consume discount code
        code = payload.discount_code.strip().upper()

        with get_conn() as conn:
            cursor = conn.cursor()

            # Validate code
            cursor.execute("""
                SELECT code, grants_tier, max_uses, current_uses, active, expires_at
                FROM discount_codes
                WHERE UPPER(code) = %s
            """, (code,))
            code_result = cursor.fetchone()

            if not code_result:
                raise HTTPException(status_code=400, detail="Invalid discount code")

            code_value, grants_tier, max_uses, current_uses, active, expires_at = code_result

            if not active:
                raise HTTPException(status_code=400, detail="Code is no longer active")

            if expires_at and datetime.now() > expires_at:
                raise HTTPException(status_code=400, detail="Code has expired")

            if max_uses is not None and current_uses >= max_uses:
                raise HTTPException(status_code=400, detail="Code usage limit reached")

            # Grant tier from code
            subscription_tier = grants_tier

            # Increment usage
            cursor.execute("""
                UPDATE discount_codes
                SET current_uses = current_uses + 1
                WHERE code = %s
            """, (code_value,))
            conn.commit()

    else:
        # Payments enabled - start free trial
        subscription_tier = 'free'
        trial_end_date = datetime.now() + timedelta(days=settings.FREE_TRIAL_DAYS)

    # Check if user exists
    existing_user = get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create user
    user_id = create_user(
        email=payload.email,
        password=payload.password,
        subscription_tier=subscription_tier,
        subscription_status='active',
        trial_end_date=trial_end_date,
        discount_code=payload.discount_code.upper() if payload.discount_code else None
    )

    user = get_user_by_id(user_id)

    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        last_login=user["last_login"],
        subscription_tier=subscription_tier,
        subscription_status='active'
    )
```

### Stripe Integration (Feature-Flagged)

```python
# api/payments.py

import stripe
from fastapi import Request, HTTPException
from .settings import get_settings

settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSessionCreate(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str

class PortalSessionCreate(BaseModel):
    return_url: str


@app.post("/payments/create-checkout-session")
async def create_checkout_session(
    payload: CheckoutSessionCreate,
    access: dict = Depends(require_active_subscription)
):
    """Create Stripe checkout session for subscription"""

    if not get_settings().PAYMENTS_ENABLED:
        raise HTTPException(status_code=503, detail="Payments not yet available")

    user_id = access["user_id"]
    user = get_user_by_id(user_id)

    # Get or create Stripe customer
    stripe_customer_id = user.get("stripe_customer_id")

    if not stripe_customer_id:
        customer = stripe.Customer.create(
            email=user["email"],
            metadata={"user_id": user_id}
        )
        stripe_customer_id = customer.id

        # Store customer ID
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET stripe_customer_id = %s
                WHERE user_id = %s
            """, (stripe_customer_id, user_id))
            conn.commit()

    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': payload.price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=payload.success_url,
        cancel_url=payload.cancel_url,
        metadata={
            'user_id': user_id
        }
    )

    return {"session_id": session.id, "url": session.url}


@app.post("/payments/create-portal-session")
async def create_portal_session(
    payload: PortalSessionCreate,
    access: dict = Depends(require_active_subscription)
):
    """Create Stripe customer portal session"""

    if not get_settings().PAYMENTS_ENABLED:
        raise HTTPException(status_code=503, detail="Payments not yet available")

    user_id = access["user_id"]
    user = get_user_by_id(user_id)

    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        raise HTTPException(status_code=400, detail="No Stripe customer found")

    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=payload.return_url
    )

    return {"url": session.url}


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""

    settings = get_settings()
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle different event types
    event_type = event['type']
    event_data = event['data']['object']

    with get_conn() as conn:
        cursor = conn.cursor()

        if event_type == 'checkout.session.completed':
            # Payment successful - activate subscription
            customer_id = event_data['customer']
            subscription_id = event_data['subscription']

            cursor.execute("""
                UPDATE users
                SET subscription_tier = 'basic',
                    subscription_status = 'active',
                    stripe_subscription_id = %s
                WHERE stripe_customer_id = %s
            """, (subscription_id, customer_id))

        elif event_type == 'customer.subscription.updated':
            # Subscription changed
            subscription_id = event_data['id']
            status = event_data['status']

            cursor.execute("""
                UPDATE users
                SET subscription_status = %s
                WHERE stripe_subscription_id = %s
            """, (status, subscription_id))

        elif event_type == 'customer.subscription.deleted':
            # Subscription canceled
            subscription_id = event_data['id']

            cursor.execute("""
                UPDATE users
                SET subscription_status = 'canceled'
                WHERE stripe_subscription_id = %s
            """, (subscription_id,))

        elif event_type == 'invoice.payment_failed':
            # Payment failed
            subscription_id = event_data['subscription']

            cursor.execute("""
                UPDATE users
                SET subscription_status = 'past_due'
                WHERE stripe_subscription_id = %s
            """, (subscription_id,))

        # Log event
        cursor.execute("""
            INSERT INTO payment_events (user_id, event_type, stripe_event_id, metadata)
            SELECT user_id, %s, %s, %s
            FROM users
            WHERE stripe_customer_id = %s OR stripe_subscription_id = %s
        """, (
            event_type,
            event['id'],
            json.dumps(event_data),
            event_data.get('customer'),
            event_data.get('subscription')
        ))

        conn.commit()

    return {"status": "success"}


@app.get("/payments/config")
async def get_payment_config():
    """Get public payment configuration"""
    settings = get_settings()

    return {
        "payments_enabled": settings.PAYMENTS_ENABLED,
        "publishable_key": settings.STRIPE_PUBLISHABLE_KEY if settings.PAYMENTS_ENABLED else None,
        "prices": {
            "basic_monthly": settings.STRIPE_PRICE_BASIC_MONTHLY,
            "basic_yearly": settings.STRIPE_PRICE_BASIC_YEARLY,
            "pro_monthly": settings.STRIPE_PRICE_PRO_MONTHLY,
            "pro_yearly": settings.STRIPE_PRICE_PRO_YEARLY
        } if settings.PAYMENTS_ENABLED else {}
    }
```

### Modified Storage Functions

```python
# api/storage.py

def create_user(
    email: str,
    password: str,
    subscription_tier: str = 'free',
    subscription_status: str = 'active',
    trial_end_date: datetime = None,
    discount_code: str = None
) -> str:
    """Create a new user with subscription info"""
    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (
                user_id, email, password_hash,
                subscription_tier, subscription_status, trial_end_date, discount_code,
                created_at, last_login
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (email) DO NOTHING
            RETURNING user_id
        """, (user_id, email, password_hash, subscription_tier, subscription_status,
              trial_end_date, discount_code))
        result = cursor.fetchone()
        conn.commit()

    return result[0] if result else None
```

---

## Frontend Implementation

### Phase 1: Discount Code Modal (Beta)

```html
<!-- DISCOUNT CODE MODAL (shown when PAYMENTS_ENABLED = false) -->
<div id="discountModal" class="modal" style="display:none">
  <div class="panel" style="max-width:400px">
    <h2 style="font:600 14px/1.2 Helvetica,Arial;margin:0 0 20px;text-transform:uppercase;letter-spacing:.08em;text-align:center">enter access code</h2>

    <p style="margin:0 0 24px;color:var(--muted);font-size:11px;line-height:1.5;text-align:center">
      this platform is currently in beta. enter your discount code to get lifetime free access.
    </p>

    <form id="discountForm">
      <div style="margin-bottom:16px">
        <label style="display:block;font-size:10px;color:var(--muted);margin-bottom:4px;text-transform:uppercase;letter-spacing:.08em">discount code</label>
        <input type="text" id="discountCode" required style="width:100%;padding:8px;border:1px solid var(--line);font-size:12px;text-transform:uppercase" placeholder="BETA2025">
      </div>
      <button type="submit" class="quiet" style="width:100%;padding:10px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;background:var(--hair);color:#fff;border:1px solid var(--hair)">validate code</button>
    </form>

    <div id="discountStatus" class="status" style="margin-top:12px;text-align:center"></div>
  </div>
</div>
```

### Phase 2: Subscription UI (Production)

```html
<!-- SUBSCRIPTION MODAL (shown when trial expires and PAYMENTS_ENABLED = true) -->
<div id="subscriptionModal" class="modal" style="display:none">
  <div class="panel" style="max-width:600px">
    <h2 style="font:600 14px/1.2 Helvetica,Arial;margin:0 0 20px;text-transform:uppercase;letter-spacing:.08em;text-align:center">choose your plan</h2>

    <div style="display:flex;gap:20px;margin-bottom:24px">
      <!-- Basic Plan -->
      <div class="section-card" style="flex:1;padding:20px;border:1px solid var(--line);border-radius:4px">
        <h3 style="font:600 13px/1.2 Helvetica,Arial;margin:0 0 8px;text-transform:uppercase">basic</h3>
        <p style="font:400 24px/1.2 Helvetica,Arial;margin:0 0 16px">$29<span style="font-size:12px;color:var(--muted)">/mo</span></p>
        <ul style="margin:0 0 20px;padding-left:20px;font-size:11px;color:var(--muted)">
          <li>unlimited job searches</li>
          <li>resume optimization</li>
          <li>AI career coaching</li>
          <li>email support</li>
        </ul>
        <button class="subscribe-btn quiet" data-price-id="price_basic_monthly" style="width:100%;padding:10px;font-size:11px;text-transform:uppercase;letter-spacing:.08em">select plan</button>
      </div>

      <!-- Pro Plan -->
      <div class="section-card" style="flex:1;padding:20px;border:2px solid var(--hair);border-radius:4px">
        <div style="text-align:center;margin-bottom:8px">
          <span style="font-size:9px;text-transform:uppercase;letter-spacing:.08em;background:var(--hair);color:#fff;padding:2px 8px;border-radius:2px">popular</span>
        </div>
        <h3 style="font:600 13px/1.2 Helvetica,Arial;margin:0 0 8px;text-transform:uppercase">pro</h3>
        <p style="font:400 24px/1.2 Helvetica,Arial;margin:0 0 16px">$79<span style="font-size:12px;color:var(--muted)">/mo</span></p>
        <ul style="margin:0 0 20px;padding-left:20px;font-size:11px;color:var(--muted)">
          <li>everything in basic</li>
          <li>competitive intelligence</li>
          <li>company OSINT analysis</li>
          <li>priority support</li>
          <li>1-on-1 coaching sessions</li>
        </ul>
        <button class="subscribe-btn quiet" data-price-id="price_pro_monthly" style="width:100%;padding:10px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;background:var(--hair);color:#fff;border:1px solid var(--hair)">select plan</button>
      </div>
    </div>

    <p style="text-align:center;font-size:10px;color:var(--muted)">
      all plans include 14-day free trial • cancel anytime
    </p>
  </div>
</div>
```

### JavaScript: Unified Access Control

```javascript
(function() {
  'use strict';

  let paymentsEnabled = false;
  let validatedCode = localStorage.getItem('validatedDiscountCode');

  // Fetch payment config on load
  fetch(`${API_BASE}/payments/config`)
    .then(r => r.json())
    .then(config => {
      paymentsEnabled = config.payments_enabled;

      // Show appropriate modal
      if (!paymentsEnabled && !validatedCode) {
        // Beta mode - show discount code modal
        document.getElementById('discountModal').style.display = 'block';
      } else {
        // Either payments enabled or code validated - show auth
        document.getElementById('authModal').style.display = 'block';
      }
    });

  // Discount code validation
  const discountForm = document.getElementById('discountForm');
  if (discountForm) {
    discountForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const code = document.getElementById('discountCode').value.trim();
      const status = document.getElementById('discountStatus');

      status.textContent = 'Validating...';
      status.className = 'status';

      try {
        const response = await fetch(`${API_BASE}/auth/validate-code`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code })
        });

        const data = await response.json();

        if (data.valid) {
          localStorage.setItem('validatedDiscountCode', code.toUpperCase());
          status.textContent = 'Code validated! Redirecting...';
          status.className = 'status ok';

          setTimeout(() => {
            document.getElementById('discountModal').style.display = 'none';
            document.getElementById('authModal').style.display = 'block';
          }, 1000);
        } else {
          status.textContent = data.message || 'Invalid code';
          status.className = 'status error';
        }
      } catch (err) {
        console.error('Code validation error:', err);
        status.textContent = 'Validation failed. Please try again.';
        status.className = 'status error';
      }
    });
  }

  // Modified registration to include discount code
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('registerEmail').value;
      const password = document.getElementById('registerPassword').value;
      const confirm = document.getElementById('registerConfirm').value;
      const discountCode = localStorage.getItem('validatedDiscountCode');
      const authStatus = document.getElementById('authStatus');

      if (password !== confirm) {
        authStatus.textContent = 'Passwords do not match';
        authStatus.className = 'status error';
        return;
      }

      if (!paymentsEnabled && !discountCode) {
        authStatus.textContent = 'No discount code found. Please refresh.';
        authStatus.className = 'status error';
        return;
      }

      authStatus.textContent = 'Creating account...';
      authStatus.className = 'status';

      try {
        const response = await fetch(`${API_BASE}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email,
            password,
            discount_code: discountCode || null
          })
        });

        const data = await response.json();

        if (response.ok) {
          authStatus.textContent = 'Account created! Please log in.';
          authStatus.className = 'status ok';

          setTimeout(() => {
            document.getElementById('registerForm').hidden = true;
            document.getElementById('loginForm').hidden = false;
            authStatus.textContent = '';
          }, 1500);
        } else {
          authStatus.textContent = data.detail || 'Registration failed';
          authStatus.className = 'status error';
        }
      } catch (err) {
        console.error('Registration error:', err);
        authStatus.textContent = 'Registration failed. Please try again.';
        authStatus.className = 'status error';
      }
    });
  }

  // Stripe checkout (when payments enabled)
  document.querySelectorAll('.subscribe-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const priceId = e.target.dataset.priceId;

      try {
        const response = await fetch(`${API_BASE}/payments/create-checkout-session`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('session_id')}`
          },
          body: JSON.stringify({
            price_id: priceId,
            success_url: `${window.location.origin}?payment=success`,
            cancel_url: `${window.location.origin}?payment=canceled`
          })
        });

        const data = await response.json();

        if (data.url) {
          window.location.href = data.url;
        }
      } catch (err) {
        console.error('Checkout error:', err);
      }
    });
  });

  // Check subscription status periodically
  setInterval(async () => {
    const sessionId = localStorage.getItem('session_id');
    if (!sessionId) return;

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: { 'Authorization': `Bearer ${sessionId}` }
      });

      const user = await response.json();

      // Show subscription modal if trial expired
      if (user.subscription_status === 'expired' && paymentsEnabled) {
        document.getElementById('subscriptionModal').style.display = 'flex';
      }
    } catch (err) {
      console.error('Status check error:', err);
    }
  }, 60000); // Check every minute

})();
```

---

## Deployment Phases

### Phase 1: Beta (Discount Codes Only)

**Environment Variables**:
```bash
PAYMENTS_ENABLED=false
# No Stripe keys needed yet
```

**Steps**:
1. Run database migrations (add columns, create tables)
2. Deploy backend with discount code endpoints
3. Deploy frontend with discount modal
4. Create initial discount codes via script
5. Test discount code flow end-to-end

### Phase 2: Test Stripe Integration (Beta)

**Environment Variables**:
```bash
PAYMENTS_ENABLED=false
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Steps**:
1. Set up Stripe account in test mode
2. Create products and prices in Stripe dashboard
3. Deploy payment endpoints (but keep PAYMENTS_ENABLED=false)
4. Set up webhook endpoint in Stripe dashboard
5. Test checkout flow with test cards
6. Verify webhook handling

### Phase 3: Production Launch

**Environment Variables**:
```bash
PAYMENTS_ENABLED=true
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_BASIC_MONTHLY=price_...
STRIPE_PRICE_PRO_MONTHLY=price_...
```

**Steps**:
1. Switch Stripe to live mode
2. Update environment variables
3. Deploy with PAYMENTS_ENABLED=true
4. Verify beta users still have access
5. Test new user signup with trial
6. Test subscription checkout flow
7. Monitor webhook events

---

## Access Control Examples

### Protect Endpoints

```python
# Require active subscription for premium features
@app.post("/jobs/search")
async def search_jobs(
    query: str,
    access: dict = Depends(require_active_subscription)
):
    """Search jobs (requires active subscription)"""
    # access["subscription_tier"] tells you what features to enable

    if access["subscription_tier"] == 'pro':
        # Enable OSINT and competitive intelligence
        pass

    # Regular job search logic
    pass
```

### Frontend Feature Gating

```javascript
// Show/hide features based on subscription tier
async function updateUIForSubscription() {
  const response = await fetch(`${API_BASE}/auth/me`, {
    headers: { 'Authorization': `Bearer ${sessionId}` }
  });

  const user = await response.json();

  // Hide pro features for basic tier
  if (user.subscription_tier === 'basic') {
    document.querySelectorAll('.pro-feature').forEach(el => {
      el.style.display = 'none';
    });
  }

  // Show upgrade CTA for free/trial users
  if (user.subscription_tier === 'free' || user.subscription_status === 'trialing') {
    document.getElementById('upgradeCTA').style.display = 'block';
  }
}
```

---

## Testing Checklist

### Phase 1: Discount Codes
- [ ] Discount modal appears for new users
- [ ] Valid code allows registration
- [ ] Invalid code rejected
- [ ] Expired code rejected
- [ ] Max-use enforcement works
- [ ] Beta users have permanent access
- [ ] Code stored in user record
- [ ] Usage counter increments

### Phase 2: Stripe Test Mode
- [ ] Checkout session creates successfully
- [ ] Test card payment succeeds
- [ ] Subscription status updates in database
- [ ] Webhooks received and processed
- [ ] Failed payment handled correctly
- [ ] Subscription cancellation works
- [ ] Customer portal accessible

### Phase 3: Production
- [ ] Beta users unaffected by payments launch
- [ ] New users get trial period
- [ ] Trial expiration triggers subscription modal
- [ ] Live payment processing works
- [ ] Webhooks update database correctly
- [ ] Access control enforced properly
- [ ] Billing portal works

---

## Stripe Setup Checklist

### Test Mode Setup
- [ ] Create Stripe account
- [ ] Create products: Basic, Pro
- [ ] Create prices: monthly/yearly for each
- [ ] Copy price IDs to environment variables
- [ ] Create webhook endpoint
- [ ] Test with test cards
- [ ] Verify webhook delivery

### Production Setup
- [ ] Activate Stripe account (live mode)
- [ ] Re-create products in live mode
- [ ] Copy live price IDs
- [ ] Update webhook endpoint to live
- [ ] Set up billing portal
- [ ] Configure email receipts
- [ ] Set up failed payment retry logic
- [ ] Add tax collection (if applicable)

---

## Admin Scripts

### List All Users with Access Levels

```python
# scripts/list_user_access.py

from api.storage import get_conn
from datetime import datetime

def list_users():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT email, subscription_tier, subscription_status,
                   trial_end_date, discount_code, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()

    print("\n👥 User Access Levels:\n")
    for email, tier, status, trial_end, code, created in users:
        access = "✅" if status == 'active' else "❌"
        trial_info = f"Trial ends: {trial_end}" if trial_end else ""
        code_info = f"Code: {code}" if code else ""

        print(f"{access} {email:30} [{tier:10}] [{status:10}] {trial_info} {code_info}")

if __name__ == "__main__":
    list_users()
```

### Grant Free Access to User

```python
# scripts/grant_free_access.py

from api.storage import get_conn

def grant_free_access(email: str):
    """Grant permanent free (beta) access to a user"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET subscription_tier = 'beta',
                subscription_status = 'active',
                discount_code = 'ADMIN_GRANTED'
            WHERE email = %s
        """, (email,))
        conn.commit()

    print(f"✅ Granted free access to {email}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python grant_free_access.py user@example.com")
    else:
        grant_free_access(sys.argv[1])
```

---

## Pricing Strategy

### Suggested Pricing Tiers

**Basic - $29/month or $290/year** (save 17%)
- Unlimited job searches
- Resume optimization
- AI career coaching
- Email support

**Pro - $79/month or $790/year** (save 17%)
- Everything in Basic
- Competitive intelligence
- Company OSINT analysis
- Priority support
- 2x 1-on-1 coaching sessions/month

**Enterprise - Custom pricing**
- Everything in Pro
- Dedicated account manager
- Custom integrations
- Team licenses
- White-label options

---

## Rollback Plan

If issues arise after enabling payments:

1. **Immediate**: Set `PAYMENTS_ENABLED=false` in Railway
2. **Verify**: Beta users still have access
3. **Communicate**: Notify users payments temporarily disabled
4. **Debug**: Check webhook logs, payment events table
5. **Fix**: Address issues in test mode
6. **Re-enable**: Flip flag back when ready

---

## Future Enhancements

- [ ] Annual discount pricing
- [ ] Referral program (give 1 month, get 1 month)
- [ ] Usage-based pricing tiers
- [ ] Team/organization accounts
- [ ] Gift subscriptions
- [ ] Lifetime deals for early adopters
- [ ] Add-on purchases (extra coaching sessions)
- [ ] Charity/nonprofit discounts

---

**END OF SPECIFICATION**
