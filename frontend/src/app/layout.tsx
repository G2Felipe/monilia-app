import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Detector de Moniliasis en Cacao",
  description: "Aplicación para la detección de moniliasis en mazorcas de cacao usando inteligencia artificial",
  icons: {
    icon: [
      {
        url: "/images/ui/frijoles.png",
        sizes: "any",
        type: "image/png"
      }
    ],
    shortcut: [
      {
        url: "/images/ui/frijoles.png",
        type: "image/png"
      }
    ],
    apple: [
      {
        url: "/images/ui/frijoles.png",
        type: "image/png"
      }
    ]
  },
  manifest: "/manifest.json"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
