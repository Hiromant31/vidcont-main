import { TimeSeriesData } from '../types/analytics_types';

export const formatChartDate = (timestamp: string): string => {
  const date = new Date(timestamp);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

export const formatChartTime = (timestamp: string): string => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

export const prepareTimeSeriesData = (data: TimeSeriesData[], smooth = true): TimeSeriesData[] => {
  if (!smooth || data.length < 3) return data;

  // Simple moving average smoothing
  return data.map((point, index) => {
    if (index === 0 || index === data.length - 1) return point;
    
    const prev = data[index - 1].value;
    const curr = point.value;
    const next = data[index + 1].value;
    
    return {
      ...point,
      value: (prev + curr + next) / 3,
    };
  });
};

export const getChartColor = (metric: string, value?: number): string => {
  if (value !== undefined) {
    if (value < 30) return '#ef4444'; // red
    if (value < 70) return '#eab308'; // yellow
    return '#22c55e'; // green
  }

  const colors: Record<string, string> = {
    cpu: '#3b82f6',
    memory: '#8b5cf6',
    queue: '#f59e0b',
    throughput: '#10b981',
    success: '#22c55e',
    failure: '#ef4444',
  };

  return colors[metric] || '#64748b';
};

export const formatTooltip = (label: string, value: number, type: 'count' | 'percent' | 'time'): string => {
  let formattedValue = value.toString();
  
  if (type === 'percent') {
    formattedValue = `${value.toFixed(1)}%`;
  } else if (type === 'time') {
    if (value >= 60) {
      formattedValue = `${(value / 60).toFixed(1)}m`;
    } else {
      formattedValue = `${value.toFixed(0)}s`;
    }
  }

  return `${label}: ${formattedValue}`;
};
