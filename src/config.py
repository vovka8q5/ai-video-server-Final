import os

# Переменные окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Путь к файлам
CLIENT_SECRETS_FILE = "/etc/secrets/client_secrets.json"
TOKEN_FILE = "/etc/secrets/token.pickle"
VIDEOS_DIR = "videos/"
FACES_DIR = "faces/"
MUSIC_PATH = "music.mp3"
