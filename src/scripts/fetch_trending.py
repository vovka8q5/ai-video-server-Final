# scripts/fetch_trending.py
import requests
import os

def get_trending_video_urls(count=3):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise EnvironmentError("YOUTUBE_API_KEY is not set in environment variables")

    api_url = (
        "https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet&chart=mostPopular&maxResults={count}&regionCode=US&key={api_key}"
    )

    response = requests.get(api_url)
    data = response.json()

    urls = []
    for item in data.get("items", []):
        video_id = item["id"]
        full_url = f"https://www.youtube.com/watch?v={video_id}"
        urls.append(full_url)

    return urls
