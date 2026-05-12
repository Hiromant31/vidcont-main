"""Prompts schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PromptPack(BaseModel):
    """Prompt pack model."""
    id: str
    name: str
    type: str
    genre: str = "general"
    style: str = "narrative"
    version: str = "1.0"
    prompts: List[Dict[str, Any]] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None


class PromptPackCreate(BaseModel):
    """Schema for creating a prompt pack."""
    name: str
    type: str = "story"
    genre: str = "general"
    style: str = "narrative"
    version: str = "1.0"
    prompts: List[Dict[str, Any]] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)


class PromptPackUpdate(BaseModel):
    """Schema for updating a prompt pack."""
    name: Optional[str] = None
    type: Optional[str] = None
    genre: Optional[str] = None
    style: Optional[str] = None
    version: Optional[str] = None
    prompts: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[str]] = None
