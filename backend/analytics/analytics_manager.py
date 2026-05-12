"""Analytics Manager - подсчёт метрик и статистики"""
import random
from datetime import datetime, timedelta
from typing import Optional
from api.schemas.analytics_schema import (
    AnalyticsOverview, PipelineMetrics, JobMetrics,
    RenderMetrics, SystemLoadMetrics, StageBreakdown
)


class AnalyticsManager:
    """Сбор и агрегация метрик для дашборда аналитики."""

    def __init__(self):
        self._start_time = datetime.utcnow()

    def get_overview(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> AnalyticsOverview:
        """Общая статистика по проектам, задачам, рендерам."""
        # TODO: заменить на реальные запросы из БД/стора
        return AnalyticsOverview(
            total_projects=random.randint(5, 20),
            total_jobs=random.randint(50, 200),
            total_renders=random.randint(20, 80),
            global_success_rate=round(random.uniform(70.0, 95.0), 1),
            total_errors=random.randint(0, 15),
            estimated_cost_usd=round(random.uniform(10.0, 150.0), 2)
        )

    def get_pipeline_stats(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        stage: Optional[str] = None
    ) -> PipelineMetrics:
        """Статистика пайплайна: успешность этапов, длительность."""
        stages = ["story", "characters", "scenes", "manifest", "render"]
        breakdown = {}
        for s in stages:
            breakdown[s] = StageBreakdown(
                success=random.randint(10, 50),
                failed=random.randint(0, 10),
                avg_time=round(random.uniform(5.0, 60.0), 1)
            )
        total_runs = sum(v.success + v.failed for v in breakdown.values())
        total_failed = sum(v.failed for v in breakdown.values())
        success_rate = ((total_runs - total_failed) / total_runs * 100) if total_runs > 0 else 0
        return PipelineMetrics(
            total_runs=total_runs,
            success_rate=round(success_rate, 1),
            failure_rate=round(100 - success_rate, 1),
            avg_duration_sec=round(random.uniform(30.0, 120.0), 1),
            stage_breakdown=breakdown
        )

    def get_jobs_stats(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status: Optional[str] = None
    ) -> JobMetrics:
        """Статистика задач: распределение по статусам."""
        return JobMetrics(
            total_jobs=random.randint(50, 200),
            queued=random.randint(0, 10),
            running=random.randint(1, 5),
            completed=random.randint(30, 150),
            failed=random.randint(0, 20),
            avg_processing_time=round(random.uniform(10.0, 90.0), 1)
        )

    def get_render_stats(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> RenderMetrics:
        """Статистика рендера:成功率, длительность, разрешения."""
        return RenderMetrics(
            total_renders=random.randint(20, 80),
            success_rate=round(random.uniform(75.0, 98.0), 1),
            avg_render_time_sec=round(random.uniform(60.0, 300.0), 1),
            avg_video_length_sec=round(random.uniform(15.0, 120.0), 1),
            resolution_distribution={
                "720p": random.randint(10, 40),
                "1080p": random.randint(5, 20),
                "480p": random.randint(0, 10)
            }
        )

    def get_system_load(self) -> SystemLoadMetrics:
        """Текущая загрузка системы (CPU, память, очередь, throughput)."""
        return SystemLoadMetrics(
            cpu_usage=round(random.uniform(10.0, 95.0), 1),
            memory_usage=round(random.uniform(20.0, 85.0), 1),
            active_connections=random.randint(1, 10),
            queue_size=random.randint(0, 15),
            throughput_per_min=round(random.uniform(0.5, 5.0), 1)
        )
