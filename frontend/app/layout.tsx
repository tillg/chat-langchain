import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Head from 'next/head';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Chat Till",
  description: "Chatbot for Till's Brainz",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body className={`${inter.className} h-full`}>
        <div
          className="flex flex-col h-full md:p-8"
          style={{ background: "rgb(38, 38, 41)" }}
        >
          {children}
        </div>
      </body>
    </html>
  );
}
