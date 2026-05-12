import { Card, CardContent } from '@/components/ui/card';
import { useAnalyticsStore } from '../stores/analytics_store';
import { AnalyticsOverviewCards } from './AnalyticsOverviewCards';
import { PipelineStatsChart } from './PipelineStatsChart';
import { JobsStatsChart } from './JobsStatsChart';
import { SystemLoadChart } from './SystemLoadChart';
import { AnalyticsFilters } from './AnalyticsFilters';
import { AnalyticsLoadingState } from './AnalyticsLoadingState';
import { EmptyAnalyticsState } from './EmptyAnalyticsState';
import { useAnalytics } from '../hooks/useAnalytics';

export function AnalyticsDashboard() {
  const { isLoading } = useAnalytics();
  const selectedTab = useAnalyticsStore((state) => state.selectedTab);

  if (isLoading) return <AnalyticsLoadingState />;

  return (
    <div className="space-y-6 p-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Analytics Dashboard</h1>
          <p className="text-sm text-gray-400">Real-time system performance monitoring</p>
        </div>
        <AnalyticsFilters />
      </div>

      <AnalyticsOverviewCards />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PipelineStatsChart />
        <JobsStatsChart />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <SystemLoadChart />
        </div>
        <div className="space-y-4">
          {/* Placeholder for ErrorRateChart or CostAnalysisPanel */}
          <Card className="bg-gray-900 border-gray-800 h-full flex items-center justify-center">
            <CardContent className="text-center text-gray-500">
              <p className="text-sm">Additional charts coming soon</p>
              <p className="text-xs mt-1">Error trends & cost analysis</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
