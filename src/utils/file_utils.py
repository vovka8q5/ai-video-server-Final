import os
import hashlib
from pathlib import Path
from typing import List
import logging
from src.utils.config import Config

logger = logging.getLogger(__name__)

def safe_delete(file_path: Path, max_retries: int = 3) -> bool:
    """Безопасное удаление файла с повторными попытками"""
    for attempt in range(max_retries):
        try:
            file_path.unlink(missing_ok=True)
            if not file_path.exists():
                return True
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1}: Не удалось удалить {file_path}: {e}")
            time.sleep(1)
    
    logger.error(f"Не удалось удалить файл после {max_retries} попыток: {file_path}")
    return False

def cleanup_temp_files(directory: Path = None, pattern: str = "*") -> int:
    """Очищает временные файлы и возвращает количество удаленных"""
    directory = directory or Config.TEMP_DIR
    deleted_count = 0
    
    for temp_file in directory.glob(pattern):
        if safe_delete(temp_file):
            deleted_count += 1
    
    logger.info(f"Удалено {deleted_count} временных файлов в {directory}")
    return deleted_count

def get_file_hash(file_path: Path, buffer_size: int = 65536) -> str:
    """Вычисляет SHA-256 хеш файла"""
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Ошибка вычисления хеша: {e}")
        raise

def rotate_files(directory: Path, max_files: int = 10) -> None:
    """Удаляет старые файлы, сохраняя не более max_files"""
    files = sorted(directory.glob("*"), key=os.path.getmtime, reverse=True)
    
    for old_file in files[max_files:]:
        safe_delete(old_file)