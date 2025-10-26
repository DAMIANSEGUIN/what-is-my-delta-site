-- Add subscription and discount code support to users table
-- Migration: 001_add_discount_codes
-- Date: 2025-10-26

-- Add subscription tracking columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR(20) DEFAULT 'free';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS discount_code VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS trial_end_date TIMESTAMP;

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_subscription ON users(subscription_tier, subscription_status);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer ON users(stripe_customer_id);

-- Create discount_codes table
CREATE TABLE IF NOT EXISTS discount_codes (
    code VARCHAR(50) PRIMARY KEY,
    description TEXT,
    grants_tier VARCHAR(20) DEFAULT 'beta',
    max_uses INTEGER DEFAULT NULL,
    current_uses INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT NULL
);

-- Add initial beta discount codes
INSERT INTO discount_codes (code, description, grants_tier, max_uses) VALUES
    ('BETA2025', 'Initial beta access - lifetime free', 'beta', NULL),
    ('EARLYBIRD', 'Early adopter - lifetime free', 'beta', 100),
    ('FOUNDER', 'Founder tier - lifetime free', 'beta', 50)
ON CONFLICT (code) DO NOTHING;
