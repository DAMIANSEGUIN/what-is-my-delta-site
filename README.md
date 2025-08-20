# What is my Delta? — Front-End Intro Flow

This is a static, deploy-ready bundle. It provides:
- **Try CoachAI** section with an embed placeholder (paste your Voiceflow or other chat widget).
- **PS101-based intro flow** with branching:
  - Variant A: Linear wizard (`?variant=A`)
  - Variant B: Conversational start (`?variant=B`)
- **Export to Markdown** of the user’s session.

## Files
- `index.html` — main entry
- `assets/styles.css` — minimal styling
- `assets/app.js` — logic for the flow, variants, export
- `.vercel.json` — clean URLs for Vercel
- `netlify.toml` — security headers for Netlify

## How to Host

### Option 1: Vercel (Ideal for iteration)
1. Create a new GitHub repo and push these files.
2. In Vercel, **New Project → Import** the repo.
3. Framework: **Other** (static). Build command: _none_. Output: `/`.
4. Deploy. Your site is live with HTTPS.
5. A/B: append `?variant=A` or `?variant=B` to the URL.

### Option 2: Netlify (Drag-and-drop)
1. Go to app.netlify.com → Sites → "+ New site" → "Deploy manually".
2. **Drag the folder** containing these files.
3. It will deploy instantly with a live URL.
4. Test variants with `?variant=A` or `?variant=B`.

### Option 3: Cloudflare Pages (Fast CDN, simple)
1. Create a new project and connect the Git repo OR upload the folder.
2. Set as static. No build step.
3. Deploy. Use query params for A/B.

## Add Your Chat Widget
Open `index.html` and paste your Voiceflow (or similar) embed where indicated:
```html
<div id="chat-embed" class="embed-placeholder">
  <!-- Paste widget script here -->
</div>
```

## Local Preview
Open `index.html` directly in your browser, or serve the folder with any static server.

## Exporting Sessions
Click **Download Markdown** to save a `what_is_my_delta_session.md` summary.
