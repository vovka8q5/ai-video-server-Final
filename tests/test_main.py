import unittest
from src.download_video import download_video_by_query
from src.process_video import (
    extract_audio,
    trim_video,
    add_animation,
    replace_faces,
    generate_new_script,
    add_subtitles,
    add_music,
)
from src.upload_video import upload_to_youtube
from src.utils import (
    send_telegram_message,
    translate_to_english,
    log_info,
    log_error,
)
from src.config import *
import os

class TestMain(unittest.TestCase):
    def setUp(self):
        self.video_path = "tests/videos/"
        self.faces_dir = "tests/faces/"
        self.music_path = "tests/music.mp3"
        self.query = "example video"
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

    def test_download_video_by_query(self):
        video_url = download_video_by_query(self.query, self.video_path)
        self.assertIsNotNone(video_url)
        self.assertTrue(os.path.exists(os.path.join(self.video_path, "downloaded_video.mp4")))

    def test_extract_audio(self):
        video_path = os.path.join(self.video_path, "downloaded_video.mp4")
        audio_path = os.path.join(self.video_path, "audio.wav")
        extract_audio(video_path, audio_path)
        self.assertTrue(os.path.exists(audio_path))

    def test_trim_video(self):
        video_path = os.path.join(self.video_path, "downloaded_video.mp4")
        trimmed_video_path = os.path.join(self.video_path, "trimmed_video.mp4")
        trim_video(video_path, 0, 50, trimmed_video_path)
        self.assertTrue(os.path.exists(trimmed_video_path))

    def test_add_animation(self):
        trimmed_video_path = os.path.join(self.video_path, "trimmed_video.mp4")
        animated_video_path = os.path.join(self.video_path, "animated_video.mp4")
        add_animation(trimmed_video_path, animated_video_path)
        self.assertTrue(os.path.exists(animated_video_path))

    def test_replace_faces(self):
        animated_video_path = os.path.join(self.video_path, "animated_video.mp4")
        replaced_video_path = os.path.join(self.video_path, "replaced_video.mp4")
        source_face = os.path.join(self.faces_dir, "source_face.jpg")
        target_face = os.path.join(self.faces_dir, "target_face.jpg")
        replace_faces(animated_video_path, replaced_video_path, source_face, target_face)
        self.assertTrue(os.path.exists(replaced_video_path))

    def test_generate_new_script(self):
        audio_path = os.path.join(self.video_path, "audio.wav")
        script = generate_new_script(audio_path)
        self.assertIsNotNone(script)

    def test_add_subtitles(self):
        replaced_video_path = os.path.join(self.video_path, "replaced_video.mp4")
        subtitled_video_path = os.path.join(self.video_path, "subtitled_video.mp4")
        script = "This is a test subtitle."
        add_subtitles(replaced_video_path, script, subtitled_video_path)
        self.assertTrue(os.path.exists(subtitled_video_path))

    def test_add_music(self):
        subtitled_video_path = os.path.join(self.video_path, "subtitled_video.mp4")
        final_video_path = os.path.join(self.video_path, "final_video.mp4")
        add_music(subtitled_video_path, self.music_path, final_video_path)
        self.assertTrue(os.path.exists(final_video_path))

    def test_upload_to_youtube(self):
        final_video_path = os.path.join(self.video_path, "final_video.mp4")
        title_en = "Test Video"
        description_en = "This is a test video."
        tags_en = ["test", "youtube", "shorts"]
        response = upload_to_youtube(final_video_path, title_en, description_en, tags_en)
        self.assertIsNotNone(response)
        self.assertIn('id', response)

if __name__ == "__main__":
    unittest.main()
