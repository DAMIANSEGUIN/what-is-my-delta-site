import Script from "next/script";

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <Script id="tawk-embed" strategy="afterInteractive" src="https://embed.tawk.to/68a767d97ebce11927982120/1j36uravb" />
    </>
  );
}
