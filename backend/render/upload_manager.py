"""
Upload Manager - Handles asset upload to Colab server
"""

import os
from typing import List, Dict, Any
from .colab_client import ColabClient


class UploadManager:
    """Manages upload of assets to Colab render server"""

    def __init__(self, colab_client: ColabClient):
        self.colab_client = colab_client

    def upload_assets(self, colab_url: str, files: List[str]) -> Dict[str, List[str]]:
        """
        Upload assets (images, audio, subtitles, manifest) to Colab server.

        INPUT:
        {
            "colab_url": string,
            "files": string[]  // paths to files
        }

        OUTPUT:
        {
            "uploaded_paths": string[]
        }

        RULES:
        - images
        - audio
        - subtitles
        - manifest.json
        """
        uploaded_paths = []

        for file_path in files:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            try:
                # Upload file to Colab server
                # In real implementation, this would use multipart/form-data
                upload_path = self._upload_file(colab_url, file_path)
                uploaded_paths.append(upload_path)
            except Exception as e:
                raise Exception(f"Failed to upload {file_path}: {str(e)}")

        return {"uploaded_paths": uploaded_paths}

    def _upload_file(self, colab_url: str, file_path: str) -> str:
        """
        Internal method to upload a single file.
        Returns the remote path on Colab server.
        """
        filename = os.path.basename(file_path)

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f)}
                response = self.colab_client.session.post(
                    f"{colab_url}/upload",
                    files=files,
                    timeout=300  # Longer timeout for file uploads
                )
                response.raise_for_status()
                result = response.json()
                return result.get("path", f"/assets/{filename}")
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def upload_render_pack(self, colab_url: str, render_payload: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Upload complete render pack including manifest and all assets.
        """
        all_files = []

        # Add assets
        all_files.extend(render_payload.get("assets", []))

        # Add subtitles file
        subtitles_file = render_payload.get("subtitles_file")
        if subtitles_file and subtitles_file not in all_files:
            all_files.append(subtitles_file)

        # Create temporary manifest file if needed
        manifest_data = render_payload.get("manifest_file")
        if manifest_data:
            import json
            import tempfile
            temp_manifest = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.json',
                delete=False
            )
            json.dump(manifest_data, temp_manifest)
            temp_manifest.close()
            all_files.append(temp_manifest.name)

        return self.upload_assets(colab_url, all_files)
