import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';

/**
 * Metadata for the application.
 */
export const metadata: Metadata = {
  title: 'PhD Progress Tracker',
  description: 'Track your PhD tasks and milestones',
};

/**
 * Root layout component with Header.
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="bg-gray-50 min-h-screen">
        <Header />
        <main className="pt-16 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
