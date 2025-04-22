import sys
import wikipedia
import urllib.parse
from wikipedia.exceptions import DisambiguationError, PageError

def get_summary(query):
        summary = wikipedia.summary(query, sentences=7)
        return summary

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


query = " ".join(sys.argv[1:])
print(get_summary(query))

