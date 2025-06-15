import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.downloader import download_video
from utils.processor import process_video
from utils.subtitles import generate_subtitles
from scripts.upload_youtube import upload_video
from notifier import send_message

def run():
    try:
        # 1. Скачивание
        video_path = download_video("https://youtu.be/dQw4w9WgXcQ")
        
        # 2. Обработка
        processed_path = process_video(video_path)
        
        # 3. Субтитры
        subtitles_path = generate_subtitles(processed_path)
        
        # 4. Загрузка
        video_url = upload_video(processed_path)
        
        send_message(f"✅ Видео загружено: {video_url}")
        return True
        
    except Exception as e:
        send_message(f"❌ Ошибка: {str(e)}")
        raise