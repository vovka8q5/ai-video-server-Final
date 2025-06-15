import os
from faster_whisper import WhisperModel
from typing import Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED_MODELS = ["tiny", "base", "small", "medium"]

def generate_subtitles(
    input_video: str,
    output_srt: str = None,
    model_size: str = "small",
    device: str = "cpu",
    beam_size: int = 5
) -> Tuple[str, float]:
    """
    Генерирует субтитры с проверкой параметров
    
    Returns:
        tuple: (путь к файлу, продолжительность обработки)
    """
    if model_size not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model. Available: {SUPPORTED_MODELS}")
    
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input file not found: {input_video}")

    output_srt = output_srt or f"{Path(input_video).stem}.srt"
    
    try:
        model = WhisperModel(model_size, device=device)
        segments, info = model.transcribe(input_video, beam_size=beam_size)
        
        with open(output_srt, "w", encoding="utf-8") as srt_file:
            for segment in segments:
                srt_file.write(
                    f"{segment.id}\n"
                    f"{segment.start:.2f} --> {segment.end:.2f}\n"
                    f"{segment.text.strip()}\n\n"
                )
        
        return (output_srt, info.duration)
    
    except Exception as e:
        logger.error(f"Subtitle generation failed: {str(e)}")
        raise  
