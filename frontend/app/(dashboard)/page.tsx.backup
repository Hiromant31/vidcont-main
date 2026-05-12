import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ConnectionStatus } from '@/components/realtime/connection_status';
import { GenerateVideoPanel } from '@/components/generate/generate_video_panel';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <ConnectionStatus />
      </div>

      {/* Generate Video Panel - главная функция */}
      <GenerateVideoPanel />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Projects</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/projects" className="text-2xl font-bold hover:underline">
              View Projects →
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Jobs</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/jobs" className="text-2xl font-bold hover:underline">
              View Jobs →
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Prompts</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/prompts" className="text-2xl font-bold hover:underline">
              Manage Prompts →
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">Settings</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/settings" className="text-2xl font-bold hover:underline">
              Configure →
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
