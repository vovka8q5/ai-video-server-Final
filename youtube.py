import os
import json
import time
import random
import logging
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_youtube_cookies():
    """Загружает cookies из переменных окружения и сохраняет в файл."""
    cookies = os.getenv("YOUTUBE_COOKIES")
    if not cookies:
        raise ValueError("Не найдены YOUTUBE_COOKIES в переменных окружения!")
    
    with open("cookies.txt", "w") as f:
        f.write(cookies)
    logger.info("Cookies для YouTube загружены")

def find_trending_video(region_code: str = "US") -> str:
    """Ищет самое популярное видео в указанном регионе."""
    try:
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        request = youtube.videos().list(
            part="id",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=1
        )
        response = request.execute()
        video_id = response["items"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        logger.info(f"Найдено трендовое видео: {url}")
        return url
    except Exception as e:
        logger.error(f"Ошибка поиска видео: {str(e)}")
        raise

def upload_video(video_path: str, title: str = "Автоматическое видео") -> str:
    """Загружает видео на YouTube с защитой от блокировки."""
    try:
        # 1. Задержка перед загрузкой (5-15 минут)
        delay = random.randint(300, 900)
        logger.info(f"Ожидание {delay} сек для избежания блокировки...")
        time.sleep(delay)

        # 2. Настройка cookies и OAuth
        load_youtube_cookies()
        creds = Credentials.from_authorized_user_info(
            info=json.loads(os.getenv("CLIENT_SECRETS_JSON"))
        )

        # 3. Загрузка через API
        youtube = build("youtube", "v3", credentials=creds)
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": "Создано автоматически",
                    "tags": ["авто", "обработка"]
                },
                "status": {"privacyStatus": "private"}
            },
            media_body=video_path
        )
        response = request.execute()
        video_id = response["id"]
        logger.info(f"Видео {video_id} успешно загружено!")
        return video_id

    except HttpError as e:
        if e.resp.status == 403:
            logger.error("Достигнут лимит загрузок! Сплю 1 час...")
            time.sleep(3600)
        raise
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
        raise
