import { Table, TableBody, TableCell, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

const mockData = [
  { id: 'job_123', type: 'Render', status: 'completed', duration: '45s', timestamp: '2024-01-15 10:30' },
  { id: 'job_124', type: 'TTS', status: 'failed', duration: '12s', timestamp: '2024-01-15 10:28' },
  { id: 'job_125', type: 'Image Gen', status: 'completed', duration: '23s', timestamp: '2024-01-15 10:25' },
  { id: 'job_126', type: 'Pipeline', status: 'running', duration: '1m 12s', timestamp: '2024-01-15 10:20' },
  { id: 'job_127', type: 'Render', status: 'queued', duration: '-', timestamp: '2024-01-15 10:15' },
];

export function AnalyticsTable() {
  return (
    <div className="rounded-md border border-gray-800 overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow className="border-gray-800 hover:bg-transparent">
            <TableHeader className="text-gray-400 text-xs">ID</TableHeader>
            <TableHeader className="text-gray-400 text-xs">Type</TableHeader>
            <TableHeader className="text-gray-400 text-xs">Status</TableHeader>
            <TableHeader className="text-gray-400 text-xs">Duration</TableHeader>
            <TableHeader className="text-gray-400 text-xs">Timestamp</TableHeader>
          </TableRow>
        </TableHeader>
        <TableBody>
          {mockData.map((row) => (
            <TableRow key={row.id} className="border-gray-800">
              <TableCell className="font-mono text-xs text-blue-400">{row.id}</TableCell>
              <TableCell className="text-xs text-white">{row.type}</TableCell>
              <TableCell>
                <Badge 
                  variant="outline" 
                  className={`text-[10px] ${
                    row.status === 'completed' ? 'border-green-900 text-green-400 bg-green-950/30' :
                    row.status === 'failed' ? 'border-red-900 text-red-400 bg-red-950/30' :
                    row.status === 'running' ? 'border-yellow-900 text-yellow-400 bg-yellow-950/30' :
                    'border-gray-700 text-gray-400 bg-gray-950/30'
                  }`}
                >
                  {row.status}
                </Badge>
              </TableCell>
              <TableCell className="text-xs text-gray-300">{row.duration}</TableCell>
              <TableCell className="text-xs text-gray-500">{row.timestamp}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
