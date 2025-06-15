import subprocess
from pathlib import Path
from typing import Tuple, Optional
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

def get_video_duration(video_path: Path) -> float:
    """Возвращает длительность видео в секундах"""
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ],
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        logger.error(f"Ошибка получения длительности: {e}")
        raise

def extract_thumbnail(
    video_path: Path,
    output_path: Optional[Path] = None,
    time: str = "00:00:01"
) -> Path:
    """Извлекает thumbnail из видео"""
    output_path = output_path or Config.TEMP_DIR / "thumbnail.jpg"
    
    try:
        subprocess.run(
            [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', time,
                '-vframes', '1',
                '-q:v', '2',
                '-y', str(output_path)
            ],
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка извлечения thumbnail: {e.stderr.decode()}")
        raise

def validate_video(video_path: Path) -> bool:
    """Проверяет валидность видео файла"""
    checks = [
        (video_path.exists(), "Файл не существует"),
        (video_path.stat().st_size < Config.VIDEO_SETTINGS['max_file_size'], "Слишком большой файл"),
        (get_video_duration(video_path) <= Config.VIDEO_SETTINGS['short_format']['duration'], "Слишком длинное видео")
    ]
    
    for condition, error_msg in checks:
        if not condition:
            logger.warning(f"Невалидное видео: {error_msg}")
            return False
    return True