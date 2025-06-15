import cv2
import os
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip
import logging

logger = logging.getLogger(__name__)

# 1. Скачать видео
def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').first()
    path = stream.download(output_path="downloads")
    logger.info(f"Видео скачано: {path}")
    return path

# 2. Обработать (кадры + субтитры + музыка)
def process_video(video_path):
    # Субтитры
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    with open("subtitles.srt", "w") as f:
        for seg in result["segments"]:
            f.write(f"{seg['text']}\n")
    
    # Музыка (файл background.mp3 должен быть в папке)
    video = VideoFileClip(video_path)
    audio = AudioFileClip("background.mp3").volumex(0.3)
    final = video.set_audio(audio)
    
    output_path = "final_video.mp4"
    final.write_videofile(output_path)
    return output_path
