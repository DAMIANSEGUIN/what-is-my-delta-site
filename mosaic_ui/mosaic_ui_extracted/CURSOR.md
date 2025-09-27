# CURSOR.md

**Project intent:** single-file HTML/JS demo; no build system.

**Constraints:**
- No dependencies.
- Keep selectors and JS inline or extract only on request.
- Respect whitespace and size choices.
- Use SVG lines + native tooltips only.

**Tasks for Cursor:**
- If asked, extract inline CSS/JS to `styles.css` / `app.js`.
- Implement `askCoach()` with error handling.
- Add optional analytics hooks behind a flag.
