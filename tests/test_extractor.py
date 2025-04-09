import unittest
import os
from utils.extractor import extract_content, is_url

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.test_txt_file = "test.txt"
        with open(self.test_txt_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_txt_file):
            os.remove(self.test_txt_file)

    def test_is_url(self):
        self.assertTrue(is_url("http://example.com"))
        self.assertFalse(is_url("not_a_url"))

    def test_extract_content_from_txt(self):
        content = extract_content(self.test_txt_file)
        self.assertIn("This is a test file.", content)

    def test_extract_content_from_raw_text(self):
        content = extract_content("This is raw text.")
        self.assertIn("This is raw text.", content)

if __name__ == "__main__":
    unittest.main()
