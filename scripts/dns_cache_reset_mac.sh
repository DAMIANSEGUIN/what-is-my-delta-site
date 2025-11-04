#!/bin/zsh
set -euo pipefail

echo "🔄 Resetting macOS DNS cache..."
/usr/bin/dscacheutil -flushcache
/usr/bin/killall -HUP mDNSResponder || true

echo "✅ DNS cache flushed"
echo ""
echo "Next steps:"
echo "1. Quit Chrome completely (⌘Q)"
echo "2. Reopen Chrome"
echo "3. DevTools → Right-click Reload → 'Empty Cache and Hard Reload'"
echo "4. Visit chrome://net-internals/#sockets → 'Flush socket pools'"
echo "5. Optional: chrome://net-internals/#dns → 'Clear host cache'"

