"""
Модуль утилит и вспомогательных функций

Содержит:
- Генерацию субтитров
- Конфигурацию приложения
- Вспомогательные инструменты
- Хелперы для работы с видео
"""

from pathlib import Path
import os

# Инициализация логгера
import logging
logger = logging.getLogger(__name__)

# Основные экспорты
from .config import Config, setup_dirs
from .subtitles import (
    generate_subtitles,
    generate_subtitles_fast,
    convert_to_srt
)
from .video_helpers import (
    get_video_duration,
    extract_thumbnail,
    validate_video
)
from .file_utils import (
    safe_delete,
    cleanup_temp_files,
    get_file_hash
)

# Автоматическая настройка при импорте
try:
    setup_dirs()
    logger.info("Директории приложения инициализированы")
except Exception as e:
    logger.error(f"Ошибка инициализации директорий: {str(e)}")

# Экспорт только необходимых компонентов
__all__ = [
    # Конфигурация
    'Config',
    
    # Субтитры
    'generate_subtitles',
    'generate_subtitles_fast',
    'convert_to_srt',
    
    # Видео-хелперы
    'get_video_duration',
    'extract_thumbnail', 
    'validate_video',
    
    # Файловые операции
    'safe_delete',
    'cleanup_temp_files',
    'get_file_hash'
]

# Дополнительная проверка окружения
if os.getenv('DEBUG_MODE'):
    logger.setLevel(logging.DEBUG)
    logger.debug("Режим отладки активирован")