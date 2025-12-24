from os import getenv

import requests
from langchain.tools import tool


@tool
def get_geolocation_by_city(city: str) -> dict:
    """Get the latitude and longitude for a given city using a public API.
    Args:
        city (str): Name of the city.
    Returns:
        dict: A dictionary containing 'lat' and 'lon' keys.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={getenv('WEATHER_API_KEY')}"
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        raise ValueError(f"Error fetching geolocation data: {response.text}")
    data = response.json()
    if not data:
        raise ValueError(f"No geolocation data found for city: {city}")
    return {"lat": data[0]["lat"], "lon": data[0]["lon"]}


@tool
def get_weather(lat: float, lon: float) -> str:
    """Get the current weather for a given location using a public API. Unit is in metric. If user asks for city name, first use get_geolocation_by_city to get lat and lon.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    Returns:
        str: Weather data in JSON format. Please understand and parse it accordingly. You need to summarize the weather information for the user.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={getenv('WEATHER_API_KEY')}"
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        raise ValueError(f"Error fetching weather data: {response.text}")
    return response.json()


@tool
def get_air_quality(lat: float, lon: float) -> str:
    """Get the current air quality for a given location using a public API.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    Returns:
        str: Air quality data in JSON format. Please understand and parse it accordingly. You need to summarize the air quality information for the user.
    """
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={getenv('WEATHER_API_KEY')}"
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        raise ValueError(f"Error fetching air quality data: {response.text}")
    return response.json()
