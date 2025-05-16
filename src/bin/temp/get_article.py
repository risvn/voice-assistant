
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import feedparser
import urllib.parse
from urllib.parse import urlparse

def fetch_news_urls(keyword, max_results=2):
    """Fetch top real article links from Google News RSS for a keyword."""
    rss_url = f"https://news.google.com/rss/search?q={urllib.parse.quote(keyword)}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for entry in feed.entries[:max_results]:
            try:
                
                page.goto(entry.link, timeout=8000)
                page.wait_for_timeout(1500)
                real_url = page.url
                links.append(real_url)
            except Exception as e:
                print(f"❌ Failed to resolve: {entry.link} - {e}")

        browser.close()

    return links

def scrape_article(url):
    """Scrape article content from a given news URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch {url}, status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Headline
    headline = soup.find("h1")
    headline = headline.text.strip() if headline else "No headline found"

    # Publish date
    date_tag = soup.find("meta", attrs={"property": "article:published_time"})
    publish_date = date_tag["content"] if date_tag and "content" in date_tag.attrs else "No date found"

    # Paragraphs (filter short or ad-like paragraphs)
    paragraphs = soup.find_all("p")
    content = "\n".join(p.text.strip() for p in paragraphs if len(p.text.strip()) > 50)

    # Extract domain name as source
    domain = urlparse(url).netloc.replace("www.", "")
    source = domain

    return {
        "headline": headline,
        "publish_date": publish_date,
        "content": content,
        "source": source
    }

def fetch_and_scrape(keyword):
    urls = fetch_news_urls(keyword)
    for url in urls:
        article = scrape_article(url)
        if article and article["content"]:  # if not empty
            return article
    return {"headline": "", "publish_date": "", "content": "No article could be fetched.", "source": ""}

# Example usage
result = fetch_and_scrape("what is waqf ")
print(result)
