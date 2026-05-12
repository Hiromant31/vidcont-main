import { SystemLoadMetrics } from '../types/analytics_types';

interface Anomaly {
  type: 'high_cpu' | 'high_memory' | 'queue_bottleneck' | 'low_throughput';
  severity: 'warning' | 'critical';
  message: string;
  value: number;
  threshold: number;
}

export const detectAnomalies = (load: SystemLoadMetrics): Anomaly[] => {
  const anomalies: Anomaly[] = [];

  if (load.cpu_usage > 85) {
    anomalies.push({
      type: 'high_cpu',
      severity: load.cpu_usage > 95 ? 'critical' : 'warning',
      message: `High CPU usage detected: ${load.cpu_usage}%`,
      value: load.cpu_usage,
      threshold: 85,
    });
  }

  if (load.memory_usage > 90) {
    anomalies.push({
      type: 'high_memory',
      severity: load.memory_usage > 95 ? 'critical' : 'warning',
      message: `High memory usage detected: ${load.memory_usage}%`,
      value: load.memory_usage,
      threshold: 90,
    });
  }

  if (load.queue_size > 100) {
    anomalies.push({
      type: 'queue_bottleneck',
      severity: load.queue_size > 200 ? 'critical' : 'warning',
      message: `Queue bottleneck detected: ${load.queue_size} jobs pending`,
      value: load.queue_size,
      threshold: 100,
    });
  }

  if (load.throughput_per_min < 5 && load.queue_size > 10) {
    anomalies.push({
      type: 'low_throughput',
      severity: 'warning',
      message: `Low throughput detected: ${load.throughput_per_min} jobs/min`,
      value: load.throughput_per_min,
      threshold: 5,
    });
  }

  return anomalies;
};

export const getSystemHealthStatus = (load: SystemLoadMetrics): 'healthy' | 'degraded' | 'critical' => {
  const anomalies = detectAnomalies(load);
  const criticalCount = anomalies.filter(a => a.severity === 'critical').length;

  if (criticalCount > 0) return 'critical';
  if (anomalies.length > 0) return 'degraded';
  return 'healthy';
};
