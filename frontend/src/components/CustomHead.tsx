'use client';

import Head from 'next/head';

export default function CustomHead() {
  return (
    <Head>
      <link rel="icon" href="/icon.svg" />
      <link rel="apple-touch-icon" href="/icon.svg" />
      <meta name="theme-color" content="#65451F" />
    </Head>
  );
}