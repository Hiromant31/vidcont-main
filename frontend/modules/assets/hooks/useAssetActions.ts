import { useDeleteAsset, useReuseAsset } from '../api/assets_queries';
import { useAssetsStore } from '../stores/assets_store';
import { useRouter } from 'next/navigation';

export const useAssetActions = () => {
  const router = useRouter();
  const { setSelectedAsset, togglePreview } = useAssetsStore();
  const deleteMutation = useDeleteAsset();
  const reuseMutation = useReuseAsset();

  const handleDelete = async (id: string) => {
    await deleteMutation.mutateAsync(id);
    if (useAssetsStore.getState().selectedAssetId === id) {
      setSelectedAsset(null);
      togglePreview(null);
    }
  };

  const handleReuse = async (assetId: string, targetType: string, targetId: string) => {
    await reuseMutation.mutateAsync({
      assetId,
      target: { type: targetType, id: targetId },
    });
    router.push(`/projects/${targetId}/scenes`);
  };

  const handleDownload = async (id: string, url: string) => {
    window.open(url, '_blank');
  };

  return {
    deleteAsset: handleDelete,
    reuseAsset: handleReuse,
    downloadAsset: handleDownload,
    isDeleting: deleteMutation.isPending,
    isReusing: reuseMutation.isPending,
  };
};
