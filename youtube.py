from pytube import YouTube
from googleapiclient.discovery import build
import os
import json

def find_trending_video():
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    request = youtube.videos().list(
        part="id",
        chart="mostPopular",
        maxResults=1
    )
    return f"https://youtu.be/{request.execute()['items'][0]['id']}"

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
                "title": "Авто-видео",
                "description": "Создано автоматически"
            },
            "status": {"privacyStatus": "private"}
        },
        media_body=video_path
    )
    return request.execute()["id"]
