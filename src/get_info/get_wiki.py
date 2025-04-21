import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup

def search_wikipedia(query):
    """Search Wikipedia and return the title of the first result."""
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
        # Construct the correct Wikipedia URL for the article
        return f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}"
    else:
        return "No matching Wikipedia page found."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_wiki_url.py <your search query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Wikipedia search URL for '{query}':")
    print(get_wikipedia_url(query))

url=get_wikipedia_url(query)

def scrape_wikipedia_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    print(f"▶️ Requested: {url}")
    print(f" Status Code: {response.status_code}")
    
    if response.status_code != 200:
        return f" Error fetching page. Status code: {response.status_code}"

    soup = BeautifulSoup(response.content, "html.parser")
    content_area = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if not content_area:
        return " Couldn't find content area."

    paragraphs = content_area.find_all("p")  # ← changed here
         
 # If paragraphs are found, extract and print text from them
    if paragraphs:
        print(f"Found {len(paragraphs)} paragraphs.")
        content = ""
        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)
            if text:  # Avoid empty paragraphs
                content += text + "\n\n"
        return content
    else:
        return " No paragraphs found in content area."





print(scrape_wikipedia_page(url))


