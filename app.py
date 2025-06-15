from apscheduler.schedulers.blocking import BlockingScheduler
from youtube import upload_video, find_trending_video
from video_processor import process_video
from telegram_bot import send_telegram_alert
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        # 1. Найти видео
        url = find_trending_video()
        logger.info(f"Найдено видео: {url}")

        # 2. Обработать (58-59 сек + анимация)
        video_path = process_video(url, duration=58)
        
        # 3. Загрузить на YouTube
        video_id = upload_video(video_path)
        msg = f"✅ Видео загружено! ID: {video_id}\nСсылка: https://youtu.be/{video_id}"
        
    except Exception as e:
        msg = f"❌ Ошибка: {str(e)}"
        logger.error(msg)
    
    # 4. Оповещение в Telegram
    send_telegram_alert(msg)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Запуск в 00:00, 06:00, 12:00, 18:00 (UTC)
    scheduler.add_job(job, 'cron', hour=00, minute=00) 
    scheduler.add_job(job, 'cron', hour=06, minute=00)
    scheduler.add_job(job, 'cron', hour=12, minute=00) 
    scheduler.add_job(job, 'cron', hour=18, minute=00) 
    logger.info("Сервис запущен. Ожидание задач...")
    scheduler.start()
