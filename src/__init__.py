"""
AI Video Server - корневой пакет

Экспортирует основные компоненты для работы с видео-пайплайном
"""

# Версия пакета
__version__ = "1.0.0"

# Импорт ключевых модулей
from .main.schedule_runner import start_scheduler
from .main.run_pipeline import run_pipeline
from .core.downloader import download_video
from .core.processor import (
    convert_to_shorts,
    apply_style,
    process_video_pipeline
)
from .services.telegram import send_notification
from .utils.subtitles import generate_subtitles
from .utils.config import Config

# Автоматическое создание директорий при импорте
Config.initialize_dirs()

__all__ = [
    # Основные функции
    'start_scheduler',
    'run_pipeline',
    
    # Компоненты пайплайна
    'download_video',
    'convert_to_shorts',
    'apply_style', 
    'process_video_pipeline',
    'generate_subtitles',
    
    # Сервисы
    'send_notification',
    
    # Конфигурация
    'Config',
    
    # Метаданные
    '__version__'
]

# Инициализация логгера
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.LOGS_DIR / 'app.log')
    ]
)