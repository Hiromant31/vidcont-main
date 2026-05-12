import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useSystemLoad } from '../api/analytics_queries';
import { detectAnomalies, getSystemHealthStatus } from '../utils/anomaly_detector';
import { cn } from '@/utils/cn';
import { Activity, AlertTriangle, CheckCircle, Server } from 'lucide-react';

export function SystemLoadChart() {
  const { data: load } = useSystemLoad();

  if (!load) return null;

  const anomalies = detectAnomalies(load);
  const healthStatus = getSystemHealthStatus(load);

  const metrics = [
    { label: 'CPU Usage', value: load.cpu_usage, unit: '%', color: 'bg-blue-500' },
    { label: 'Memory', value: load.memory_usage, unit: '%', color: 'bg-purple-500' },
    { label: 'Queue Size', value: load.queue_size, unit: 'jobs', color: 'bg-yellow-500' },
    { label: 'Throughput', value: load.throughput_per_min, unit: '/min', color: 'bg-green-500' },
  ];

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center gap-2">
          <Server className="h-5 w-5 text-gray-400" />
          <CardTitle className="text-sm font-medium text-white">System Load</CardTitle>
        </div>
        <div className={cn(
          "flex items-center gap-1 px-2 py-1 rounded text-xs font-medium",
          healthStatus === 'healthy' && "bg-green-900/30 text-green-400",
          healthStatus === 'degraded' && "bg-yellow-900/30 text-yellow-400",
          healthStatus === 'critical' && "bg-red-900/30 text-red-400"
        )}>
          {healthStatus === 'healthy' ? <CheckCircle className="h-3 w-3" /> : <AlertTriangle className="h-3 w-3" />}
          {healthStatus.toUpperCase()}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {metrics.map((metric) => (
          <div key={metric.label} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-gray-400">{metric.label}</span>
              <span className="text-white font-medium">{metric.value} {metric.unit}</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
              <div 
                className={cn("h-full transition-all duration-500", metric.color)}
                style={{ width: `${Math.min(metric.value, 100)}%` }}
              />
            </div>
          </div>
        ))}

        {anomalies.length > 0 && (
          <div className="mt-4 p-3 bg-red-950/30 border border-red-900/50 rounded">
            <div className="flex items-center gap-2 text-red-400 text-xs font-semibold mb-2">
              <AlertTriangle className="h-3 w-3" />
              Alerts ({anomalies.length})
            </div>
            <ul className="space-y-1">
              {anomalies.map((anomaly, idx) => (
                <li key={idx} className="text-[10px] text-red-300">
                  {anomaly.message}
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
