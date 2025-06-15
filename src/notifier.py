import os
import requests
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def send_message(text: str, max_retries: int = 3) -> bool:
    """
    Отправляет сообщение в Telegram с обработкой ошибок
    
    Args:
        text: Текст сообщения
        max_retries: Количество попыток отправки
        
    Returns:
        bool: True если сообщение отправлено успешно
    """
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("Telegram credentials not configured!")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            logger.warning(f"Attempt {attempt + 1}: Status {response.status_code}")
        except Exception as e:
            logger.error(f"Telegram send error: {str(e)}")
    
    logger.error(f"Failed after {max_retries} attempts")
    return False
