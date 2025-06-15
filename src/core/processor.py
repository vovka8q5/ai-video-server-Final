import subprocess
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def convert_to_shorts(
    input_path: Path,
    output_path: Optional[Path] = None,
    max_duration: int = 59
) -> Path:
    """Безопасная конвертация в Shorts формат"""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file missing: {input_path}")
    
    output_path = output_path or input_path.with_stem(f"{input_path.stem}_shorts")
    
    try:
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vf", "scale=720:1280,setsar=1",
            "-t", str(max_duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "copy",
            "-y", str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            check=True,
            timeout=300,  # 5 минут таймаут
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
            
        return output_path
        
    except subprocess.TimeoutExpired:
        logger.error("FFmpeg timeout exceeded")
        raise
    except Exception as e:
        logger.error(f"Video processing failed: {str(e)}")
        raise
