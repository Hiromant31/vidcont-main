"""
Context builder for assembling stage execution contexts.
"""

from typing import Dict, Any, List

from ..interfaces import StorageInterface
from .event_logger import EventLogger


class ContextBuilder:
    """
    Строитель контекстов для выполнения stages.
    
    Собирает минимальный необходимый контекст для каждого этапа pipeline.
    """
    
    # Hardcoded dependencies mapping
    STAGE_DEPENDENCIES = {
        "story_generation": [],
        "character_extraction": ["story_generation"],
        "story_adaptation": ["story_generation", "character_extraction"],
        "storyboard_generation": ["story_adaptation"],
        "tts_generation": ["story_adaptation"],
        "subtitle_generation": ["tts_generation"],
        "character_render": ["character_extraction"],
        "scene_image_generation": ["storyboard_generation", "character_render"],
        "manifest_generation": ["scene_image_generation", "tts_generation"],
        "video_render": ["manifest_generation"],
        "metadata_generation": ["video_render"]
    }
    
    def __init__(self, storage: StorageInterface, event_logger: EventLogger):
        """
        Инициализирует ContextBuilder.
        
        Args:
            storage: StorageInterface instance
            event_logger: EventLogger instance
        """
        self._storage = storage
        self._event_logger = event_logger
    
    def build_context(self, job_id: str, stage_name: str) -> Dict[str, Any]:
        """
        Собирает минимальный контекст для выполнения stage.
        
        Args:
            job_id: ID задачи
            stage_name: имя этапа
            
        Returns:
            dict с ТОЛЬКО необходимыми данными для этого stage
            
        Rules:
            - НЕ передавать весь project
            - НЕ передавать данные других stages
            - ТОЛЬКО минимум для текущего stage
        """
        # Get the job to access project info
        from ..managers import JobManager
        job_manager = JobManager(self._storage)
        job = job_manager.get_job(job_id)
        
        # Get all previous stage runs for this job
        stage_runs = self._storage.get_stage_runs(job_id)
        
        # Build context with job info
        context = {
            "job_id": job_id,
            "project_id": job.project_id,
        }
        
        # Add outputs from dependent stages
        dependencies = self._get_stage_dependencies(stage_name)
        
        for dep_stage in dependencies:
            # Find the completed stage run for this dependency
            dep_run = None
            for run in stage_runs:
                if run.stage_name == dep_stage and run.status == "completed":
                    dep_run = run
                    break
            
            if dep_run and dep_run.output_data:
                # Add output data with stage-specific key
                context[f"{dep_stage}_output"] = dep_run.output_data
        
        # Stage-specific context enrichment
        context = self._enrich_context(context, stage_name)
        
        return context
    
    def _enrich_context(self, context: Dict[str, Any], stage_name: str) -> Dict[str, Any]:
        """
        Добавляет специфичные данные для конкретного этапа.
        
        Args:
            context: Базовый контекст
            stage_name: Имя этапа
            
        Returns:
            enriched context
        """
        # This is a placeholder for stage-specific enrichment logic
        # In a real implementation, this would fetch settings, templates, etc.
        
        # Example placeholders (would be fetched from settings block in real impl):
        if stage_name == "story_generation":
            context["prompt_template"] = "Generate a story..."
            context["settings"] = {}  # Would come from settings block
        
        elif stage_name == "character_extraction":
            context["extraction_config"] = {}  # Character extraction settings
        
        elif stage_name == "storyboard_generation":
            context["storyboard_config"] = {}  # Storyboard generation settings
        
        elif stage_name == "tts_generation":
            context["tts_config"] = {}  # TTS settings
        
        elif stage_name == "character_render":
            context["render_config"] = {}  # Character render settings
        
        elif stage_name == "scene_image_generation":
            context["image_settings"] = {}  # Image generation settings
        
        elif stage_name == "video_render":
            context["video_config"] = {}  # Video render settings
        
        elif stage_name == "metadata_generation":
            context["metadata_config"] = {}  # Metadata settings
        
        return context
    
    def _get_stage_dependencies(self, stage_name: str) -> List[str]:
        """
        Возвращает список stage_name, от которых зависит текущий stage.
        
        Args:
            stage_name: Имя этапа
            
        Returns:
            Список зависимых stage names
            
        Note:
            HARDCODED mapping зависимостей.
        """
        return self.STAGE_DEPENDENCIES.get(stage_name, [])
