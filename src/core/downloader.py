def download_from_youtube(url: str, output_path="input/raw_videos/video.mp4") -> str:
    import yt_dlp
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': output_path,
        'quiet': True,
        'cookiefile': 'youtube_cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path
