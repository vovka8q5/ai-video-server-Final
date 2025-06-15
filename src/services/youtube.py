import os
from googleapiclient.discovery import build

# Безопасное получение ключа (с проверкой на ошибки)
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_APT_KEY")  # Используйте .get(), чтобы избежать KeyError

if not YOUTUBE_API_KEY:
    raise ValueError(
        "YouTube API key not found! "
        "Проверьте, что переменная 'YOUTUBE_APT_KEY' установлена в Render.com."
    )

# Инициализация клиента YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)