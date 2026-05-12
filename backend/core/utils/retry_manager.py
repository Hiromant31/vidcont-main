"""
Retry manager for handling stage execution retries.
"""

from typing import Dict

from ..models import StageRun


class RetryManager:
    """
    Менеджер для управления повторными попытками выполнения stages.
    
    Использует exponential backoff стратегию для задержек между попытками.
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        """
        Инициализирует RetryManager.
        
        Args:
            max_retries: Максимальное количество попыток
            base_delay: Базовая задержка (секунды), используется exponential backoff
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def should_retry(self, stage_run: StageRun) -> Dict[str, any]:
        """
        Определяет, нужно ли повторить выполнение stage.
        
        Args:
            stage_run: StageRun с status="failed"
            
        Returns:
            {
                "retry": bool,
                "delay_seconds": float
            }
            
        Logic:
            - if retry_count < max_retries: retry=True
            - delay = base_delay * (2 ^ retry_count)
        """
        if stage_run.retry_count < self.max_retries:
            # Exponential backoff: delay = base_delay * 2^retry_count
            delay_seconds = self.base_delay * (2 ** stage_run.retry_count)
            return {
                "retry": True,
                "delay_seconds": delay_seconds
            }
        else:
            return {
                "retry": False,
                "delay_seconds": 0.0
            }
    
    def get_retry_count(self, stage_run: StageRun) -> int:
        """
        Возвращает текущее количество попыток для stage run.
        
        Args:
            stage_run: StageRun объект
            
        Returns:
            Количество попыток
        """
        return stage_run.retry_count
    
    def get_max_retries(self) -> int:
        """
        Возвращает максимальное количество попыток.
        
        Returns:
            Максимальное количество retry попыток
        """
        return self.max_retries
