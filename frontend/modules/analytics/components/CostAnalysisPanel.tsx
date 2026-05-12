import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAnalyticsOverview } from '../api/analytics_queries';
import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';

export function CostAnalysisPanel() {
  const { data: overview } = useAnalyticsOverview();

  if (!overview) return null;

  const costPerJob = overview.total_jobs > 0 ? overview.estimated_cost_usd / overview.total_jobs : 0;
  const trend = overview.estimated_cost_usd > 100 ? 'up' : 'down';

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center gap-2">
          <DollarSign className="h-5 w-5 text-emerald-400" />
          <CardTitle className="text-sm font-medium text-white">Cost Analysis</CardTitle>
        </div>
        {trend === 'up' ? (
          <TrendingUp className="h-4 w-4 text-red-400" />
        ) : (
          <TrendingDown className="h-4 w-4 text-green-400" />
        )}
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <div className="text-xs text-gray-400">Total Estimated Cost</div>
          <div className="text-xl font-bold text-white">${overview.estimated_cost_usd.toFixed(2)}</div>
        </div>
        <div className="grid grid-cols-2 gap-2 pt-2 border-t border-gray-800">
          <div>
            <div className="text-[10px] text-gray-500">Avg per Job</div>
            <div className="text-sm text-white">${costPerJob.toFixed(3)}</div>
          </div>
          <div>
            <div className="text-[10px] text-gray-500">Jobs Count</div>
            <div className="text-sm text-white">{overview.total_jobs}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
