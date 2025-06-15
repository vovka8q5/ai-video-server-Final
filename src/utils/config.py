import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Config:
    """Централизованное хранилище конфигурации приложения"""
    
    # Базовые пути
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / 'assets'
    OUTPUT_DIR = BASE_DIR / 'output'
    TEMP_DIR = BASE_DIR / 'temp'
    
    # Пути к файлам
    COOKIES_PATH = ASSETS_DIR / 'youtube_cookies.txt'
    SECRETS_PATH = ASSETS_DIR / 'client_secrets.json'
    
    # Настройки видео
    VIDEO_SETTINGS = {
        'short_format': {
            'width': 720,
            'height': 1280,
            'duration': 59  # секунд
        },
        'max_file_size': 500 * 1024 * 1024  # 500MB
    }
    
    @classmethod
    def get_ffmpeg_path(cls) -> Path:
        """Возвращает путь к ffmpeg с проверкой наличия"""
        ffmpeg_path = Path('ffmpeg')  # В системе PATH
        try:
            subprocess.run([ffmpeg_path, '-version'], check=True, capture_output=True)
            return ffmpeg_path
        except:
            raise RuntimeError("FFmpeg не найден. Установите ffmpeg и добавьте в PATH")

    @classmethod
    def setup_dirs(cls):
        """Создает необходимые директории"""
        dirs = [cls.ASSETS_DIR, cls.OUTPUT_DIR, cls.TEMP_DIR]
        for dir_path in dirs:
            dir_path.mkdir(exist_ok=True)
            logger.debug(f"Директория {dir_path} проверена")

# Автоматическая инициализация при импорте
Config.setup_dirs()