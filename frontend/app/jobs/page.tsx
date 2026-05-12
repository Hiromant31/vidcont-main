'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { jobsApi } from '@/services/api/jobs';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ProgressBar } from '@/components/feedback/progress_bar';
import type { Job } from '@/types';

export default function JobsPage() {
  const queryClient = useQueryClient();

  const { data: jobs = [], isLoading, error, refetch } = useQuery({
    queryKey: ['jobs'],
    queryFn: () => jobsApi.getAll(),
    refetchInterval: 5000,
  });

  const stopMutation = useMutation({
    mutationFn: (id: string) => jobsApi.stop(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      alert('Job stopped successfully!');
    },
    onError: (error) => {
      alert(`Failed to stop job: ${error.message}`);
    },
  });

  const retryMutation = useMutation({
    mutationFn: (id: string) => jobsApi.retry(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      alert('Job restarted successfully!');
    },
    onError: (error) => {
      alert(`Failed to retry job: ${error.message}`);
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading jobs: {error.message}</div>;

  const getStatusColor = (status: Job['status']) => {
    switch (status) {
      case 'completed': return 'text-green-500';
      case 'failed': return 'text-red-500';
      case 'running': return 'text-blue-500';
      case 'paused': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Jobs</h1>
        <Button onClick={() => refetch()}>Refresh</Button>
      </div>

      <div className="space-y-4">
        {jobs.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">No jobs yet</p>
            </CardContent>
          </Card>
        ) : (
          jobs.map((job) => (
            <Card key={job.job_id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{job.job_id}</CardTitle>
                  <span className={`text-sm font-medium ${getStatusColor(job.status)}`}>
                    {job.status}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Progress</span>
                    <span>{job.progress}%</span>
                  </div>
                  <ProgressBar progress={job.progress} />
                  {job.current_stage && (
                    <p className="text-sm text-muted-foreground">
                      Stage: {job.current_stage}
                    </p>
                  )}
                </div>
                <div className="mt-4 flex space-x-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => {
                      alert(`Job Details:\nID: ${job.job_id}\nStatus: ${job.status}\nProgress: ${job.progress}%\nStage: ${job.current_stage || 'N/A'}`);
                    }}
                  >
                    View Details
                  </Button>
                  {job.status === 'running' && (
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => {
                        if (confirm('Are you sure you want to stop this job?')) {
                          stopMutation.mutate(job.job_id);
                        }
                      }}
                      disabled={stopMutation.isPending}
                    >
                      {stopMutation.isPending ? 'Stopping...' : 'Stop'}
                    </Button>
                  )}
                  {job.status === 'failed' && (
                    <Button 
                      variant="secondary" 
                      size="sm"
                      onClick={() => {
                        retryMutation.mutate(job.job_id);
                      }}
                      disabled={retryMutation.isPending}
                    >
                      {retryMutation.isPending ? 'Retrying...' : 'Retry'}
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
