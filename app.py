import time
from apscheduler.schedulers.blocking import BlockingScheduler
from youtube_tools import find_trending_video, upload_video
from video_processor import download_video, process_video
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        logger.info("=== Начало автоматической загрузки ===")
        
        # 1. Найти трендовое видео
        url = find_trending_video()
        logger.info(f"Найдено видео: {url}")
        
        # 2. Скачать и обработать
        video_path = download_video(url)
        final_video = process_video(video_path)
        
        # 3. Загрузить на YouTube
        video_id = upload_video(final_video)
        logger.info(f"Видео загружено! ID: {video_id}")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', hours=6)  # Запуск каждые 6 часов
    logger.info("Сервис запущен. Ожидание задач...")
    scheduler.start()
