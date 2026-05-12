"""
Core system interfaces for AI video generation platform.
"""

from .stage_interface import StageInterface
from .storage_interface import StorageInterface

__all__ = ["StageInterface", "StorageInterface"]
