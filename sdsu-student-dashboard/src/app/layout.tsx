import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "SDSU Student Experience Dashboard",
  description: "Interactive dashboard for visualizing SDSU student living experiences, mental health, and campus community data. Help improve student life through data-driven insights.",
  keywords: ["SDSU", "student experience", "mental health", "campus life", "data visualization", "survey"],
  authors: [{ name: "San Diego State University" }],
  robots: "noindex, nofollow", // Since this is a demo
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} antialiased min-h-full bg-gray-50`}>
        {children}
      </body>
    </html>
  );
}
