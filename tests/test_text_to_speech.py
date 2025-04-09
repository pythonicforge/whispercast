import unittest
import os
from utils.text_to_speech import generate_audio_file

class TestTextToSpeech(unittest.TestCase):
    def setUp(self):
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))

    def test_generate_audio_file_valid_content(self):
        content = "This is a test content for TTS."
        title = "TestAudio"
        output_path = generate_audio_file(content, title)
        self.assertTrue(os.path.exists(output_path))

    def test_generate_audio_file_empty_content(self):
        content = ""
        title = "EmptyAudio"
        output_path = generate_audio_file(content, title)
        self.assertEqual(output_path, "")

    def test_generate_audio_file_short_content(self):
        content = "Short"
        title = "ShortAudio"
        output_path = generate_audio_file(content, title)
        self.assertEqual(output_path, "")

if __name__ == "__main__":
    unittest.main()
