import { create } from 'zustand';
import type { Job } from '@/types';
import { websocketService } from '@/services/websocket/service';

interface JobStore {
  jobs: Job[];
  activeJob: Job | null;
  setJobs: (jobs: Job[]) => void;
  addJob: (job: Job) => void;
  updateJob: (jobId: string, updates: Partial<Job>) => void;
  removeJob: (jobId: string) => void;
  setActiveJob: (job: Job | null) => void;
}

export const useJobStore = create<JobStore>((set, get) => {
  // Подписка на WebSocket при создании стора
  const setupSubscriptions = () => {
    websocketService.on('job_progress', (message) => {
      const { job_id, progress, current_stage } = message.data;
      get().updateJob(job_id, { progress, current_stage });
    });

    websocketService.on('job_completed', (message) => {
      const { job_id } = message.data;
      get().updateJob(job_id, { status: 'completed', progress: 100 });
    });

    websocketService.on('job_failed', (message) => {
      const { job_id, error } = message.data;
      get().updateJob(job_id, { status: 'failed', errors: [error] });
    });

    websocketService.on('stage_completed', (message) => {
      const { job_id, stage_name } = message.data;
      console.log(`Stage ${stage_name} completed for job ${job_id}`);
    });
  };

  setupSubscriptions();

  return {
    jobs: [],
    activeJob: null,

    setJobs: (jobs) => set({ jobs }),

    addJob: (job) => set((state) => ({
      jobs: [...state.jobs, job],
    })),

    updateJob: (jobId, updates) => set((state) => ({
      jobs: state.jobs.map((j) =>
        j.job_id === jobId ? { ...j, ...updates } : j
      ),
      activeJob: state.activeJob?.job_id === jobId
        ? { ...state.activeJob, ...updates }
        : state.activeJob,
    })),

    removeJob: (jobId) => set((state) => ({
      jobs: state.jobs.filter((j) => j.job_id !== jobId),
    })),

    setActiveJob: (job) => set({ activeJob: job }),
  };
});
