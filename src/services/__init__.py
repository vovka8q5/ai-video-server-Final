"""
Сервисный слой приложения - взаимодействие с внешними API и сервисами

Содержит:
- Telegram уведомления
- YouTube API клиент
- OpenAI интеграцию
- Другие внешние сервисы
"""

from .telegram import (
    send_message,
    send_alert,
    notify_admin,
    setup_telegram_bot
)

from .youtube import (
    upload_video,
    fetch_trending_videos,
    get_video_stats
)

from .openai import (
    generate_video_title,
    generate_description,
    generate_tags,
    analyze_script
)

# Экспорт только основных функций
__all__ = [
    # Telegram
    'send_message',
    'send_alert',
    'notify_admin',
    'setup_telegram_bot',
    
    # YouTube
    'upload_video',
    'fetch_trending_videos',
    'get_video_stats',
    
    # OpenAI
    'generate_video_title',
    'generate_description',
    'generate_tags',
    'analyze_script'
]

# Инициализация сервисов при импорте
try:
    setup_telegram_bot(
        token=os.getenv('TELEGRAM_BOT_TOKEN'),
        chat_id=os.getenv('TELEGRAM_CHAT_ID')
    )
except Exception as e:
    import logging
    logging.warning(f"Не удалось инициализировать Telegram бота: {str(e)}")