// components/Layout.tsx
import React from 'react';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="mb-8 p-4 bg-gray-100 rounded-lg shadow-md flex justify-around max-w-3xl mx-auto mt-4">
        <Link href="/" className="text-blue-600 hover:underline text-lg font-medium px-4 py-2 rounded-md hover:bg-blue-100 transition-colors">
          🏡 Home (Leaderboard)
        </Link>
        <Link href="/daily" className="text-blue-600 hover:underline text-lg font-medium px-4 py-2 rounded-md hover:bg-blue-100 transition-colors">
          🧮 Daily Verified Listings
        </Link>
        <Link href="/glengarry-index" className="text-blue-600 hover:underline text-lg font-medium px-4 py-2 rounded-md hover:bg-blue-100 transition-colors">
          📚 The Glengarry Index
        </Link>
      </nav>
      <main>
        {children}
      </main>
    </div>
  );
};

export default Layout;