import requests
import json

def get_detailed_weather(city):
    url = f"https://wttr.in/{city}?format=j1"  # JSON format
    try:
        res = requests.get(url)
        data = res.json()

        current = data["current_condition"][0]

        context = (
            f"Weather Report for {city.capitalize()}:\n"
            f"- Temperature: {current['temp_C']}°C\n"
            f"- Condition: {current['weatherDesc'][0]['value']}\n"
            f"- Wind: {current['windspeedKmph']} km/h {current['winddir16Point']}\n"
            f"- Humidity: {current['humidity']}%\n"
            f"- Feels Like: {current['FeelsLikeC']}°C\n"
            f"- Cloud Cover: {current['cloudcover']}%\n"
        )

        return context

    except Exception as e:
        return f"Error fetching weather: {e}"

if __name__ == "__main__":
    print(get_detailed_weather("hyderabad"))

