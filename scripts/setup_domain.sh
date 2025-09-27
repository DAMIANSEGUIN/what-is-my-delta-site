#!/bin/zsh
set -euo pipefail

# WIMD Domain Setup - One Shot Script
# This script sets up whatismydelta.com with Railway

echo "=== WIMD Domain Setup ==="
echo "Setting up whatismydelta.com with Railway..."

# Step 1: Check current domains
echo "Step 1: Checking current Railway domains..."
railway domain

# Step 2: Get verification records
echo "Step 2: Getting verification records..."
echo "Railway will show TXT records you need to add to Netlify DNS"
railway domain whatismydelta.com

# Step 3: Wait for user to add TXT records
echo ""
echo "Step 3: MANUAL ACTION REQUIRED"
echo "1. Go to Netlify DNS panel"
echo "2. Add the TXT record shown above"
echo "3. Wait for Railway to verify (check dashboard)"
echo "4. Press Enter when Railway shows domain as 'Ready'"
read -p "Press Enter when Railway domain is verified..."

# Step 4: Test domains
echo "Step 4: Testing domains..."
echo "Testing www.whatismydelta.com..."
curl -s https://www.whatismydelta.com/health || echo "www.whatismydelta.com not ready yet"

echo "Testing whatismydelta.com..."
curl -s https://whatismydelta.com/health || echo "whatismydelta.com not ready yet"

# Step 5: Final verification
echo ""
echo "Step 5: Final verification..."
echo "Run these commands to test:"
echo "curl https://www.whatismydelta.com/health"
echo "curl https://whatismydelta.com/health"
echo ""
echo "=== Domain Setup Complete ==="
