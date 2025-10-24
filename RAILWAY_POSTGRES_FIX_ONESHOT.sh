#!/bin/bash
# Railway PostgreSQL Connection Fix - One-Shot Command
# Run this after you've manually updated DATABASE_URL in Railway dashboard

set -e

echo "========================================="
echo "Railway PostgreSQL Migration - One-Shot"
echo "========================================="
echo ""

# Step 1: Verify Railway CLI is linked
echo "[1/5] Verifying Railway CLI connection..."
railway status || { echo "ERROR: Railway CLI not connected. Run 'railway link' first."; exit 1; }
echo "✅ Railway CLI connected"
echo ""

# Step 2: Check DATABASE_URL is set
echo "[2/5] Checking DATABASE_URL environment variable..."
DB_URL=$(railway variables | grep -A1 "DATABASE_URL" | tail -1 | awk '{print $2}' | head -c 50)
if [[ -z "$DB_URL" ]]; then
    echo "❌ ERROR: DATABASE_URL not found in Railway variables"
    echo "   You must add DATABASE_URL in Railway dashboard first"
    exit 1
fi
echo "✅ DATABASE_URL found: ${DB_URL}..."
echo ""

# Step 3: Trigger deployment
echo "[3/5] Triggering Railway deployment..."
echo "# PostgreSQL connection test" >> README.md
git add README.md
git commit -m "Deploy: Verify PostgreSQL connection with updated DATABASE_URL"
git push railway-origin main
echo "✅ Deployment triggered"
echo ""

# Step 4: Wait for deployment
echo "[4/5] Waiting for deployment to complete..."
echo "   (This will take ~2 minutes)"
sleep 120
echo "✅ Deployment should be complete"
echo ""

# Step 5: Check logs for PostgreSQL connection
echo "[5/5] Checking deployment logs for PostgreSQL connection..."
echo "   Looking for connection success messages..."
echo ""

railway logs | tail -100 | grep -E "STORAGE|PostgreSQL|mosaic.db" || echo "   (No storage-related logs found in last 100 lines)"

echo ""
echo "========================================="
echo "Deployment Complete"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Check logs above for:"
echo "   ✅ '[STORAGE] ✅ PostgreSQL connection pool created successfully'"
echo "   ❌ 'data/migration_backups/...' (means still using SQLite)"
echo ""
echo "2. Test persistence:"
echo "   - Go to https://whatismydelta.com"
echo "   - Register user: test@example.com / testpass123"
echo "   - Run this script again (triggers new deploy)"
echo "   - Try logging in again"
echo "   - Should work (user persisted)"
echo ""
echo "3. If still seeing SQLite in logs:"
echo "   - DATABASE_URL might still be using public URL (railway.app)"
echo "   - Check Railway dashboard for PRIVATE url (railway.internal)"
echo "   - Update DATABASE_URL and run this script again"
echo ""
