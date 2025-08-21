# What is my Delta? — Front-End Intro Flow

Static bundle with:
- PS101 intro flow + A/B variants (`?variant=A|B`)
- Export to Markdown
- CSV prompt/completion library (local upload, and auto-load from `assets/prompts.csv` if present)
- Voiceflow embed placeholder

## Host on Vercel (fast)
- New Project → Import GitHub repo → Framework: Other (Static)
- Build command: (blank) | Output dir: `/`
- Deploy

## Using the CSV
- For private local use: upload your CSV via the "Prompt Library (CSV)" card.
- To ship with a shared bundle: place your CSV at `assets/prompts.csv` (headers: `prompt,completion`) and deploy. Anyone can then load it from the site.
