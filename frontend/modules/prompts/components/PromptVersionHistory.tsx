import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { usePromptVersions } from '../hooks/usePromptVersions';
import { Badge } from '@/components/ui/badge';
import { Clock } from 'lucide-react';

interface PromptVersionHistoryProps {
  templateId: string;
}

export function PromptVersionHistory({ templateId }: PromptVersionHistoryProps) {
  const { versions, isLoading } = usePromptVersions(templateId);

  if (isLoading) {
    return (
      <div className="p-4 text-center text-gray-500">
        Loading version history...
      </div>
    );
  }

  if (versions.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        No version history available.
      </div>
    );
  }

  return (
    <div className="rounded border border-gray-800 overflow-hidden">
      <div className="flex items-center gap-2 p-3 bg-gray-900/50 border-b border-gray-800">
        <Clock className="h-4 w-4 text-gray-400" />
        <h3 className="text-sm font-semibold text-white">Version History</h3>
      </div>
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent">
            <TableHead className="text-gray-400">Version</TableHead>
            <TableHead className="text-gray-400">Date</TableHead>
            <TableHead className="text-gray-400">Author</TableHead>
            <TableHead className="text-gray-400">Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {[...versions].reverse().map((version) => (
            <TableRow key={version.id}>
              <TableCell className="font-mono">v{version.version}</TableCell>
              <TableCell>{new Date(version.created_at).toLocaleDateString()}</TableCell>
              <TableCell>{version.created_by || 'System'}</TableCell>
              <TableCell>
                <Badge variant={version.version === versions.length ? "default" : "outline"}>
                  {version.version === versions.length ? "Current" : "Archived"}
                </Badge>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
