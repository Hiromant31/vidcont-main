import { create } from 'zustand';
import type { Job } from '@/types';

interface JobState {
  jobs: Job[];
  activeJob: Job | null;
  setJobs: (jobs: Job[]) => void;
  addJob: (job: Job) => void;
  updateJob: (jobId: string, updates: Partial<Job>) => void;
  setActiveJob: (job: Job | null) => void;
  removeJob: (jobId: string) => void;
}

export const useJobStore = create<JobState>((set) => ({
  jobs: [],
  activeJob: null,

  setJobs: (jobs) => set({ jobs }),

  addJob: (job) =>
    set((state) => ({
      jobs: [...state.jobs, job],
    })),

  updateJob: (jobId, updates) =>
    set((state) => ({
      jobs: state.jobs.map((job) =>
        job.job_id === jobId ? { ...job, ...updates } : job
      ),
      activeJob:
        state.activeJob?.job_id === jobId
          ? { ...state.activeJob, ...updates }
          : state.activeJob,
    })),

  setActiveJob: (job) => set({ activeJob: job }),

  removeJob: (jobId) =>
    set((state) => ({
      jobs: state.jobs.filter((job) => job.job_id !== jobId),
      activeJob: state.activeJob?.job_id === jobId ? null : state.activeJob,
    })),
}));
