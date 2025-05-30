import sys
import wikipedia
import requests
from wikipedia.exceptions import DisambiguationError, PageError

def get_summary(query):
    try:
        # Try getting the summary directly
        summary = wikipedia.summary(query, sentences=6)
        return summary
    except (DisambiguationError, PageError) as e:
        # If summary fails, fallback to search and get the title
        title = search_wikipedia(query)
        if title:
            return wikipedia.summary(title, sentences=6)
        else:
            return "No relevant inforamation page found."
    except Exception as e:
        return f"Unexpected error: {e}"

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <your search query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(get_summary(query))

