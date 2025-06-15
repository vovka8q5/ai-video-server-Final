
from faster_whisper import WhisperModel
import os

def generate_subtitles(input_video_path, output_srt_path="stylized/stylized.srt", output_txt_path="stylized/stylized.txt"):
    model_size = "small"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print("🧠 Transcribing:", input_video_path)
    segments, _ = model.transcribe(input_video_path, beam_size=5)

    with open(output_srt_path, "w", encoding="utf-8") as srt_file,          open(output_txt_path, "w", encoding="utf-8") as txt_file:

        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            text = segment.text.strip()

            srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            txt_file.write(f"{text} ")

    print("✅ Subtitles saved:", output_srt_path)

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"
