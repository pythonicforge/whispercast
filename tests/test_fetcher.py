import unittest
from utils.fetcher import get_wikipedia_summary, fetch_news_from_google

class TestFetcher(unittest.TestCase):
    def test_get_wikipedia_summary(self):
        summary = get_wikipedia_summary("Python (programming language)")
        self.assertIn("Python is an interpreted", summary)

    def test_fetch_news_from_google(self):
        articles = fetch_news_from_google("Python programming")
        self.assertTrue(len(articles) > 0)

if __name__ == "__main__":
    unittest.main()
