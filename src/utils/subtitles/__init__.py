"""
Модуль генерации субтитров

Предоставляет:
- Базовую генерацию субтитров (точная, но медленная)
- Быструю генерацию (менее точная, но оптимальная для Shorts)
- Конвертацию между форматами
"""

from pathlib import Path
from typing import Optional
import logging
from src.utils.config import Config

logger = logging.getLogger(__name__)

# Основные экспорты
from .base import (
    generate_subtitles as generate_subs_accurate,
    convert_to_srt,
    convert_to_vtt
)

from .fast import (
    generate_subtitles as generate_subs_fast,
    DEFAULT_MODEL_SIZE
)

# Алиасы для удобства
generate_subtitles = generate_subs_fast  # По умолчанию используем быстрый вариант

def auto_generate_subtitles(
    video_path: Path,
    output_path: Optional[Path] = None,
    fast: bool = True,
    model_size: str = DEFAULT_MODEL_SIZE
) -> Path:
    """
    Умная генерация субтитров с автоматическим выбором метода
    
    Args:
        video_path: Путь к видеофайлу
        output_path: Целевой путь (None = auto)
        fast: Использовать быстрый метод
        model_size: Размер модели (tiny, base, small, medium)
    
    Returns:
        Path: Путь к файлу субтитров (.srt)
    """
    output_path = output_path or Config.OUTPUT_DIR / f"{video_path.stem}.srt"
    
    try:
        if fast:
            logger.info(f"Генерация субтитров (быстрый режим, модель {model_size})")
            return generate_subs_fast(video_path, output_path, model_size)
        else:
            logger.info("Генерация субтитров (точный режим)")
            return generate_subs_accurate(video_path, output_path)
            
    except Exception as e:
        logger.error(f"Ошибка генерации субтитров: {str(e)}")
        raise RuntimeError(f"Subtitle generation failed: {str(e)}")

__all__ = [
    # Основные функции
    'generate_subtitles',
    'auto_generate_subtitles',
    
    # Точная генерация
    'generate_subs_accurate',
    
    # Конвертеры
    'convert_to_srt',
    'convert_to_vtt',
    
    # Константы
    'DEFAULT_MODEL_SIZE'
]