import os
from pathlib import Path

class Config:
    # Базовые директории
    BASE_DIR = Path(__file__).parent.parent
    
    # Пути к секретным файлам в Render
    COOKIES_PATH = Path('/etc/secrets/youtube_cookies.txt')
    SECRETS_PATH = Path('/etc/secrets/client_secrets.json')
    
    # Локальные пути для тестирования (если файлы не найдены в /etc/secrets)
    LOCAL_COOKIES = BASE_DIR / 'assets' / 'youtube_cookies.txt'
    LOCAL_SECRETS = BASE_DIR / 'assets' / 'client_secrets.json'
    
    @classmethod
    def get_cookies_path(cls):
        """Возвращает корректный путь к файлу cookies"""
        if cls.COOKIES_PATH.exists():
            return cls.COOKIES_PATH
        return cls.LOCAL_COOKIES
    
    @classmethod
    def get_secrets_path(cls):
        """Возвращает корректный путь к client_secrets.json"""
        if cls.SECRETS_PATH.exists():
            return cls.SECRETS_PATH
        return cls.LOCAL_SECRETS
    
    # Директории для выходных файлов
    OUTPUT_DIR = BASE_DIR / 'output'
    DOWNLOADS_DIR = OUTPUT_DIR / 'downloads'
    PROCESSED_DIR = OUTPUT_DIR / 'processed'

# Создаем директории при импорте
Config.OUTPUT_DIR.mkdir(exist_ok=True)
Config.DOWNLOADS_DIR.mkdir(exist_ok=True)
Config.PROCESSED_DIR.mkdir(exist_ok=True)