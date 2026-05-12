import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useJobsStats } from '../api/analytics_queries';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#3b82f6', '#a855f7', '#22c55e', '#ef4444'];

export function JobsStatsChart() {
  const { data: jobs } = useJobsStats();

  if (!jobs) return null;

  const jobData = [
    { name: 'Queued', value: jobs.queued },
    { name: 'Running', value: jobs.running },
    { name: 'Completed', value: jobs.completed },
    { name: 'Failed', value: jobs.failed },
  ].filter(d => d.value > 0);

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-white">Job Distribution</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={jobData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={2}
                dataKey="value"
                 label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {jobData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '6px' }}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
          <div className="p-2 bg-gray-800 rounded">
            <div className="text-gray-400">Total Jobs</div>
            <div className="text-white font-bold">{jobs.total_jobs}</div>
          </div>
          <div className="p-2 bg-gray-800 rounded">
            <div className="text-gray-400">Avg Processing</div>
            <div className="text-white font-bold">{Math.round(jobs.avg_processing_time)}s</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
