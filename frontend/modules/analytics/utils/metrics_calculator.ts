import { PipelineMetrics, JobMetrics, RenderMetrics, SystemLoadMetrics } from '../types/analytics_types';

export const calculateSuccessRate = (success: number, total: number): number => {
  if (total === 0) return 0;
  return Math.round((success / total) * 100);
};

export const calculateTrend = (current: number, previous: number): number => {
  if (previous === 0) return current > 0 ? 100 : 0;
  return Math.round(((current - previous) / previous) * 100);
};

export const formatMetricValue = (value: number, type: 'count' | 'percent' | 'time' | 'currency'): string => {
  switch (type) {
    case 'percent':
      return `${value.toFixed(1)}%`;
    case 'time':
      if (value >= 3600) return `${(value / 3600).toFixed(1)}h`;
      if (value >= 60) return `${(value / 60).toFixed(1)}m`;
      return `${value.toFixed(0)}s`;
    case 'currency':
      return `$${value.toFixed(2)}`;
    default:
      return value.toLocaleString();
  }
};

export const aggregateStageMetrics = (metrics: PipelineMetrics) => {
  const stages = Object.entries(metrics.stage_breakdown);
  const totalSuccess = stages.reduce((acc, [, data]) => acc + data.success, 0);
  const totalFailed = stages.reduce((acc, [, data]) => acc + data.failed, 0);
  const avgTime = stages.reduce((acc, [, data]) => acc + data.avg_time, 0) / stages.length;

  return {
    totalSuccess,
    totalFailed,
    avgTime,
    successRate: calculateSuccessRate(totalSuccess, totalSuccess + totalFailed),
  };
};
