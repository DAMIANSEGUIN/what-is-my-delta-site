import Script from "next/script";

export default function Home() {
  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>What is my Delta?</h1>
      <p>Welcome to your Delta app. The Tidio chat widget is live in the corner.</p>
      <Script src="//code.tidio.co/n1vonfqtzyrhkdd2k4k9k9oq7ve6p7dv.js" strategy="afterInteractive" />
    </main>
  );
}
