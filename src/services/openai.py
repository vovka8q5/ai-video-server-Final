import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_youtube_title_description(topic: str) -> dict:
    prompt = (
        f"Ты — маркетолог. Напиши крутой заголовок, описание и теги для Shorts "
        f"по теме: {topic}\\n\\n"
        f"Title: ...\\nDescription: ...\\nTags: ..."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return parse_result(response.choices[0].message.content.strip())

def parse_result(text: str) -> dict:
    lines = text.split("\\n")
    return {
        "title": next((l[6:].strip() for l in lines if l.startswith("Title:")), ""),
        "description": next((l[12:].strip() for l in lines if l.startswith("Description:")), ""),
        "tags": next((l[5:].strip() for l in lines if l.startswith("Tags:")), "")
    }
