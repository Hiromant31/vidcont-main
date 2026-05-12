import { useSystemLoad as useSystemLoadQuery } from '../api/analytics_queries';

export const useSystemLoad = () => {
  return useSystemLoadQuery();
};
