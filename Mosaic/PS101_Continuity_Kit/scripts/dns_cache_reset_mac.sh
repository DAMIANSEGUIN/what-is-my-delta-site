#!/bin/zsh
set -euo pipefail
/usr/bin/dscacheutil -flushcache
/usr/bin/killall -HUP mDNSResponder || true
