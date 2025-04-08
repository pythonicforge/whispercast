import ssl
import requests
import wikipedia
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from utils import logger

ssl._create_default_https_context = ssl._create_unverified_context

@logger.catch
def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=50)
        page = wikipedia.page(topic)
        
        links = page.links[:3]
        links_text = "\n".join([f"- {link}" for link in links])
        
        return f"{summary}\n\nRead more: {page.url}\n\nTop Links:\n{links_text}"
    except Exception as e:
        logger.critical(f"Could not fetch Wikipedia summary: {e}")

@logger.catch
def fetch_news_from_google(topic: str, max_articles=5):
    query = topic.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_articles]:
        title = entry.title
        link = entry.link
        published = entry.published if hasattr(entry, "published") else "Unknown date"

        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text() for p in paragraphs[:]]) 
            articles.append(f"Title: {title}\nPublished: {published}\nContent: {content}\nLink: {link}")
            return articles
        except Exception as e:
            logger.critical(f"Could not fetch article content: {e}")

@logger.catch
def fetch_topic_data(topic: str):
    wiki = get_wikipedia_summary(topic)
    news = fetch_news_from_google(topic)
    
    return f"Wikipedia Summary:\n{wiki}\n\nGoogle News Articles:\n" + "\n\n".join(news)