from pytube import YouTube
from googleapiclient.discovery import build
import os
import logging

logger = logging.getLogger(__name__)

# 1. Поиск популярного видео
def find_trending_video():
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    request = youtube.videos().list(
        part="id",
        chart="mostPopular",
        maxResults=1
    )
    response = request.execute()
    return f"https://youtu.be/{response['items'][0]['id']}"

# 2. Загрузка на канал
def upload_video(video_path):
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(
        info=json.loads(os.getenv("CLIENT_SECRETS_JSON"))
    )
    youtube = build("youtube", "v3", credentials=creds)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Автоматическое видео",
                "description": "Создано роботом"
            },
            "status": {"privacyStatus": "private"}
        },
        media_body=video_path
    )
    return request.execute()["id"]
