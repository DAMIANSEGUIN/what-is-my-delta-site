export default async function handler(req, res) {
  // Placeholder: in production you would query Supabase with service role (server-side)
  const now = new Date().toISOString();
  const stats = {
    generated_at: now,
    top_prompts: [
      { index: 0, text: "What problem are you trying to solve, in one sentence?", count: 12 },
      { index: 3, text: "What’s one action you can take in the next 48 hours?", count: 9 }
    ],
    themes: ["scope", "obstacles", "momentum"]
  };
  res.setHeader('Content-Type', 'application/json');
  res.status(200).send(JSON.stringify(stats));
}