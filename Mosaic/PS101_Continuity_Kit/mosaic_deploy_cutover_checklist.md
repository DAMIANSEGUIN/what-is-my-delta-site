# Mosaic / PS101 — Production Cutover Checklist (2025‑11‑04)

**Goal**: Serve updated Mosaic/PS101 UI at https://whatismydelta.com with trial-mode auto-init for unauthenticated users.

## A) Commit the pending files
```bash
git add docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md \
        scripts/verify_mosaic_ui.sh \
        frontend/index.html \
        mosaic_ui/index.html \
        netlify.toml
git commit -m "PS101 Mosaic: trial-mode init, guardrails, verify script, set base/publish=mosaic_ui"
git push origin main
```

## B) Netlify production deploy (force dir)
```bash
netlify deploy --prod --site bb594f69-4d23-4817-b7de-dadb8b4db874 --dir mosaic_ui
```

## C) DNS / cache refresh on macOS + Chrome
1. External DNS sanity
   ```bash
   nslookup whatismydelta.com 1.1.1.1
   nslookup whatismydelta.com 8.8.8.8
   ```
2. Local flush
   ```bash
   /usr/bin/dscacheutil -flushcache
   /usr/bin/killall -HUP mDNSResponder
   ```
3. Chrome
   - Quit Chrome (⌘Q), reopen.
   - DevTools → right-click Reload → "Empty Cache and Hard Reload".
   - Visit `chrome://net-internals/#sockets` → Flush socket pools.
   - Optional: `chrome://net-internals/#dns` → Clear host cache.

4. Hosts file check: ensure `/etc/hosts` has **no** entry for `whatismydelta.com`.

## D) Verify production
```bash
# HTTP reachability
curl -I https://whatismydelta.com

# Verify build fingerprint in HTML source:
#   <!-- BUILD_ID:...|SHA:... -->
# Confirm it matches the latest commit.

# Run helper
bash scripts/verify_mosaic_ui.sh
```
Expected UX: no login wall for fresh visitors; trial-mode UI appears; adding `?forceLogin=1` shows the auth modal for QA.