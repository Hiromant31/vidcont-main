export type AssetType =
  | "image"
  | "audio"
  | "video"
  | "subtitle"
  | "thumbnail"
  | "temp";

export type AssetStatus =
  | "processing"
  | "ready"
  | "failed";

export interface Asset {
  id: string;
  project_id: string;
  job_id?: string;
  scene_id?: string;
  render_id?: string;
  type: AssetType;
  url: string;
  thumbnail_url?: string;
  status: AssetStatus;
  metadata?: Record<string, any>;
  size_bytes?: number;
  duration_sec?: number;
  created_at: string;
  name?: string;
}

export interface AssetUsage {
  id: string;
  asset_id: string;
  entity_type: "scene" | "job" | "render" | "project";
  entity_id: string;
  used_at: string;
  context?: string;
}

export interface AssetsFilters {
  type?: AssetType | "all";
  status?: AssetStatus | "all";
  search?: string;
  date_from?: string;
  date_to?: string;
}
