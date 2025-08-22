import { useEffect, useState } from "react";

export default function Status() {
  const [client, setClient] = useState({ tawk:false, css:false });

  useEffect(() => {
    const hasTawk = !!document.querySelector("script[src*=\"embed.tawk.to\"]");
    const hasCss  = !!document.querySelector("link[href*=\"/_next/static/css/\"]") || !!document.querySelector("style[data-n-href]");
    setClient({ tawk: hasTawk, css: hasCss });
  }, []);

  // Vercel exposes these at build time
  const env = process.env.VERCEL_ENV || "unknown";
  const sha = (process.env.VERCEL_GIT_COMMIT_SHA || "").slice(0,7) || "unknown";

  return (
    <main style={{fontFamily:"system-ui, Arial, sans-serif", padding: 24}}>
      <h1>Site Status</h1>
      <p><strong>Environment:</strong> {env}</p>
      <p><strong>Commit:</strong> {sha}</p>
      <h2>Checks</h2>
      <ul>
        <li>Tawk script tag present: <strong>{String(client.tawk)}</strong></li>
        <li>Global CSS present: <strong>{String(client.css)}</strong></li>
      </ul>
      <p className="muted">Open this on Production to verify the real site.</p>
    </main>
  );
}
