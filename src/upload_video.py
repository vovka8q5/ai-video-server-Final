from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import logging

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"] 

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(video_path, title, description, tags):
    try:
        youtube = get_authenticated_service()
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22",  # Категория "People & Blogs"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }
        media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file,
        ).execute()
        logging.info(f"Видео загружено на YouTube: {response['id']}")
        send_telegram_message("Видео успешно загружено!")
        return response
    except Exception as e:
        logging.error(f"Ошибка при загрузке видео: {e}")
        send_telegram_message(f"Ошибка при загрузке видео: {e}")
        raise