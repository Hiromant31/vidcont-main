"""Assets API Routes"""
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from typing import Optional, List
from api.schemas.asset_schema import (
    AssetResponse, AssetUsageResponse, ReuseAssetRequest, DeleteAssetResponse
)
from assets.asset_manager import AssetManager

router = APIRouter()
asset_manager = AssetManager()


@router.get("", response_model=List[AssetResponse], tags=["Assets"])
@router.get("/", response_model=List[AssetResponse], tags=["Assets"])
async def get_assets(
    type: Optional[str] = Query(None, alias="type", description="Filter by asset type"),
    status: Optional[str] = Query(None, description="Filter by status (processing/ready/failed)"),
    search: Optional[str] = Query(None, description="Search by name or ID")
):
    """Get all assets with optional filters."""
    try:
        return asset_manager.get_all(
            asset_type=type,
            status=status,
            search=search
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get assets: {str(e)}")


@router.get("/{asset_id}", response_model=AssetResponse, tags=["Assets"])
async def get_asset(asset_id: str):
    """Get asset by ID."""
    try:
        asset = asset_manager.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
        return asset
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asset: {str(e)}")


@router.delete("/{asset_id}", response_model=DeleteAssetResponse, tags=["Assets"])
async def delete_asset(asset_id: str):
    """Delete an asset."""
    try:
        result = asset_manager.delete(asset_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
        return DeleteAssetResponse(message="Asset deleted successfully", asset_id=asset_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete asset: {str(e)}")


@router.post("/reuse", response_model=AssetResponse, tags=["Assets"])
async def reuse_asset(request: ReuseAssetRequest):
    """Reuse an existing asset."""
    try:
        asset = asset_manager.reuse(request.asset_id, request.target_entity)
        if not asset:
            raise HTTPException(status_code=404, detail=f"Asset '{request.asset_id}' not found")
        return asset
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reuse asset: {str(e)}")


@router.get("/{asset_id}/usage", response_model=List[AssetUsageResponse], tags=["Assets"])
async def get_asset_usage(asset_id: str):
    """Get usage history of an asset."""
    try:
        asset = asset_manager.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
        return asset_manager.get_usage(asset_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asset usage: {str(e)}")


@router.get("/{asset_id}/download", tags=["Assets"])
async def download_asset(asset_id: str):
    """Download an asset file."""
    try:
        file_path = asset_manager.get_download_path(asset_id)
        if not file_path:
            raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
        # В реальном приложении — FileResponse с реальным файлом
        return {"message": "Download endpoint ready", "file_path": file_path, "asset_id": asset_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download asset: {str(e)}")
