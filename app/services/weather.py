import requests


def get_current_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    current = data.get("current_weather", {})

    return {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": current.get("weathercode")
    }
