import feedparser
import re
from datetime import datetime

# RSS feeds from Indian news sources
RSS_FEEDS = [
    "https://feeds.feedburner.com/ndtvnews-top-stories",
    "https://indianexpress.com/section/india/feed/",
    "https://www.indiatoday.in/rss/home"
]

def clean_source_name(name):
    name = re.sub(r'\s*Search Records Found.*$', '', name)
    name = re.sub(r'\s*\d+\s*$', '', name)
    return name.strip()

def fetch_top_headlines(max_articles=3):
    headlines = []
    sources = set()
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        source_raw = feed.feed.get("title", "Unknown Source")
        source = clean_source_name(source_raw)
        sources.add(source)
        for entry in feed.entries:
            title = entry.title.strip()
            description = entry.get("summary", "").strip()
            headlines.append({
                "title": title,
                "description": description,
                "source": source
            })
    # Limit to max_articles
    return headlines[:max_articles], sorted(sources)

if __name__ == "__main__":
    today = datetime.now().strftime("%A, %d %B %Y")
    headlines, sources = fetch_top_headlines()

    print(f" {today}")
    print(f" Top News Headlines in India Today from {', '.join(sources)}:\n")

    for idx, article in enumerate(headlines, start=1):
        print(f"Article {idx} ")
        print(f" Title      : {article['title']}")
        print(f" Description: {article['description'] or 'No description available.'}")
        print(f" Source     : {article['source']}\n")

