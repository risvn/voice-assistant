
# wiki_scraper.py
import sys
import requests
import urllib.parse
from bs4 import BeautifulSoup
import re

def search_wikipedia(query):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1
    }
    response = requests.get(search_url, params=params, headers={"User-Agent": "WikiFetcher/1.0"})
    if response.status_code == 200:
        results = response.json().get("query", {}).get("search", [])
        if results:
            return results[0]["title"]
    return None

def get_wikipedia_url(query):
    title = search_wikipedia(query)
    if title:
        return f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}"
    return None

def scrape_wikipedia_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error fetching page. Status code: {response.status_code}"

    soup = BeautifulSoup(response.content, "html.parser")
    content_area = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if not content_area:
        return "Couldn't find content area."

    paragraphs = content_area.find_all("p")
    if paragraphs:
        content = ""
        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)
            if text:
                content += text + "\n\n"

        #  Remove reference markers like [1], [2], [3]...
        cleaned = re.sub(r'\[\d+\]', '', content)
        return cleaned.strip()
    else:
        return "No paragraphs found."

def fallback_scrape(query):
    url = get_wikipedia_url(query)
    if url:
        return scrape_wikipedia_page(url)
    else:
        return "No Wikipedia page found for this query."
if __name__=="__main__"
    print(fallback_scrape(sys.argv[1]))
