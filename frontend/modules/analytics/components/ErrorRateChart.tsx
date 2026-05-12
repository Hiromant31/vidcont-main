import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useJobsStats } from '../api/analytics_queries';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export function ErrorRateChart() {
  const { data: jobs } = useJobsStats();

  if (!jobs) return null;

  // Mock time series data based on current stats for demonstration
  const errorData = [
    { time: '00:00', errors: Math.floor(jobs.failed * 0.1) },
    { time: '04:00', errors: Math.floor(jobs.failed * 0.2) },
    { time: '08:00', errors: Math.floor(jobs.failed * 0.3) },
    { time: '12:00', errors: Math.floor(jobs.failed * 0.6) },
    { time: '16:00', errors: Math.floor(jobs.failed * 0.8) },
    { time: '20:00', errors: jobs.failed },
  ];

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-white">Error Rate Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={errorData}>
              <XAxis dataKey="time" tick={{ fill: '#9ca3af', fontSize: 10 }} />
              <YAxis tick={{ fill: '#9ca3af', fontSize: 10 }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '6px' }}
              />
              <Line type="monotone" dataKey="errors" stroke="#ef4444" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
