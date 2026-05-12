"""Prompts management routes."""

from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from api.schemas.prompts import PromptPack, PromptPackCreate, PromptPackUpdate
from services.prompt_service import PromptService

router = APIRouter()

prompt_service = PromptService()


class PreviewPromptRequest(BaseModel):
    template_id: str
    variables: dict = {}


@router.get("/", response_model=List[PromptPack])
async def get_all_prompts():
    """Get all prompt packs."""
    return prompt_service.get_all_prompts()


@router.get("/{prompt_id}", response_model=PromptPack)
async def get_prompt(prompt_id: str):
    """Get a specific prompt pack by ID."""
    prompt = prompt_service.get_prompt_by_id(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt pack not found")
    return prompt


@router.post("/", response_model=PromptPack)
async def create_prompt(data: PromptPackCreate):
    """Create a new prompt pack."""
    return prompt_service.create_prompt(data)


@router.put("/{prompt_id}", response_model=PromptPack)
async def update_prompt(prompt_id: str, data: PromptPackUpdate):
    """Update an existing prompt pack."""
    prompt = prompt_service.update_prompt(prompt_id, data)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt pack not found")
    return prompt


@router.post("/preview", tags=["Prompts"])
async def preview_prompt(request: PreviewPromptRequest):
    """
    Preview a rendered prompt with variables substituted.
    """
    try:
        prompt = prompt_service.get_prompt_by_id(request.template_id)
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt pack not found")

        rendered = request.template_id
        variables_used = list(request.variables.keys())

        # Simple variable substitution
        if hasattr(prompt, 'prompts') and prompt.prompts:
            import json
            content = json.dumps(prompt.prompts)
            for key, value in request.variables.items():
                content = content.replace("{{" + key + "}}", str(value))
            rendered = content

        return {"rendered_prompt": rendered, "variables_used": variables_used}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")


@router.delete("/{prompt_id}")
async def delete_prompt(prompt_id: str):
    """Delete a prompt pack."""
    success = prompt_service.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt pack not found")
    return {"message": "Prompt pack deleted successfully"}
