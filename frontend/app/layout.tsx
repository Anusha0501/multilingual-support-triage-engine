import './globals.css';
import type { ReactNode } from 'react';
export const metadata = { title: 'Triage Engine', description: 'Multilingual AI support triage SaaS' };
export default function RootLayout({ children }: { children: ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
