'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { projectsApi } from '@/services/api/projects';
import { pipelineApi, type GenerateVideoRequest } from '@/services/api/pipeline';
import type { PipelineStatus } from '@/types';

interface StageBadgeProps {
  stage: { name: string; status: string; progress?: number; error?: string };
}

function StageBadge({ stage }: StageBadgeProps) {
  const statusColors: Record<string, string> = {
    pending: 'bg-gray-500',
    running: 'bg-blue-500 animate-pulse',
    completed: 'bg-green-500',
    failed: 'bg-red-500',
    skipped: 'bg-gray-300',
  };

  return (
    <div className="flex items-center gap-2">
      <Badge className={statusColors[stage.status] || 'bg-gray-500'}>
        {stage.status}
      </Badge>
      <span className="text-sm">{stage.name.replace('_', ' ')}</span>
      {stage.progress !== undefined && (
        <span className="text-xs text-gray-500">{Math.round(stage.progress)}%</span>
      )}
      {stage.error && (
        <span className="text-xs text-red-500" title={stage.error}>⚠️</span>
      )}
    </div>
  );
}

export function GenerateVideoPanel() {
  const queryClient = useQueryClient();
  const [showProgress, setShowProgress] = useState(false);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus | null>(null);

  const [formData, setFormData] = useState({
    idea: '',
    duration: 60,
    orientation: 'vertical' as const,
    quality: '720p' as const,
    episodes_count: 1,
    genre: 'general',
    style: 'cinematic',
  });

  // Mutation для создания проекта и запуска пайплайна
  const generateMutation = useMutation({
    mutationFn: async () => {
      // Сначала создаём проект
      const project = await projectsApi.create({
        name: `Video: ${formData.idea.slice(0, 30)}...`,
        description: formData.idea,
      });

      // Затем запускаем пайплайн
      const pipelineData: GenerateVideoRequest = {
        project_id: project.project_id,
        idea: formData.idea,
        duration: formData.duration,
        orientation: formData.orientation,
        quality: formData.quality,
        episodes_count: formData.episodes_count,
        genre: formData.genre,
        style: formData.style,
      };

      return await pipelineApi.run(pipelineData);
    },
    onSuccess: (data) => {
      setShowProgress(true);
      setCurrentJobId(data.job_id);
      setPipelineStatus(data as unknown as PipelineStatus);
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      alert('Pipeline started! Check progress below.');
    },
    onError: (error: any) => {
      alert(`Failed to start pipeline: ${error.message}`);
    },
  });

  // Polling для обновления статуса
  useState(() => {
    if (!showProgress || !currentJobId) return;

    const pollInterval = setInterval(async () => {
      try {
        const status = await pipelineApi.getStatus(currentJobId);
        setPipelineStatus(status as unknown as PipelineStatus);

        // Если пайплайн завершён или провален, останавливаем polling
        if (['completed', 'failed'].includes(status.status)) {
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 3000); // Обновление каждые 3 секунды

    return () => clearInterval(pollInterval);
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.idea.trim()) {
      alert('Please enter an idea');
      return;
    }
    generateMutation.mutate();
  };

  if (showProgress && pipelineStatus) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Pipeline Progress</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Overall Progress</span>
              <span>{Math.round(pipelineStatus.progress)}%</span>
            </div>
            <Progress value={pipelineStatus.progress} className="w-full" />
          </div>

          <div className="space-y-2">
            <h4 className="font-medium">Stages:</h4>
            {pipelineStatus.stages?.map((stage) => (
              <StageBadge key={stage.name} stage={stage} />
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => setShowProgress(false)}
              disabled={['running', 'pending'].includes(pipelineStatus.status)}
            >
              Close
            </Button>
            {pipelineStatus.status === 'completed' && (
              <Button onClick={() => window.location.href = '/jobs'}>
                View Result in Jobs
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Video</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="idea">Video Idea</Label>
            <Textarea
              id="idea"
              placeholder="Describe your video idea..."
              value={formData.idea}
              onChange={(e) => setFormData({ ...formData, idea: e.target.value })}
              rows={4}
              disabled={generateMutation.isPending}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="duration">Duration (seconds)</Label>
              <Input
                id="duration"
                type="number"
                min={15}
                max={300}
                value={formData.duration}
                onChange={(e) => setFormData({ ...formData, duration: parseInt(e.target.value) || 60 })}
                disabled={generateMutation.isPending}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="episodes">Episodes Count</Label>
              <Input
                id="episodes"
                type="number"
                min={1}
                max={10}
                value={formData.episodes_count}
                onChange={(e) => setFormData({ ...formData, episodes_count: parseInt(e.target.value) || 1 })}
                disabled={generateMutation.isPending}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="orientation">Orientation</Label>
              <Select
                value={formData.orientation}
                onValueChange={(value: any) => setFormData({ ...formData, orientation: value })}
                disabled={generateMutation.isPending}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="vertical">Vertical (9:16)</SelectItem>
                  <SelectItem value="horizontal">Horizontal (16:9)</SelectItem>
                  <SelectItem value="square">Square (1:1)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="quality">Quality</Label>
              <Select
                value={formData.quality}
                onValueChange={(value: any) => setFormData({ ...formData, quality: value })}
                disabled={generateMutation.isPending}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="720p">720p HD</SelectItem>
                  <SelectItem value="1080p">1080p Full HD</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="genre">Genre</Label>
              <Select
                value={formData.genre}
                onValueChange={(value: any) => setFormData({ ...formData, genre: value })}
                disabled={generateMutation.isPending}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="general">General</SelectItem>
                  <SelectItem value="drama">Drama</SelectItem>
                  <SelectItem value="comedy">Comedy</SelectItem>
                  <SelectItem value="action">Action</SelectItem>
                  <SelectItem value="documentary">Documentary</SelectItem>
                  <SelectItem value="educational">Educational</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="style">Style</Label>
              <Select
                value={formData.style}
                onValueChange={(value: any) => setFormData({ ...formData, style: value })}
                disabled={generateMutation.isPending}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cinematic">Cinematic</SelectItem>
                  <SelectItem value="cartoon">Cartoon</SelectItem>
                  <SelectItem value="realistic">Realistic</SelectItem>
                  <SelectItem value="anime">Anime</SelectItem>
                  <SelectItem value="minimalist">Minimalist</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={generateMutation.isPending || !formData.idea.trim()}
          >
            {generateMutation.isPending ? 'Starting Pipeline...' : '🎬 Generate Video'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
