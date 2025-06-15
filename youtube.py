import os
import json
import random
import logging
import openai  # Добавляем OpenAI
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# Настройка OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Исправьте название переменной, если нужно

def generate_metadata(video_title: str) -> dict:
    """Генерирует заголовок, описание и теги через OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник для создания SEO-оптимизированных метаданных YouTube."},
                {"role": "user", "content": f"Сгенерируй креативные заголовок, описание и 5 тегов для видео на тему: '{video_title}'. Ответ в формате JSON."}
            ]
        )
        return json.loads(response.choices[0].message["content"])
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {str(e)}")
        return {
            "title": video_title + " | Автоматическое видео",
            "description": "Создано автоматически. Подпишитесь на канал!",
            "tags": ["авто", "видео", "обработка"]
        }

def upload_video(video_path: str, original_title: str) -> str:
    """Загружает видео с AI-метаданными."""
    try:
        # Генерация метаданных
        metadata = generate_metadata(original_title)
        
        # Загрузка на YouTube
        creds = Credentials.from_authorized_user_info(
            info=json.loads(os.getenv("CLIENT_SECRETS_JSON"))
        youtube = build("youtube", "v3", credentials=creds)
        
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "tags": metadata["tags"]
                },
                "status": {"privacyStatus": "private"}
            },
            media_body=video_path
        )
        return request.execute()["id"]
    except HttpError as e:
        logger.error(f"Ошибка YouTube API: {str(e)}")
        raise
