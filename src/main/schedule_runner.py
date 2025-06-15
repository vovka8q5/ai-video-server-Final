import time
import schedule
from datetime import datetime
from run_pipeline import run
from notifier import send_message

SCHEDULE_TIMES = ["08:00", "14:00", "20:00"]  # UTC

def job():
    start_time = datetime.now()
    send_message(f"⏳ Начало обработки в {start_time.strftime('%H:%M')} UTC")
    
    try:
        if run():
            duration = (datetime.now() - start_time).total_seconds() / 60
            send_message(f"✅ Успешно завершено за {duration:.1f} минут")
    except Exception as e:
        send_message(f"🔥 Ошибка пайплайна: {str(e)}")

def main():
    send_message("🚀 Планировщик запущен")
    
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()