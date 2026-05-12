"""
FFmpeg Instruction Builder

Генерирует команды ffmpeg для рендеринга видео на основе манифеста.
"""

from typing import List, Dict, Any, Optional
from .render_schema import Manifest, ManifestScene, TransitionMap


class FFmpegInstructionBuilder:
    """
    Строитель инструкций для ffmpeg.
    
    Генерирует полный скрипт команд для рендеринга видео
    на основе Manifest.
    """
    
    # Разрешения видео
    RESOLUTIONS = {
        "240p": "426x240",
        "360p": "640x360",
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
    }
    
    # Ориентации
    ORIENTATIONS = {
        "vertical": "9:16",
        "horizontal": "16:9",
        "square": "1:1",
    }
    
    def build_ffmpeg_script(self, manifest: Manifest) -> Dict[str, str]:
        """
        Построить полный скрипт ffmpeg.
        
        Args:
            manifest: Объект манифеста
            
        Returns:
            Dict с ffmpeg_script
        """
        commands = []
        
        # Добавляем заголовок
        commands.append("#!/bin/bash")
        commands.append(f"# FFmpeg render script for job: {manifest.job_id}")
        commands.append(f"# Resolution: {manifest.resolution}")
        commands.append(f"# Orientation: {manifest.orientation}")
        commands.append(f"# Total duration: {manifest.total_duration_sec:.2f}s")
        commands.append("")
        
        # Получаем разрешение
        resolution = self.RESOLUTIONS.get(manifest.resolution, "1280x720")
        
        # Генерируем complex filter для всех сцен
        filter_complex = self._build_filter_complex(manifest)
        
        # Основная команда ffmpeg
        cmd = f'ffmpeg -y \\\n'
        
        # Input файлы (изображения и аудио)
        inputs = self._build_inputs(manifest)
        cmd += inputs
        
        # Filter complex
        cmd += f'-filter_complex "{filter_complex}" \\\n'
        
        # Output настройки
        cmd += f'-c:v libx264 -preset fast -crf 23 \\\n'
        cmd += f'-c:a aac -b:a 192k \\\n'
        cmd += f'-movflags +faststart \\\n'
        cmd += f'-pix_fmt yuv420p \\\n'
        cmd += f'-r 30 \\\n'
        cmd += f'{resolution} \\\n'
        
        # Output файл
        output_file = f"output_{manifest.job_id}.mp4"
        cmd += f'"{output_file}"'
        
        commands.append(cmd)
        commands.append("")
        commands.append(f"echo 'Render complete: {output_file}'")
        
        full_script = "\n".join(commands)
        
        return {
            "ffmpeg_script": full_script
        }
    
    def _build_inputs(self, manifest: Manifest) -> str:
        """
        Построить список input файлов.
        
        Args:
            manifest: Объект манифеста
            
        Returns:
            Строка с input параметрами
        """
        inputs = []
        
        # Добавляем изображения
        for scene in manifest.scenes:
            if scene.image_path:
                inputs.append(f'-loop 1 -t {scene.duration_sec} -i "{scene.image_path}" \\\n')
        
        # Добавляем аудио
        for audio_path in manifest.audio_tracks:
            if audio_path:
                inputs.append(f'-i "{audio_path}" \\\n')
        
        # Фоновая музыка
        if manifest.background_music:
            inputs.append(f'-i "{manifest.background_music}" \\\n')
        
        return "".join(inputs)
    
    def _build_filter_complex(self, manifest: Manifest) -> str:
        """
        Построить complex filter chain.
        
        Args:
            manifest: Объект манифеста
            
        Returns:
            Строка filter_complex
        """
        filters = []
        
        num_scenes = len(manifest.scenes)
        
        if num_scenes == 0:
            return ""
        
        # Генерируем цепочку фильтров для каждой сцены
        scene_filters = []
        audio_indices = list(range(num_scenes))  # Индексы аудио потоков
        
        for i, scene in enumerate(manifest.scenes):
            # Индекс видео потока
            video_idx = i
            audio_idx = i
            
            # Масштабирование и движение камеры
            scale_filter = f"[{video_idx}:v]scale={self.RESOLUTIONS.get(manifest.resolution, '1280x720')}"
            
            # Движение камеры
            motion_filter = self._get_camera_motion_filter(scene.camera_motion, scene.duration_sec)
            if motion_filter:
                scale_filter += f",{motion_filter}"
            
            # Переходы
            if i < num_scenes - 1:
                transition = manifest.transitions[i] if i < len(manifest.transitions) else None
                if transition:
                    trans_filter = self._get_transition_filter(transition.type, transition.duration_sec)
                    if trans_filter:
                        scale_filter += f",{trans_filter}"
            
            scale_filter += f"[v{i}]"
            scene_filters.append(scale_filter)
            
            # Аудио нормализация
            audio_filter = f"[{audio_idx}:a]anormalize=peak=0.95[a{i}]"
            scene_filters.append(audio_filter)
        
        # Конкатенация видео и аудио
        video_concat_inputs = "".join([f"[v{i}]" for i in range(num_scenes)])
        audio_concat_inputs = "".join([f"[a{i}]" for i in range(num_scenes)])
        
        concat_filter = f"{video_concat_inputs}{audio_concat_inputs}concat=n={num_scenes}:v=1:a=1[outv][outa]"
        scene_filters.append(concat_filter)
        
        # Субтитры (если есть)
        if manifest.subtitles:
            subtitle_file = "subtitles.srt"
            subtitle_filter = f"[outv]subtitles={subtitle_file}[finalv]"
            scene_filters.append(subtitle_filter)
            final_output = "[finalv][outa]"
        else:
            final_output = "[outv][outa]"
        
        # Добавляем маппинг
        filters.append(";".join(scene_filters))
        
        return filters[0] if filters else ""
    
    def _get_camera_motion_filter(self, motion: str, duration: float) -> str:
        """
        Получить фильтр для движения камеры.
        
        Args:
            motion: Тип движения (static, zoom_in, zoom_out, pan, shake)
            duration: Длительность в секундах
            
        Returns:
            Строка фильтра или пустая строка
        """
        if motion == "static" or not motion:
            return ""
        
        if motion == "zoom_in":
            return f"zoompan=z='min(zoom+0.0015,1.5)':d={int(duration*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        
        elif motion == "zoom_out":
            return f"zoompan=z='max(zoom-0.0015,1)':d={int(duration*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        
        elif motion == "pan":
            return f"crop=iw*0.9:ih*0.9,xstack"
        
        elif motion == "shake":
            return f"crop=iw:iw*0.9,shake=amplitude=2:pitch=0.5:yaw=0.5"
        
        return ""
    
    def _get_transition_filter(self, transition_type: str, duration: float) -> str:
        """
        Получить фильтр для перехода.
        
        Args:
            transition_type: Тип перехода
            duration: Длительность перехода
            
        Returns:
            Строка фильтра или пустая строка
        """
        if transition_type == "cut" or duration == 0:
            return ""
        
        if transition_type == "fade":
            return f"fade=t=out:st={duration-0.5}:d=0.5"
        
        elif transition_type == "blur":
            return f"boxblur=10:1"
        
        elif transition_type == "glitch":
            return f"displace=ox=0.05:oy=0.05"
        
        return ""
    
    def generate_simple_concat_script(
        self,
        scenes: List[ManifestScene],
        output_file: str,
        resolution: str = "720p"
    ) -> Dict[str, str]:
        """
        Сгенерировать простой скрипт для конкатенации сцен.
        
        Args:
            scenes: Список сцен
            output_file: Имя выходного файла
            resolution: Разрешение
            
        Returns:
            Dict с ffmpeg_script
        """
        commands = []
        commands.append("#!/bin/bash")
        commands.append("# Simple concat script")
        commands.append("")
        
        # Создаём файл списка
        commands.append("cat > concat_list.txt << EOF")
        for scene in scenes:
            commands.append(f"file '{scene.image_path}'")
            commands.append(f"duration {scene.duration_sec}")
        commands.append("EOF")
        commands.append("")
        
        resolution_str = self.RESOLUTIONS.get(resolution, "1280x720")
        
        cmd = f'ffmpeg -y -f concat -safe 0 -i concat_list.txt \\\n'
        cmd += f'-c:v libx264 -preset fast -crf 23 \\\n'
        cmd += f'-c:a aac -b:a 192k \\\n'
        cmd += f'-movflags +faststart \\\n'
        cmd += f'-pix_fmt yuv420p \\\n'
        cmd += f'-r 30 \\\n'
        cmd += f'{resolution_str} \\\n'
        cmd += f'"{output_file}"'
        
        commands.append(cmd)
        
        return {
            "ffmpeg_script": "\n".join(commands)
        }
