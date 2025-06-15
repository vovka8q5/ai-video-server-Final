import os
import logging
from config import settings
import cv2
import torch

logger = logging.getLogger(__name__)

# Загрузка модели (кешируем один раз)
model = None

def load_model():
    """Загружаем модель при первом вызове."""
    global model
    if model is None:
        try:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=settings.model_path)
            logger.info("Модель YOLO загружена")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {str(e)}")
            raise
    return model

async def process_video(input_path: str) -> str:
    """Обрабатываем видео и возвращаем путь к результату."""
    try:
        model = load_model()
        output_path = input_path.replace(".mp4", "_output.mp4")

        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (frame_width, frame_height)
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Детекция объектов
            results = model(frame)
            rendered_frame = results.render()[0]
            out.write(rendered_frame)

        cap.release()
        out.release()
        logger.info(f"Видео обработано: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Ошибка обработки видео: {str(e)}")
        raise
