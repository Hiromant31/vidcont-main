import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// Mock data for demonstration
const heatmapData = [
  { hour: '00', intensity: 0.2 }, { hour: '01', intensity: 0.1 }, { hour: '02', intensity: 0.1 },
  { hour: '03', intensity: 0.1 }, { hour: '04', intensity: 0.2 }, { hour: '05', intensity: 0.3 },
  { hour: '06', intensity: 0.4 }, { hour: '07', intensity: 0.6 }, { hour: '08', intensity: 0.8 },
  { hour: '09', intensity: 0.9 }, { hour: '10', intensity: 1.0 }, { hour: '11', intensity: 0.9 },
  { hour: '12', intensity: 0.8 }, { hour: '13', intensity: 0.7 }, { hour: '14', intensity: 0.8 },
  { hour: '15', intensity: 0.9 }, { hour: '16', intensity: 1.0 }, { hour: '17', intensity: 0.9 },
  { hour: '18', intensity: 0.7 }, { hour: '19', intensity: 0.6 }, { hour: '20', intensity: 0.5 },
  { hour: '21', intensity: 0.4 }, { hour: '22', intensity: 0.3 }, { hour: '23', intensity: 0.2 },
];

export function UsageHeatmap() {
  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader>
        <CardTitle className="text-sm font-medium text-white">Activity Heatmap</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-12 gap-1">
          {heatmapData.map((item) => (
            <div
              key={item.hour}
              className="h-8 rounded flex items-end justify-center pb-1 text-[9px] text-gray-400"
              style={{
                backgroundColor: `rgba(59, 130, 246, ${item.intensity})`,
              }}
              title={`${item.hour}:00 - ${Math.round(item.intensity * 100)}% activity`}
            >
              {item.hour}
            </div>
          ))}
        </div>
        <div className="mt-2 text-xs text-gray-500 text-center">
          Jobs activity by hour of day
        </div>
      </CardContent>
    </Card>
  );
}
