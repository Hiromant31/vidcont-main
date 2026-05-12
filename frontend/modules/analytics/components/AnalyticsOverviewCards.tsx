import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAnalytics } from '../hooks/useAnalytics';
import { calculateSuccessRate, formatMetricValue } from '../utils/metrics_calculator';
import { Activity, CheckCircle, AlertTriangle, Clock, DollarSign, Layers } from 'lucide-react';

export function AnalyticsOverviewCards() {
  const { overview, jobs, pipeline, render } = useAnalytics();

  if (!overview) return null;

  const successRate = jobs ? calculateSuccessRate(jobs.completed, jobs.total_jobs) : 0;
  const failureRate = jobs ? calculateSuccessRate(jobs.failed, jobs.total_jobs) : 0;

  const cards = [
    {
      title: 'Total Jobs',
      value: overview.total_jobs.toLocaleString(),
      icon: Layers,
      color: 'text-blue-500',
      subtext: `${jobs?.queued || 0} queued`,
    },
    {
      title: 'Success Rate',
      value: formatMetricValue(successRate, 'percent'),
      icon: CheckCircle,
      color: 'text-green-500',
      subtext: `${failureRate}% failed`,
    },
    {
      title: 'Total Renders',
      value: overview.total_renders.toLocaleString(),
      icon: Activity,
      color: 'text-purple-500',
      subtext: render ? `${Math.round(render.avg_render_time_sec)}s avg` : '',
    },
    {
      title: 'Avg Pipeline Time',
      value: pipeline ? formatMetricValue(pipeline.avg_duration_sec, 'time') : '--',
      icon: Clock,
      color: 'text-yellow-500',
      subtext: pipeline ? `${pipeline.total_runs} runs` : '',
    },
    {
      title: 'Total Errors',
      value: overview.total_errors.toLocaleString(),
      icon: AlertTriangle,
      color: 'text-red-500',
      subtext: overview.total_errors > 0 ? 'Review required' : 'System healthy',
    },
    {
      title: 'Est. Cost',
      value: formatMetricValue(overview.estimated_cost_usd, 'currency'),
      icon: DollarSign,
      color: 'text-emerald-500',
      subtext: 'This period',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <Card key={card.title} className="bg-gray-900 border-gray-800">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs font-medium text-gray-400">{card.title}</CardTitle>
              <Icon className={`h-4 w-4 ${card.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-white">{card.value}</div>
              <p className="text-[10px] text-gray-500 mt-1">{card.subtext}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
