from moviepy.editor import VideoFileClip, vfx, TextClip, CompositeVideoClip, AudioFileClip
import whisper
import cv2
import face_recognition
import numpy as np
import os

def extract_audio(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='mp3')
        log_info(f"Аудио извлечено: {audio_path}")
    except Exception as e:
        log_error(f"Ошибка при извлечении аудио: {e}")
        raise

def trim_video(video_path, start_time, end_time, output_path):
    try:
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        clip.write_videofile(output_path, codec="libx264")
        log_info(f"Видео обрезано: {output_path}")
    except Exception as e:
        log_error(f"Ошибка при обрезке видео: {e}")
        raise

def add_animation(video_path, output_path):
    try:
        clip = VideoFileClip(video_path)
        animated_clip = clip.fx(vfx.colorx, 1.5)  # Увеличение яркости
        animated_clip.write_videofile(output_path, codec="libx264")
        log_info(f"Анимация добавлена: {output_path}")
    except Exception as e:
        log_error(f"Ошибка при добавлении анимации: {e}")
        raise

def load_face_encoding(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) == 0:
            raise ValueError("Лицо не найдено на изображении.")
        return face_encodings[0]
    except Exception as e:
        log_error(f"Ошибка при загрузке кодировки лица: {e}")
        raise

def replace_faces(video_path, output_path, source_face, target_face):
    try:
        # Загрузка изображений лиц
        source_face_encoding = load_face_encoding(source_face)
        target_face_encoding = load_face_encoding(target_face)
        
        # Загрузка видео
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Распознавание лиц на кадре
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Сравнение лиц
                matches = face_recognition.compare_faces([source_face_encoding], face_encoding)
                
                if matches[0]:
                    # Замена лица
                    target_face_image = face_recognition.load_image_file(target_face)
                    target_face_image = cv2.cvtColor(target_face_image, cv2.COLOR_RGB2BGR)
                    target_face_location = face_recognition.face_locations(target_face_image)[0]
                    
                    # Обрезка и масштабирование целевого лица
                    top_t, right_t, bottom_t, left_t = target_face_location
                    target_face_image = target_face_image[top_t:bottom_t, left_t:right_t]
                    target_face_image = cv2.resize(target_face_image, (right-left, bottom-top))
                    
                    # Замена лица на кадре
                    frame[top:bottom, left:right] = target_face_image
            
            out.write(frame)
        
        cap.release()
        out.release()
        log_info(f"Лица заменены: {output_path}")
    except Exception as e:
        log_error(f"Ошибка при замене лиц: {e}")
        raise

def generate_new_script(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript = result["text"]
        prompt = f"Generate a new script based on: {transcript}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        log_error(f"Ошибка при генерации сценария: {e}")
        return ""

def add_subtitles(video_path, subtitles, output_path):
    try:
        video = VideoFileClip(video_path)
        subtitles_clip = TextClip(subtitles, fontsize=24, color='white')
        subtitles_clip = subtitles_clip.set_position(('center', 'bottom')).set_duration(video.duration)
        final_clip = CompositeVideoClip([video, subtitles_clip])
        final_clip.write_videofile(output_path, codec="libx264")
        log_info(f"Субтитры добавлены: {output_path}")
    except Exception as e:
        log_error(f"Ошибка при добавлении субтитров: {e}")
        raise

def add_music(video_path, music_path, output_path):
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(music_path)
        final_clip = video.set_audio(audio)
        final_clip.write_videofile(output_path, codec="libx264")
        log_info(f"Музыка добавлена: {output_path}")
    except Exception as e:
        log_error(f"Ошибка при добавлении музыки: {e}")
        raise
