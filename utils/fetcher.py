import feedparser
import wikipedia
import ssl
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=10)
        page = wikipedia.page(topic)
        
        links = page.links[:3]
        links_text = "\n".join([f"- {link}" for link in links])
        
        return f"{summary}\n\nRead more: {page.url}\n\nTop Links:\n{links_text}"
    except Exception as e:
        return f"Could not fetch Wikipedia summary: {e}"

def fetch_news_from_google(topic: str, max_articles=5):
    query = topic.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_articles]:
        title = entry.title
        link = entry.link
        summary = entry.summary if hasattr(entry, "summary") else (
            entry.description if hasattr(entry, "description") else "No summary available"
        )

        published = entry.published if hasattr(entry, "published") else "Unknown date"
        articles.append(f"Title: {title}\nPublished: {published}\nSummary: {summary}\nLink: {link}")
    
    return articles

def fetch_topic_data(topic: str):
    print(f"Fetching data for topic: {topic} (at {datetime.now()})\n")

    wiki = get_wikipedia_summary(topic)
    print("Wikipedia Summary:\n", wiki, "\n")
    
    news = fetch_news_from_google(topic)
    print("Google News Articles:\n", "\n\n".join(news), "\n")
    
    return f"Wikipedia Summary:\n{wiki}\n\nGoogle News Articles:\n" + "\n\n".join(news)

if __name__ == "__main__":
    topic = input("Enter a topic to fetch information about: ")
    print(fetch_topic_data(topic))