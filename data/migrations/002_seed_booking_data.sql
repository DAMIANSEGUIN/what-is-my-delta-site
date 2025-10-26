-- Migration: Seed initial booking data
-- Date: 2025-10-25
-- Description: Insert promo code and default coach availability

-- Seed promo code: WIMD25 (25 uses)
INSERT INTO promo_codes (code, max_uses, active)
VALUES ('WIMD25', 25, true)
ON CONFLICT (code) DO NOTHING;

-- Seed default coach availability
-- Monday-Friday, 9AM-5PM EST (America/Toronto)
-- User (Damian) can modify these via admin interface later

INSERT INTO coach_availability (day_of_week, start_time, end_time, timezone, active) VALUES
  (1, '09:00:00', '17:00:00', 'America/Toronto', true), -- Monday
  (2, '09:00:00', '17:00:00', 'America/Toronto', true), -- Tuesday
  (3, '09:00:00', '17:00:00', 'America/Toronto', true), -- Wednesday
  (4, '09:00:00', '17:00:00', 'America/Toronto', true), -- Thursday
  (5, '09:00:00', '17:00:00', 'America/Toronto', true)  -- Friday
ON CONFLICT DO NOTHING;

-- Create view for sessions_remaining calculation
CREATE OR REPLACE VIEW session_packages_with_remaining AS
SELECT
  id,
  user_id,
  package_type,
  sessions_total,
  sessions_used,
  (sessions_total - sessions_used) AS sessions_remaining,
  purchase_date,
  stripe_payment_intent_id,
  amount_paid,
  currency,
  status,
  expires_at,
  created_at
FROM session_packages;

COMMENT ON VIEW session_packages_with_remaining IS 'Convenient view with calculated sessions_remaining field';
