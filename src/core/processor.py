import os
import subprocess
import logging
from pathlib import Path
from typing import Optional
from src.services.telegram import notify_admin
from src.utils.config import Config

logger = logging.getLogger(__name__)

def convert_to_shorts(
    input_path: Path,
    output_dir: Optional[Path] = None,
    duration: str = "00:00:59"
) -> Path:
    """
    Конвертирует видео в вертикальный формат Shorts (720x1280)
    
    Args:
        input_path: Путь к исходному видео
        output_dir: Директория для сохранения (по умолчанию PROCESSED_DIR)
        duration: Максимальная длительность (HH:MM:SS)
    
    Returns:
        Path: Путь к обработанному видео
    
    Raises:
        RuntimeError: Если конвертация не удалась
    """
    try:
        output_dir = output_dir or Config.PROCESSED_DIR
        output_path = output_dir / f"shorts_{input_path.name}"
        
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-t", duration,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "copy",
            "-y", str(output_path)
        ]
        
        logger.info(f"Конвертирую видео в Shorts: {input_path}")
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Ошибка конвертации: {e.stderr.decode()}"
        logger.error(error_msg)
        notify_admin(f"❌ Ошибка конвертации видео: {input_path.name}")
        raise RuntimeError(error_msg)

def apply_style(
    input_path: Path,
    style: str = "anime",
    output_dir: Optional[Path] = None
) -> Path:
    """
    Применяет AI-стилизацию к видео
    
    Args:
        input_path: Путь к исходному видео
        style: Стиль обработки ('anime', 'watercolor', 'sketch')
        output_dir: Директория для сохранения (по умолчанию STYLIZED_DIR)
    
    Returns:
        Path: Путь к стилизованному видео
    
    Raises:
        RuntimeError: Если стилизация не удалась
    """
    try:
        output_dir = output_dir or Config.STYLIZED_DIR
        output_path = output_dir / f"styled_{style}_{input_path.name}"
        
        # Заглушка для реальной AI-стилизации
        # В продакшене замените на вызов вашей модели
        if os.getenv("DEBUG_MODE"):
            logger.info(f"[DEBUG] Стилизация {input_path} как {style}")
            import shutil
            shutil.copy(input_path, output_path)
        else:
            # Здесь должен быть вызов реальной модели стилизации
            raise NotImplementedError("AI стилизация не реализована")
        
        logger.info(f"Стилизация завершена: {output_path}")
        return output_path
        
    except Exception as e:
        error_msg = f"Ошибка стилизации: {str(e)}"
        logger.error(error_msg, exc_info=True)
        notify_admin(f"❌ Ошибка стилизации: {input_path.name}")
        raise RuntimeError(error_msg)

def process_video_pipeline(
    input_path: Path,
    keep_intermediate: bool = False
) -> Path:
    """
    Полный пайплайн обработки видео:
    1. Конвертация в Shorts
    2. Стилизация
    
    Args:
        input_path: Путь к исходному видео
        keep_intermediate: Сохранять ли промежуточные файлы
    
    Returns:
        Path: Путь к финальному видео
    
    Raises:
        RuntimeError: Если любой этап не удался
    """
    try:
        # 1. Конвертация
        shorts_path = convert_to_shorts(input_path)
        
        # 2. Стилизация
        styled_path = apply_style(shorts_path, style="anime")
        
        if not keep_intermediate:
            shorts_path.unlink(missing_ok=True)
            
        return styled_path
        
    except Exception as e:
        logger.critical(f"Пайплайн обработки прерван: {str(e)}")
        raise