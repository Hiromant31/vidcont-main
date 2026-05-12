"""
Stage interface - abstract base class for all stage implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class StageInterface(ABC):
    """
    Базовый интерфейс для всех stage-реализаций.
    Core system ТОЛЬКО вызывает этот метод, НЕ знает реализацию.
    """
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет этап pipeline.
        
        INPUT:
            context: dict с данными для этого stage
            
        OUTPUT:
            dict с результатами выполнения
            
        RAISES:
            Exception при ошибке (будет поймана в stage_executor)
        """
        pass
    
    @property
    @abstractmethod
    def stage_name(self) -> str:
        """
        Уникальное имя этапа.
        
        Должно соответствовать одному из значений в STAGES списке.
        """
        pass
