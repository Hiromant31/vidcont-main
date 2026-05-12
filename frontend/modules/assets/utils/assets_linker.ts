import { Asset } from '../types/assets_types';

export const linkAssetToScene = (asset: Asset, sceneId: string): Partial<Asset> => ({
  scene_id: sceneId,
});

export const linkAssetToJob = (asset: Asset, jobId: string): Partial<Asset> => ({
  job_id: jobId,
});

export const linkAssetToRender = (asset: Asset, renderId: string): Partial<Asset> => ({
  render_id: renderId,
});

export const isAssetLinked = (asset: Asset): boolean => {
  return !!(asset.scene_id || asset.job_id || asset.render_id);
};

export const getLinkedEntityId = (asset: Asset): string | null => {
  return asset.scene_id || asset.job_id || asset.render_id || null;
};
