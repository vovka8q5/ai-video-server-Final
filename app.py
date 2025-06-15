import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from detector import process_video
from config import settings

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS (настройте под ваш фронтенд)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на конкретные домены
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

def allowed_file(filename: str) -> bool:
    """Проверяем, что файл имеет разрешенное расширение."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in settings.allowed_extensions
    )

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """Эндпоинт для загрузки видео."""
    try:
        # Проверка расширения файла
        if not allowed_file(file.filename):
            raise HTTPException(400, "Недопустимый формат файла")

        # Проверка размера файла
        max_size = settings.max_file_size_mb * 1024 * 1024
        file_size = 0
        for chunk in file.file:
            file_size += len(chunk)
            if file_size > max_size:
                raise HTTPException(400, "Файл слишком большой")

        # Сохраняем файл
        file_path = os.path.join(settings.upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            file.file.seek(0)
            buffer.write(file.file.read())

        logger.info(f"Файл {file.filename} успешно загружен")
        return {"filename": file.filename}

    except Exception as e:
        logger.error(f"Ошибка загрузки: {str(e)}")
        raise HTTPException(500, "Ошибка обработки файла")

@app.get("/detect/{filename}")
async def detect_objects(filename: str):
    """Эндпоинт для обработки видео."""
    try:
        file_path = os.path.join(settings.upload_folder, filename)
        if not os.path.exists(file_path):
            raise HTTPException(404, "Файл не найден")

        output_path = await process_video(file_path)
        return FileResponse(output_path, media_type="video/mp4")

    except Exception as e:
        logger.error(f"Ошибка детекции: {str(e)}")
        raise HTTPException(500, "Ошибка обработки видео")

@app.on_event("shutdown")
def cleanup():
    """Очистка временных файлов при завершении работы."""
    for filename in os.listdir(settings.upload_folder):
        file_path = os.path.join(settings.upload_folder, filename)
        try:
            os.unlink(file_path)
            logger.info(f"Удален временный файл: {filename}")
        except Exception as e:
            logger.error(f"Ошибка удаления {filename}: {str(e)}")
