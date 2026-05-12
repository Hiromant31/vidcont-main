import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { usePipelineStats } from '../api/analytics_queries';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { getChartColor } from '../utils/chart_formatter';

export function PipelineStatsChart() {
  const { data: pipeline } = usePipelineStats();

  if (!pipeline || !pipeline.stage_breakdown) return null;

  const stageData = Object.entries(pipeline.stage_breakdown).map(([key, data]) => ({
    name: key.replace('_', ' ').toUpperCase(),
    success: data.success,
    failed: data.failed,
    avgTime: Math.round(data.avg_time),
  }));

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-white">Pipeline Stage Performance</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={stageData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 10 }} />
              <YAxis tick={{ fill: '#9ca3af', fontSize: 10 }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '6px' }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Bar dataKey="success" name="Success" radius={[4, 4, 0, 0]}>
                {stageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getChartColor('success')} />
                ))}
              </Bar>
              <Bar dataKey="failed" name="Failed" radius={[4, 4, 0, 0]}>
                {stageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getChartColor('failure')} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
          <div className="text-center p-2 bg-green-950/20 rounded border border-green-900/30">
            <div className="text-gray-400">Total Success</div>
            <div className="text-green-400 font-bold">{stageData.reduce((acc, d) => acc + d.success, 0)}</div>
          </div>
          <div className="text-center p-2 bg-red-950/20 rounded border border-red-900/30">
            <div className="text-gray-400">Total Failed</div>
            <div className="text-red-400 font-bold">{stageData.reduce((acc, d) => acc + d.failed, 0)}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
