import logging
import telegram
import openai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

def send_telegram_message(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        chat_id = TELEGRAM_CHAT_ID
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")

def translate_to_english(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate to English: {text}",
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Ошибка при переводе текста: {e}")
        return text

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
