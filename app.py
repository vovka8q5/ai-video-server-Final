from apscheduler.schedulers.blocking import BlockingScheduler
from youtube import find_english_trending_video, upload_video
from video_processor import process_video
from telegram_bot import send_telegram_alert
import logging
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_english_metadata(video_title: str):
    """Генерирует англоязычные метаданные"""
    # Ваша реализация с OpenAI (используйте prompt на английском)
    return {
        "title": f"Top Trending: {video_title}",
        "description": "Auto-generated English content. Like and subscribe!",
        "tags": ["trending", "english", "compilation"]
    }

def job():
    try:
        # 1. Поиск англоязычного видео
        url = find_english_trending_video()
        yt = YouTube(url)
        
        # 2. Генерация метаданных
        metadata = generate_english_metadata(yt.title)
        
        # 3. Обработка видео
        video_path = process_video(url, duration=58)
        
        # 4. Загрузка
        video_id = upload_video(
            video_path,
            metadata["title"],
            metadata["description"],
            metadata["tags"]
        )
        
        send_telegram_alert(
            f"🎬 New English video uploaded!\n"
            f"Title: {metadata['title']}\n"
            f"URL: https://youtu.be/{video_id}"
        )
        
    except Exception as e:
        send_telegram_alert(f"🚨 Error: {str(e)}")
        logger.error(f"Job failed: {str(e)}", exc_info=True)

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(job, 'cron', hour='0,6,12,18'minute=00)  # 00:00, 06:00, 12:00, 18:00 UTC 
    logger.info("Scheduler started (English content only)")
    scheduler.start()
