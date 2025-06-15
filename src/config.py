import os
from pydantic import BaseSettings, FilePath

class Settings(BaseSettings):
    # Основные настройки
    upload_folder: str = "./uploads"
    allowed_extensions: list = ["mp4", "avi", "mov"]
    max_file_size_mb: int = 100
    model_path: str = "./models/yolov5s.pt"
    
    # YouTube API настройки
    youtube_cookies_path: str = "./youtube_cookies.txt"
    client_secrets_path: str = "./client_secrets.json"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def validate_paths(self):
        """Проверяем существование критичных файлов"""
        required_files = {
            "YouTube Cookies": self.youtube_cookies_path,
            "Client Secrets": self.client_secrets_path,
            "Model": self.model_path
        }
        
        for name, path in required_files.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"{name} файл не найден: {path}")

# Инициализация настроек
settings = Settings()

# Проверка путей при старте
try:
    settings.validate_paths()
    # Создаем папку для загрузок, если её нет
    os.makedirs(settings.upload_folder, exist_ok=True)
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.error(f"Ошибка конфигурации: {str(e)}")
    raise
