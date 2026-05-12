'use client';

import { useAppStore } from '@/stores/app_store';
import { Button } from '@/components/ui/button';
import { Menu, X } from 'lucide-react';

export function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useAppStore();

  const navItems = [
    { label: 'Dashboard', href: '/' },
    { label: 'Projects', href: '/projects' },
    { label: 'Jobs', href: '/jobs' },
    { label: 'Prompts', href: '/prompts' },
    { label: 'Settings', href: '/settings' },
    { label: 'Render', href: '/render' },
  ];

  return (
    <aside
      className={`fixed left-0 top-0 z-40 h-screen transition-transform ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } w-64 border-r bg-background`}
    >
      <div className="flex h-14 items-center border-b px-4">
        <span className="text-lg font-bold">AI Video Platform</span>
        <Button
          variant="ghost"
          size="sm"
          className="ml-auto"
          onClick={toggleSidebar}
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
      <nav className="space-y-1 p-4">
        {navItems.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="block rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
          >
            {item.label}
          </a>
        ))}
      </nav>
    </aside>
  );
}
