
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_KEY")
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Keep recent results briefly to avoid unnecessary API requests.
weather_cache = {}
CACHE_SECONDS = 300


def get_weather(city):
    """Fetch current weather for a city."""
    if not API_KEY:
        print("API key missing. Please add OPENWEATHER_KEY to your .env file.")
        return None

    cache_key = city.strip().lower()
    cached = weather_cache.get(cache_key)

    if cached and time.time() - cached["time"] < CACHE_SECONDS:
        print("(Using recently saved weather data.)")
        return cached["data"]

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            CURRENT_WEATHER_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            print("City not found. Please check the spelling.")
            return None

        if response.status_code == 401:
            print("Invalid or inactive API key. Check your .env file.")
            return None

        response.raise_for_status()
        data = response.json()

        weather_cache[cache_key] = {
            "time": time.time(),
            "data": data
        }

        return data

    except requests.exceptions.RequestException as error:
        print(f"Network or API problem: {error}")
        return None


def get_forecast(city):
    """Fetch a five-day forecast and select one entry per day."""
    if not API_KEY:
        return None

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            print("Forecast request failed: check your API key.")
            return None

        if response.status_code == 404:
            print("City not found for forecast.")
            return None

        response.raise_for_status()
        data = response.json()

        daily_forecasts = {}

        for item in data.get("list", []):
            date = item.get("dt_txt", "").split(" ")[0]

            if date and date not in daily_forecasts:
                main = item.get("main", {})
                weather_list = item.get("weather", [])

                description = (
                    weather_list[0].get("description", "Unavailable")
                    if weather_list else "Unavailable"
                )

                daily_forecasts[date] = {
                    "temperature": main.get("temp", "N/A"),
                    "description": description
                }

        return list(daily_forecasts.items())[:5]

    except requests.exceptions.RequestException as error:
        print(f"Could not retrieve forecast: {error}")
        return None


def display_weather(data):
    """Display the current weather details."""
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    wind = data.get("wind", {})

    description = (
        weather_list[0].get("description", "Unavailable")
        if weather_list else "Unavailable"
    )

    print("\n" + "=" * 40)
    print(f"WEATHER FOR {data.get('name', 'Unknown city').upper()}")
    print("=" * 40)
    print(f"Temperature : {main.get('temp', 'N/A')} °C")
    print(f"Feels like  : {main.get('feels_like', 'N/A')} °C")
    print(f"Humidity    : {main.get('humidity', 'N/A')}%")
    print(f"Conditions  : {description.capitalize()}")
    print(f"Wind speed  : {wind.get('speed', 'N/A')} m/s")


def display_forecast(forecasts):
    """Display the forecast in a simple table."""
    print("\nFIVE-DAY FORECAST")
    print("-" * 65)
    print(f"{'Date':<15}{'Temperature':<18}{'Conditions'}")
    print("-" * 65)

    if not forecasts:
        print("Forecast unavailable.")
        return

    for date, details in forecasts:
        print(
            f"{date:<15}"
            f"{str(details['temperature']) + ' °C':<18}"
            f"{details['description'].capitalize()}"
        )

    print("-" * 65)


def main():
    print("=" * 40)
    print("       PYTHON WEATHER APP")
    print("=" * 40)

    if not API_KEY:
        print("Please add your OpenWeather API key to the .env file.")
        return

    while True:
        city = input("\nEnter city name (blank to quit): ").strip()

        if not city:
            print("Thank you for using the Weather App!")
            break

        data = get_weather(city)

        if data:
            display_weather(data)
            forecast = get_forecast(city)
            display_forecast(forecast)


if __name__ == "__main__":
    main()
