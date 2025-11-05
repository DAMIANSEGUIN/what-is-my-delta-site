#!/bin/bash
# Restore authentication UI and JavaScript to frontend/index.html

set -e

BACKUP="mosaic_ui/index.backup.20251027.html"
CURRENT="frontend/index.html"
OUTPUT="frontend/index.html.with-auth"

echo "🔧 Restoring authentication to frontend..."

# Step 1: Extract auth modals HTML (lines 132-230 from backup)
echo "  Extracting auth modal HTML..."
sed -n '132,230p' "$BACKUP" > /tmp/auth_modals_section.html

# Step 2: Insert auth modals before closing modals div in current frontend
echo "  Merging auth modals into current frontend..."
# Current frontend line 982 is </div> (closing modals), line 984 is <script>
# Insert auth modals between them

head -982 "$CURRENT" > "$OUTPUT"
cat /tmp/auth_modals_section.html >> "$OUTPUT"
tail -n +984 "$CURRENT" >> "$OUTPUT"

echo "  ✅ Auth modals inserted"

# Step 3: Now we need to add auth JavaScript variables and functions
# This is more complex - need to insert after API_BASE declaration

echo "  Extracting auth JavaScript..."

# Extract auth state variables (lines 474-475 from backup)
sed -n '474,475p' "$BACKUP" > /tmp/auth_variables.js

# Extract authenticateUser function (lines 645-720 from backup)
sed -n '645,720p' "$BACKUP" > /tmp/auth_function.js

# Extract logout function (lines 770-810 from backup)
sed -n '770,810p' "$BACKUP" > /tmp/logout_function.js

echo "  ⚠️  Manual merge required for JavaScript"
echo "  Files created in /tmp/:"
echo "    - auth_modals_section.html (inserted)"
echo "    - auth_variables.js (needs manual insertion after API_BASE)"
echo "    - auth_function.js (needs manual insertion)"
echo "    - logout_function.js (needs manual insertion)"

echo ""
echo "📄 Output written to: $OUTPUT"
echo ""
echo "Next steps:"
echo "1. Review $OUTPUT"
echo "2. Manually merge auth JavaScript functions"
echo "3. Add auth event listeners"
echo "4. Test locally"
echo "5. Deploy"
