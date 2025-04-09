import unittest
from cli.shell import Whisper

class TestShell(unittest.TestCase):
    def test_whisper_intro(self):
        shell = Whisper()
        self.assertIn("Welcome to WhisperCast!", shell.intro)

if __name__ == "__main__":
    unittest.main()
