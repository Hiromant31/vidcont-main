'use client';

import { useAppStore } from '@/stores/app_store';
import { Button } from '@/components/ui/button';
import { Menu } from 'lucide-react';

export function TopBar() {
  const { toggleSidebar } = useAppStore();

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center border-b bg-background px-4">
      <Button variant="ghost" size="sm" onClick={toggleSidebar} className="mr-4">
        <Menu className="h-4 w-4" />
      </Button>
      <div className="flex flex-1 items-center justify-end space-x-4">
        <div className="text-sm text-muted-foreground">
          Connected to backend
        </div>
      </div>
    </header>
  );
}
