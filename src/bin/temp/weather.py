import requests
import json

def get_detailed_weather(city):
    url = f"https://wttr.in/{city}?format=j1"  # JSON format
    try:
        res = requests.get(url)
        data = res.json()

        current = data["current_condition"][0]

        print(f" Location     : {city.capitalize()}")
        print(f" Temperature  : {current['temp_C']}°C")
        print(f" Condition    : {current['weatherDesc'][0]['value']}")
        print(f" Wind         : {current['windspeedKmph']} km/h {current['winddir16Point']}")
        print(f" Humidity     : {current['humidity']}%")
        print(f" Feels Like   : {current['FeelsLikeC']}°C")
        print(f" Cloud Cover  : {current['cloudcover']}%")

    except Exception as e:
        print("Error fetching weather:", e)

get_detailed_weather("hyderabad")
