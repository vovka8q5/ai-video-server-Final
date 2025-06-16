from pytube import YouTube
from googleapiclient.discovery import build
import os

def search_videos(query, max_results=1, order='viewCount'):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            order=order  # Сортировка по количеству просмотров
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        return video_ids
    except Exception as e:
        log_error(f"Ошибка при поиске видео: {e}")
        return []

def download_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        download_path = os.path.join(output_path, "downloaded_video.mp4")
        stream.download(output_path=output_path, filename="downloaded_video.mp4")
        log_info(f"Видео скачано: {download_path}")
        return video_url
    except Exception as e:
        log_error(f"Ошибка при скачивании видео: {e}")
        return None

def download_video_by_query(query, output_path):
    try:
        video_ids = search_videos(query, max_results=1, order='viewCount')
        if not video_ids:
            log_error("Видео не найдено по запросу.")
            return None
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        downloaded_url = download_video(video_url, output_path)
        return downloaded_url
    except Exception as e:
        log_error(f"Ошибка при поиске и скачивании видео: {e}")
        return None
