import { apiClient } from './client';
import type { Job, PipelineStatus } from '@/types';

export interface GenerateVideoRequest {
  project_id: string;
  idea: string;
  duration: number;
  orientation: 'vertical' | 'horizontal' | 'square';
  quality: '720p' | '1080p';
  episodes_count: number;
  genre?: string;
  style?: string;
}

export interface PipelineRunResponse {
  job_id: string;
  status: string;
  current_stage: string | null;
  stages: Array<{
    name: string;
    status: string;
    progress?: number;
    error?: string;
  }>;
  progress: number;
  created_at: string;
  updated_at: string;
}

export const pipelineApi = {
  async run(data: GenerateVideoRequest): Promise<PipelineRunResponse> {
    // Backend ожидает job_id, поэтому сначала создаём job через /api/jobs/start
    const jobResponse = await apiClient.post('/jobs/start', {
      project_id: data.project_id,
      idea: data.idea,
      genre: data.genre || 'general',
      style: data.style || 'cinematic',
      duration_target: data.duration,
      orientation: data.orientation,
      resolution: data.quality,
    });
    
    const jobId = jobResponse.data.job_id;
    
    // Затем запускаем пайплайн для этого job
    const pipelineResponse = await apiClient.post('/pipeline/run', {
      job_id: jobId,
      stages: null,
    });
    
    return {
      ...pipelineResponse.data,
      job_id: jobId,
    };
  },

  async getStatus(jobId: string): Promise<PipelineRunResponse> {
    const response = await apiClient.get(`/jobs/${jobId}`);
    return response.data;
  },

  async pause(jobId: string): Promise<{ status: string; job_id: string }> {
    const response = await apiClient.post(`/pipeline/pause?job_id=${jobId}`);
    return response.data;
  },

  async resume(jobId: string): Promise<{ status: string; job_id: string }> {
    const response = await apiClient.post(`/pipeline/resume?job_id=${jobId}`);
    return response.data;
  },
};
