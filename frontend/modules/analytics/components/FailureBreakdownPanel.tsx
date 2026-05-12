import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';

const mockFailures = [
  { type: 'Timeout Error', count: 12, percentage: 35 },
  { type: 'API Rate Limit', count: 8, percentage: 23 },
  { type: 'Invalid Prompt', count: 6, percentage: 17 },
  { type: 'Resource Exhausted', count: 5, percentage: 14 },
  { type: 'Network Error', count: 4, percentage: 11 },
];

export function FailureBreakdownPanel() {
  const total = mockFailures.reduce((acc, f) => acc + f.count, 0);

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-red-400" />
          <CardTitle className="text-sm font-medium text-white">Failure Breakdown</CardTitle>
        </div>
        <span className="text-xs text-gray-400">{total} total</span>
      </CardHeader>
      <CardContent className="space-y-3">
        {mockFailures.map((failure) => (
          <div key={failure.type} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-gray-300">{failure.type}</span>
              <span className="text-gray-400">{failure.count} ({failure.percentage}%)</span>
            </div>
            <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-red-500 rounded-full"
                style={{ width: `${failure.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
