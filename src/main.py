import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from download_video import download_video_by_query
from process_video import (
    extract_audio,
    trim_video,
    add_animation,
    replace_faces,
    generate_new_script,
    add_subtitles,
    add_music,
)
from upload_video import upload_to_youtube
from utils import (
    send_telegram_message,
    translate_to_english,
    log_info,
    log_error,
)
from config import *

def check_files():
    required_files = [
        CLIENT_SECRETS_FILE,
        TOKEN_FILE,
        MUSIC_PATH,
        os.path.join(FACES_DIR, "source_face.jpg"),
        os.path.join(FACES_DIR, "target_face.jpg"),
    ]
    for file in required_files:
        if not os.path.exists(file):
            log_error(f"Файл не найден: {file}")
            raise FileNotFoundError(f"Файл не найден: {file}")

def main():
    try:
        # Проверка наличия необходимых файлов
        check_files()
        
        # Поиск и скачивание видео по ключевому слову с многомиллионными просмотрами
        query = "example video"  # Замените на нужный ключевой запрос
        video_path = VIDEOS_DIR
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        video_url = download_video_by_query(query, video_path)
        if not video_url:
            log_error("Не удалось скачать видео по запросу.")
            return
        
        # Обрезка видео на эпизоды
        trimmed_video_path = os.path.join(video_path, "trimmed_video.mp4")
        trim_video(os.path.join(video_path, "downloaded_video.mp4"), 0, 50, trimmed_video_path)
        
        # Анимация кадров
        animated_video_path = os.path.join(video_path, "animated_video.mp4")
        add_animation(trimmed_video_path, animated_video_path)
        
        # Замена лиц
        replaced_video_path = os.path.join(video_path, "replaced_video.mp4")
        source_face = os.path.join(FACES_DIR, "source_face.jpg")
        target_face = os.path.join(FACES_DIR, "target_face.jpg")
        replace_faces(animated_video_path, replaced_video_path, source_face, target_face)
        
        # Генерация нового сценария
        audio_path = os.path.join(video_path, "audio.wav")
        extract_audio(replaced_video_path, audio_path)
        script = generate_new_script(audio_path)
        
        # Наложение субтитров
        subtitled_video_path = os.path.join(video_path, "subtitled_video.mp4")
        add_subtitles(replaced_video_path, script, subtitled_video_path)
        
        # Добавление музыки
        final_video_path = os.path.join(video_path, "final_video.mp4")
        add_music(subtitled_video_path, MUSIC_PATH, final_video_path)
        
        # Загрузка на YouTube
        title_ru = "Моя первая видеозапись"
        description_ru = "Описание моей первой видеозаписи"
        tags_ru = ["первое видео", "YouTube Shorts"]
        
        title_en = translate_to_english(title_ru)
        description_en = translate_to_english(description_ru)
        tags_en = [translate_to_english(tag) for tag in tags_ru]
        
        upload_to_youtube(final_video_path, title_en, description_en, tags_en)
        
    except Exception as e:
        log_error(f"Ошибка: {e}")
        send_telegram_message(f"Ошибка: {e}")

def schedule_videos():
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour='20', minute='34')  # Расписание на 20:34
    scheduler.start()

if __name__ == "__main__":
    schedule_videos()
