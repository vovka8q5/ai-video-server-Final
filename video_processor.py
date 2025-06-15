from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.all import speedx
import cv2
import numpy as np
import os

def process_video(url, duration=58):
    # Скачать видео
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').first()
    path = stream.download(output_path="downloads")
    
    # Обрезать до 58-59 сек
    clip = VideoFileClip(path).subclip(0, duration)
    
    # Анимация: ускорение/замедление
    final_clip = speedx(clip, factor=1.2)  # Пример эффекта
    
    # Добавить музыку
    audio = AudioFileClip("background.mp3").volumex(0.3)
    final_clip = final_clip.set_audio(audio)
    
    # Сохранить
    output_path = "final_video.mp4"
    final_clip.write_videofile(output_path)
    return output_path
