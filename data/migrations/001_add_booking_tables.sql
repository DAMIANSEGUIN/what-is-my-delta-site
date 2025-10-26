-- Migration: Add booking system tables
-- Date: 2025-10-25
-- Description: Core booking functionality with payments, packages, and notifications

-- 1. Session Packages (must be created first due to foreign key)
CREATE TABLE IF NOT EXISTS session_packages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Package details
  package_type VARCHAR(50) NOT NULL, -- 'three_pack'
  sessions_total INTEGER NOT NULL, -- 3
  sessions_used INTEGER DEFAULT 0,

  -- Payment
  purchase_date TIMESTAMPTZ DEFAULT NOW(),
  stripe_payment_intent_id VARCHAR(255) UNIQUE,
  amount_paid DECIMAL(10,2) NOT NULL,
  currency VARCHAR(3) NOT NULL, -- 'USD' or 'CAD'

  -- Status
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'expired', 'refunded'
  expires_at TIMESTAMPTZ, -- Optional: packages expire after X months

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Appointments
CREATE TABLE IF NOT EXISTS appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  google_event_id VARCHAR(255) UNIQUE NOT NULL,

  -- Session details
  session_type VARCHAR(50) NOT NULL, -- 'free', 'paid_single', 'paid_package'
  promo_code VARCHAR(50),
  scheduled_datetime TIMESTAMPTZ NOT NULL,
  backup_datetime TIMESTAMPTZ,
  duration_minutes INTEGER DEFAULT 30,

  -- Contact info
  user_phone VARCHAR(20) NOT NULL,
  user_email VARCHAR(255) NOT NULL,

  -- Status tracking
  status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'completed', 'cancelled', 'no_show', 'rescheduled'

  -- Payment
  payment_status VARCHAR(50), -- 'pending', 'paid', 'refunded', 'partial_refund'
  payment_amount DECIMAL(10,2),
  payment_currency VARCHAR(3), -- 'USD' or 'CAD'
  stripe_payment_intent_id VARCHAR(255),
  package_id UUID REFERENCES session_packages(id) ON DELETE SET NULL,

  -- Reschedule tracking
  reschedule_count INTEGER DEFAULT 0,
  cancellation_fee_applied BOOLEAN DEFAULT FALSE,
  cancellation_fee_amount DECIMAL(10,2),

  -- Notifications
  notification_preferences JSONB DEFAULT '{"email": true, "inapp": true, "sms": false}'::jsonb,

  -- Preparation notes
  preparation_notes TEXT DEFAULT 'Prepare for your session by completing the AI prompts from your previous conversations as far as you are able.',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  cancelled_at TIMESTAMPTZ
);

-- 3. Promo Codes
CREATE TABLE IF NOT EXISTS promo_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(50) UNIQUE NOT NULL,
  max_uses INTEGER DEFAULT 25,
  current_uses INTEGER DEFAULT 0,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Coach Availability (default schedule)
CREATE TABLE IF NOT EXISTS coach_availability (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  day_of_week INTEGER NOT NULL, -- 0=Sunday, 1=Monday, ..., 6=Saturday
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  timezone VARCHAR(50) DEFAULT 'America/Toronto',
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Blocked Dates (PTO, holidays, etc.)
CREATE TABLE IF NOT EXISTS blocked_dates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  blocked_date DATE NOT NULL UNIQUE,
  reason VARCHAR(255),
  notify_affected_users BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Notification Log (track what was sent)
CREATE TABLE IF NOT EXISTS notification_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  appointment_id UUID REFERENCES appointments(id) ON DELETE CASCADE,
  notification_type VARCHAR(50) NOT NULL, -- 'email', 'sms', 'inapp'
  notification_event VARCHAR(50) NOT NULL, -- 'booking_confirmed', 'reminder_24h', 'cancellation', 'reschedule'
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'sent', -- 'sent', 'failed', 'delivered'
  error_message TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_appointments_user_id ON appointments(user_id);
CREATE INDEX IF NOT EXISTS idx_appointments_scheduled_datetime ON appointments(scheduled_datetime);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_appointments_google_event_id ON appointments(google_event_id);
CREATE INDEX IF NOT EXISTS idx_session_packages_user_id ON session_packages(user_id);
CREATE INDEX IF NOT EXISTS idx_session_packages_stripe_id ON session_packages(stripe_payment_intent_id);
CREATE INDEX IF NOT EXISTS idx_blocked_dates_date ON blocked_dates(blocked_date);
CREATE INDEX IF NOT EXISTS idx_notification_log_appointment_id ON notification_log(appointment_id);

-- Update trigger for appointments.updated_at
CREATE OR REPLACE FUNCTION update_appointments_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER appointments_updated_at_trigger
  BEFORE UPDATE ON appointments
  FOR EACH ROW
  EXECUTE FUNCTION update_appointments_updated_at();

-- Comments for documentation
COMMENT ON TABLE appointments IS 'Stores all coaching session bookings';
COMMENT ON TABLE session_packages IS 'Stores multi-session package purchases';
COMMENT ON TABLE promo_codes IS 'Promo codes for free sessions';
COMMENT ON TABLE coach_availability IS 'Coach default weekly availability schedule';
COMMENT ON TABLE blocked_dates IS 'Dates when coach is unavailable';
COMMENT ON TABLE notification_log IS 'Audit log of all notifications sent';
