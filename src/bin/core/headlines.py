import requests

NEWS_API_KEY = "67c5d79c7ae84b59ba4ed47b606d0ddc"

def get_latest_news():
    news_headlines = []
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=67c5d79c7ae84b59ba4ed47b606d0ddc')
    res = requests.get(url).json()
    articles = res["articles"]
    for article in articles:
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        source = article.get("source", {}).get("name", "Unknown Source")
    
        news_headlines.append({
            "title": title,
            "description": description,
            "source": source
        })
    
    return news_headlines[:5]

news_list = get_latest_news()

for idx, news in enumerate(news_list, start=1):
    print(f"\n Article {idx}")
    print(f" Title      : {news['title']}")
    print(f" Description: {news['description']}")
    print(f" Source     : {news['source']}")
