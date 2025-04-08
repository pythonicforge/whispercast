import ssl
import requests
import wikipedia
import feedparser
from bs4 import BeautifulSoup
from utils import logger
from urllib.parse import quote_plus

ssl._create_default_https_context = ssl._create_unverified_context

@logger.catch
def get_wikipedia_summary(topic):
    try:
        search_results = wikipedia.search(topic)
        if not search_results:
            raise ValueError("No matching pages found on Wikipedia")

        best_match = search_results[0]
        summary = wikipedia.summary(best_match, sentences=30)
        page = wikipedia.page(best_match)

        links = page.links[:5]
        links_text = "\n".join([f"- {link}" for link in links])

        return f"{summary}\n\nRead more: {page.url}\n\nTop Links:\n{links_text}"
    except Exception as e:
        logger.warning(f"Fallback: Wikipedia summary failed for '{topic}': {e}")
        return "Wikipedia summary not available."

@logger.catch
def fetch_news_from_google(topic: str, max_articles=5):
    query = quote_plus(topic)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_articles]:
        title = entry.title
        link = entry.link
        published = getattr(entry, "published", "Unknown date")

        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text() for p in paragraphs[:5]])
            articles.append(f"Title: {title}\nPublished: {published}\nContent: {content}\nLink: {link}")
        except Exception as e:
            logger.warning(f"Skipping article due to fetch error: {e}")
            continue

    if not articles:
        return ["No recent news articles found."]
    return articles

@logger.catch
def fetch_from_duckduckgo(topic: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        query = quote_plus(topic)
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all("a", class_="result__a")
        texts = [result.get_text() for result in results[:3]]
        links = [result["href"] for result in results[:3]]

        return "\n".join([f"{texts[i]} - {links[i]}" for i in range(len(texts))])
    except Exception as e:
        logger.warning(f"DuckDuckGo fallback failed: {e}")
        return "DuckDuckGo search failed."
    
@logger.catch
def fetch_reddit_posts(topic: str, max_posts: int = 3):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = quote_plus(topic)
    url = f"https://www.reddit.com/search/?q={query}&sort=relevance&t=week"

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("a", attrs={"data-click-id": "body"}, limit=max_posts)

        results = []
        for post in posts:
            title = post.get_text()
            link = "https://www.reddit.com" + post["href"]
            results.append(f"{title} - {link}")

        return results if results else ["No relevant Reddit posts found."]
    except Exception as e:
        logger.warning(f"Failed to fetch Reddit posts!")
        return [f"Error fetching Reddit posts: {e}"]

@logger.catch
def fetch_hacker_news_articles(topic: str, max_articles: int = 3):
    try:
        hn_url = f"https://hn.algolia.com/api/v1/search?query={quote_plus(topic)}"
        response = requests.get(hn_url)
        data = response.json()

        hits = data.get("hits", [])[:max_articles]
        articles = []
        for hit in hits:
            title = hit.get("title", "No title")
            link = hit.get("url", "No URL")
            articles.append(f"{title} - {link}")

        return articles if articles else ["No Hacker News articles found."]
    except Exception as e:
        logger.warning(f"Failed to fetch HackerNews posts!")
        return [f"Error fetching Hacker News articles: {e}"]

@logger.catch
def fetch_topic_data(topic: str):
    logger.info(f"Fetching topic data for: {topic}")
    wiki = get_wikipedia_summary(topic)
    news = fetch_news_from_google(topic)
    ddg = fetch_from_duckduckgo(topic)
    reddit = fetch_reddit_posts(topic)
    hacker_news = fetch_hacker_news_articles(topic)

    news_data = "\n\n".join(news)

    return f"Wikipedia Summary:\n{wiki}\n\nGoogle News Articles:\n{news_data}\n\nDuckDuckGo Insights:\n{ddg}\nReddit:\n{reddit}\nHackerNews:\n{hacker_news}"
