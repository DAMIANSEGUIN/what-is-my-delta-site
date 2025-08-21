import "../styles/globals.css";
import Script from "next/script";

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      {/* Load any site JS from public/ via absolute path */}
      <Script strategy="afterInteractive" src="/assets/app.js" />
      {/* Tawk chat */}
      <Script id="tawk-embed" strategy="afterInteractive" src="https://embed.tawk.to/68a767d97ebce11927982120/1j36uravb" />
    </>
  );
}
