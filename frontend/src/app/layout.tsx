import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RippleWatch | AI Market-Change Agent for Small Businesses",
  description:
    "RippleWatch monitors public market shifts across Google Shopping, News, and Search via SerpApi, detects competitor moves, and generates human-approved low-cost action briefs backed by clickable evidence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#090d16] text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
