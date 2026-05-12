'use client';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function RenderPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Render Queue</h1>

      <Card>
        <CardHeader>
          <CardTitle>No Active Renders</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-4">
            No render jobs in queue. Start a job from the Jobs page.
          </p>
          <Button>View Jobs</Button>
        </CardContent>
      </Card>
    </div>
  );
}
