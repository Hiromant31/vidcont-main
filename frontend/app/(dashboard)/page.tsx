import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ConnectionStatus } from '@/components/realtime/connection_status';
import { GenerateVideoPanel } from '@/components/generate/generate_video_panel';
import { Video, Briefcase, List, Settings } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">
                AI Video Platform
              </h1>
              <p className="mt-2 text-lg text-gray-600 dark:text-gray-400">
                Create stunning videos from text prompts using advanced AI models
              </p>
            </div>
            <ConnectionStatus />
          </div>
          
          {/* Main Call to Action */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
            <h2 className="text-3xl font-semibold text-gray-900 dark:text-gray-100 mb-6">
              Generate Your First Video
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Simply describe your video idea and our AI will handle the rest - from script generation to final render
            </p>
            <div className="w-full"><GenerateVideoPanel /> </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Projects */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <Video className="h-5 w-5 text-blue-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Projects
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Manage and organize your video projects
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/projects" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                View Projects
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>

          {/* Jobs */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <Briefcase className="h-5 w-5 text-green-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Jobs
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Monitor and manage your rendering jobs
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/jobs" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                View Jobs
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>

          {/* Prompts */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <List className="h-5 w-5 text-purple-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Prompts
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Create and reuse AI prompts for consistent results
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/prompts" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                Manage Prompts
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>

          {/* Settings */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <Settings className="h-5 w-5 text-gray-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Settings
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Configure your AI models and preferences
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/settings" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                Configure
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>

          {/* Render */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <Video className="h-5 w-5 text-indigo-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Render
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Monitor real-time rendering progress and outputs
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/render" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                View Render Queue
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>

          {/* Analytics */}
          <Card className="bg-white dark:bg-gray-800 hover:shadow-xl transition-shadow duration-300 border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3 mb-4">
                <Settings className="h-5 w-5 text-yellow-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Analytics
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Track performance and usage metrics
              </p>
            </CardHeader>
            <CardContent>
              <Link href="/analytics" className="w-full inline-flex items-center justify-between text-sm font-medium text-primary-foreground hover:text-primary/90 dark:hover:text-primary/80">
                View Analytics
                <span className="ml-2">→</span>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
