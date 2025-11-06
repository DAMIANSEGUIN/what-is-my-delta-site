# Mosaic Production Deployment & Troubleshooting Package — 2025‑11‑05

This single file contains everything required for the current Mosaic deployment on Netlify:
- Netlify configuration (`netlify.toml`)
- SPA redirect fallback (`_redirects`)
- Environment sanity checklist
- Runtime hotfix snippet (`index.html`)
- Verification instructions

Save this file as `MOSAIC_DEPLOYMENT_FULL_2025-11-05.md` in your `.ai-agents/` or `docs/` directory for reference.

---

## 📘 1. netlify.toml

```toml
[build]
  base = "mosaic_ui"
  publish = "mosaic_ui"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https://api.whatismydelta.com https://api.openai.com https://*.openai.com https://*.anthropic.com; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; font-src 'self' data:; frame-ancestors 'self'; base-uri 'self'"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    Permissions-Policy = "geolocation=(), microphone=(), camera=(), fullscreen=(self), payment=()"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/:filename"
  [headers.values]
    Cache-Control = "public, max-age=86400"
```

Place this file at the repository root. Commit and redeploy.

---

## 📄 2. _redirects

If your build ignores Netlify TOML redirects, create a `_redirects` file in the project root containing:

```
/*   /index.html   200
```

---

## ⚙️ 3. Environment Variables (Netlify UI)

Navigate to **Site Settings → Build & Deploy → Environment** and confirm:

| Variable | Example Value | Required |
|-----------|----------------|-----------|
| `VITE_API_BASE` | `https://api.whatismydelta.com` | ✅ |
| `NODE_ENV` | `production` | ✅ |
| `VITE_BUILD_ID` | `3614131613a6e0` | optional |
| `VITE_ENV` | `prod` | optional |

If your code expects `window.__API_BASE`, ensure the API URL is also in your HTML head:

```html
<meta name="api-base" content="https://api.whatismydelta.com">
```

After deploying, confirm from browser console:

```js
window.__API_BASE
fetch(window.__API_BASE + "/health").then(r=>r.text())
```

---

## 🧩 4. Runtime Hotfix Snippet (for index.html)

Append this before `</body>` in your built `index.html` to validate `initApp()` and watch network behavior:

```html
<script>
(function () {
  console.info('[Mosaic][INIT-HOTFIX] Bootstrapping prod checks…');
  window.__APP = window.__APP || { state: {}, actions: {} };
  if (!window.__API_BASE) {
    const metaApi = document.querySelector('meta[name="api-base"]')?.content;
    window.__API_BASE = metaApi || '';
    console.warn('[Mosaic] __API_BASE derived =', window.__API_BASE);
  }
  if (!window.__FETCH_WRAP_INSTALLED__) {
    const _fetch = window.fetch.bind(window);
    window.fetch = async function (url, opts) {
      console.info('[Mosaic][fetch]', url, opts?.method || 'GET');
      try { const r = await _fetch(url, opts); console.info('[Mosaic][fetch][ok]', r.status, url); return r; }
      catch (e) { console.error('[Mosaic][fetch][err]', url, e); throw e; }
    };
    window.__FETCH_WRAP_INSTALLED__ = true;
  }
  function openAuthModal() {
    const modal = document.querySelector('[data-auth-modal],[data-modal="auth"]');
    if (!modal) { console.warn('[Mosaic] Auth modal node not found'); return; }
    modal.style.display = 'block'; modal.removeAttribute('aria-hidden');
    console.info('[Mosaic] Auth modal forced open');
  }
  window.addEventListener('auth:open', openAuthModal);
  setTimeout(() => {
    const userKnown = !!(window.__APP?.state?.auth?.user);
    const modalVisible = !!document.querySelector('[data-auth-modal]:not([aria-hidden="true"])');
    if (!userKnown && !modalVisible) openAuthModal();
  }, 2000);
  if (typeof window.initApp === 'function') {
    const o = window.initApp;
    window.initApp = async function () {
      console.info('[Mosaic][INIT] initApp() starting…');
      const r = await o.apply(this, arguments);
      console.info('[Mosaic][INIT] initApp() done');
      return r;
    };
  } else console.warn('[Mosaic] initApp not found');
})();
</script>
```

---

## 🔍 5. Post‑Deployment Verification Steps

1. **Console Output**
   - `[Mosaic][INIT-HOTFIX] Bootstrapping prod checks…`
   - `[Mosaic][INIT] initApp() starting…` and `done`
   - `[Mosaic][fetch]` lines when sending chat requests

2. **Modal Behavior**
   - If no auth state, modal opens automatically after 2 s.

3. **Network Calls**
   - Confirm fetches appear under Network → `api.whatismydelta.com`.

4. **CSP Confirmation**
   - If blocked, ensure API host is in `connect-src` of your CSP.

5. **Redirect Behavior**
   - Deep links should resolve without 404s (SPA routing verified).

---

## 🚀 Quick Deployment Steps Summary

```bash
# at repo root
printf "%s" "$(cat <<'EOF'
[build]
  base = "mosaic_ui"
  publish = "mosaic_ui"
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
)" > netlify.toml

echo "/*   /index.html   200" > _redirects

git add netlify.toml _redirects
git commit -m "Mosaic deploy config and redirects"
git push
```

Then trigger a Netlify redeploy.

---

**End of Mosaic Deployment & Troubleshooting Package — 2025‑11‑05**
