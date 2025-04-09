import unittest
from utils.llm import extract_llama_core_text, clean_placeholders

class TestLLM(unittest.TestCase):
    def test_extract_llama_core_text_with_delimiters(self):
        response = "---\nThis is the core text.\n---"
        result = extract_llama_core_text(response)
        self.assertEqual(result, "This is the core text.")

    def test_extract_llama_core_text_without_delimiters(self):
        response = "This is the full response."
        result = extract_llama_core_text(response)
        self.assertEqual(result, "This is the full response.")

    def test_clean_placeholders(self):
        text = "Hello [Name], welcome to [Podcast Name]."
        result = clean_placeholders(text, name="John", podcast_name="TechTalk")
        self.assertEqual(result, "Hello John, welcome to TechTalk.")

if __name__ == "__main__":
    unittest.main()
