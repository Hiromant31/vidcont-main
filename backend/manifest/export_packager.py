"""
Export Packager

Формирует финальный пакет для рендеринга (RenderPack).
"""

from typing import List, Dict, Any, Optional
import json
from .render_schema import Manifest, RenderPack


class ExportPackager:
    """
    Упаковщик данных для экспорта на сервер рендеринга.
    
    Собирает манифест, ffmpeg скрипт и список ассетов
    в единый пакет для передачи на Colab.
    """
    
    def package_render(
        self,
        manifest: Manifest,
        ffmpeg_script: str,
        subtitles_file: Optional[str] = None
    ) -> RenderPack:
        """
        Упаковать все данные для рендеринга.
        
        Args:
            manifest: Объект манифеста
            ffmpeg_script: Скрипт команд ffmpeg
            subtitles_file: Путь к файлу субтитров (опционально)
            
        Returns:
            Объект RenderPack
        """
        # Собираем список всех необходимых ассетов
        assets_list = self._collect_assets(manifest)
        
        # Если файл субтитров не указан, создаём заглушку
        if not subtitles_file:
            subtitles_file = f"subtitles_{manifest.job_id}.srt"
        
        render_pack = RenderPack(
            manifest=manifest,
            ffmpeg_script=ffmpeg_script,
            assets_list=assets_list,
            subtitles_file=subtitles_file
        )
        
        return render_pack
    
    def _collect_assets(self, manifest: Manifest) -> List[str]:
        """
        Собрать список всех необходимых файлов ассетов.
        
        Args:
            manifest: Объект манифеста
            
        Returns:
            Список путей к файлам
        """
        assets = []
        
        # Изображения сцен
        for scene in manifest.scenes:
            if scene.image_path and scene.image_path not in assets:
                assets.append(scene.image_path)
        
        # Аудио треки
        for audio_path in manifest.audio_tracks:
            if audio_path and audio_path not in assets:
                assets.append(audio_path)
        
        # Фоновая музыка
        if manifest.background_music and manifest.background_music not in assets:
            assets.append(manifest.background_music)
        
        return assets
    
    def export_to_json(
        self,
        render_pack: RenderPack,
        output_path: Optional[str] = None
    ) -> str:
        """
        Экспортировать RenderPack в JSON формат.
        
        Args:
            render_pack: Объект RenderPack
            output_path: Путь для сохранения файла (опционально)
            
        Returns:
            JSON строка
        """
        data = {
            "job_id": render_pack.manifest.job_id,
            "manifest": self._manifest_to_dict(render_pack.manifest),
            "ffmpeg_script": render_pack.ffmpeg_script,
            "assets_list": render_pack.assets_list,
            "subtitles_file": render_pack.subtitles_file
        }
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Если указан путь, сохраняем в файл
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    def _manifest_to_dict(self, manifest: Manifest) -> Dict[str, Any]:
        """
        Конвертировать Manifest в словарь для JSON сериализации.
        
        Args:
            manifest: Объект Manifest
            
        Returns:
            Dict представление манифеста
        """
        return {
            "job_id": manifest.job_id,
            "orientation": manifest.orientation,
            "resolution": manifest.resolution,
            "total_duration_sec": manifest.total_duration_sec,
            "scenes": [
                {
                    "scene_id": scene.scene_id,
                    "start_time_sec": scene.start_time_sec,
                    "end_time_sec": scene.end_time_sec,
                    "duration_sec": scene.duration_sec,
                    "image_path": scene.image_path,
                    "audio_path": scene.audio_path,
                    "visual_prompt": scene.visual_prompt,
                    "camera_motion": scene.camera_motion,
                    "transition": scene.transition,
                    "subtitle_range": {
                        "start_index": scene.subtitle_range.start_index,
                        "end_index": scene.subtitle_range.end_index
                    }
                }
                for scene in manifest.scenes
            ],
            "subtitles": [
                {
                    "index": sub.index,
                    "start_time_sec": sub.start_time_sec,
                    "end_time_sec": sub.end_time_sec,
                    "text": sub.text
                }
                for sub in manifest.subtitles
            ],
            "audio_tracks": manifest.audio_tracks,
            "background_music": manifest.background_music,
            "transitions": [
                {
                    "from_scene_id": t.from_scene_id,
                    "to_scene_id": t.to_scene_id,
                    "type": t.type,
                    "duration_sec": t.duration_sec
                }
                for t in manifest.transitions
            ]
        }
    
    def generate_subtitle_file(
        self,
        manifest: Manifest,
        output_path: str
    ) -> str:
        """
        Сгенерировать файл субтитров в формате SRT.
        
        Args:
            manifest: Объект манифеста
            output_path: Путь для сохранения файла
            
        Returns:
            Путь к созданному файлу
        """
        lines = []
        
        for i, sub in enumerate(manifest.subtitles):
            # Индекс субтитра
            lines.append(str(i + 1))
            
            # Тайминги в формате SRT (HH:MM:SS,mmm --> HH:MM:SS,mmm)
            start_time = self._seconds_to_srt_time(sub.start_time_sec)
            end_time = self._seconds_to_srt_time(sub.end_time_sec)
            lines.append(f"{start_time} --> {end_time}")
            
            # Текст
            lines.append(sub.text)
            lines.append("")  # Пустая строка между субтитрами
        
        content = "\n".join(lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """
        Конвертировать секунды в формат времени SRT.
        
        Args:
            seconds: Время в секундах
            
        Returns:
            Строка в формате HH:MM:SS,mmm
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def create_deploy_package(
        self,
        render_pack: RenderPack,
        output_dir: str
    ) -> Dict[str, str]:
        """
        Создать пакет для деплоя на сервер рендеринга.
        
        Args:
            render_pack: Объект RenderPack
            output_dir: Директория для сохранения файлов
            
        Returns:
            Dict с путями к созданным файлам
        """
        import os
        
        # Создаём директорию если не существует
        os.makedirs(output_dir, exist_ok=True)
        
        # Пути к файлам
        manifest_path = os.path.join(output_dir, "manifest.json")
        script_path = os.path.join(output_dir, "render.sh")
        subtitles_path = os.path.join(output_dir, render_pack.subtitles_file)
        
        # Сохраняем манифест
        self.export_to_json(render_pack, manifest_path)
        
        # Сохраняем скрипт
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(render_pack.ffmpeg_script)
        
        # Делаем скрипт исполняемым
        os.chmod(script_path, 0o755)
        
        # Генерируем файл субтитров
        self.generate_subtitle_file(render_pack.manifest, subtitles_path)
        
        return {
            "manifest": manifest_path,
            "script": script_path,
            "subtitles": subtitles_path,
            "output_dir": output_dir
        }
