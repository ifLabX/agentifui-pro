import { Geist, Geist_Mono, Inter, Playfair_Display } from "next/font/google";

export const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
  preload: true,
});

export const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
  preload: true,
});

export const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "optional",
  preload: false,
});

export const playfairDisplay = Playfair_Display({
  variable: "--font-serif",
  subsets: ["latin"],
  display: "optional",
  preload: false,
});
