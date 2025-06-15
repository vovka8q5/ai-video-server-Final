import os
import json
import logging
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_english_trending_video():
    """Ищет англоязычное трендовое видео"""
    try:
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        
        # Ищем в международных трендах (регион US + английский язык)
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode="US",
            maxResults=50,  # Больше выбор для фильтрации
            relevanceLanguage="en"  # Только английский
        )
        videos = request.execute()["items"]
        
        # Фильтруем по названию (исключаем неанглийские)
        for video in videos:
            title = video["snippet"]["title"]
            if all(ord(char) < 128 for char in title):  # Проверка на английские символы
                return f"https://youtu.be/{video['id']}"
        
        raise ValueError("Не найдено англоязычных видео в трендах")
        
    except Exception as e:
        logger.error(f"Ошибка поиска: {str(e)}")
        raise

def upload_video(video_path: str, title: str, description: str, tags: list):
    """Загружает видео с английскими метаданными"""
    try:
        youtube = build("youtube", "v3", 
                      credentials=Credentials.from_authorized_user_info(
                          json.loads(os.getenv("CLIENT_SECRETS_JSON"))
                      )
        
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "defaultLanguage": "en"  # Основной язык
                },
                "status": {"privacyStatus": "private"}
            },
            media_body=video_path
        )
        return request.execute()["id"]
    except HttpError as e:
        logger.error(f"Ошибка загрузки: {str(e)}")
        raise
