import type { Metadata } from "next";
import Link from "next/link";
import "@fontsource/epilogue/400.css";
import "@fontsource/epilogue/500.css";
import "@fontsource/epilogue/700.css";
import "@fontsource/epilogue/900.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "./globals.css";
import { ThemeToggle } from "@/components/ThemeToggle";

export const metadata: Metadata = {
  title: "CVthèque · ERP RH",
  description: "ERP RH du TP Club GenAI : consulter les profils et leurs CV.",
};

// Applique le thème choisi avant le premier rendu, pour éviter un flash clair/sombre.
const themeScript = `try{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <header className="topbar">
          <div className="wrap topbar-inner">
            <Link href="/" className="brand">
              <span className="brand-mark" aria-hidden="true" />
              <span className="brand-name">CVthèque</span>
              <span className="brand-tag">ERP RH</span>
            </Link>
            <ThemeToggle />
          </div>
        </header>
        <main className="wrap">{children}</main>
        <footer className="wrap footer">
          Données fictives · TP Club GenAI · Intégrer l&apos;IA dans son SDLC
        </footer>
      </body>
    </html>
  );
}
