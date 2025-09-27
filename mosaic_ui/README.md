# Mosaic Minimal UI — Pack

**Updated:** 2025-09-11 19:24

A breathing‑space, TE‑inspired front‑end for *What Is My Delta* (Mosaic). It’s a single-file demo you can open locally, plus notes for integrating with your backend.

## What’s inside
- `index.html` — unified demo (intro/journey, Fast Track/Discovery, metrics, modules, chat, upload, feedback, save/load, autosave, leave guard)
- `DEPLOY.md` — Vercel/Netlify/Pages steps
- `INTEGRATION.md` — hook chat to `/wimd`, upload to `/wimd/upload`
- `CLAUDE.md`, `CURSOR.md` — collaboration guardrails
- `CHANGELOG.md`, `TODO.md`

## Quickstart
1. Open `index.html` in your browser.
2. To wire chat, in `index.html` replace the `askCoach()` stub with a fetch to your endpoint.
3. Set `SURVEY_URL` if you want to open SurveyMonkey after feedback submit.

## Notes
- Fonts are tiny; whitespace is large by design.
- Everything is native (no libs): SVG lines, `title` tooltips, `<details>`, localStorage.
