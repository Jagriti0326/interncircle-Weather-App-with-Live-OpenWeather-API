# Weather App with Live OpenWeather API

## Project Overview
This project is a Python-based Weather App that retrieves real-time weather information and a five-day forecast for a city using the OpenWeather API.

## Features
- Get current temperature in Celsius.
- Display feels-like temperature.
- Show humidity and weather conditions.
- Display wind speed.
- Retrieve a five-day weather forecast.
- Handle invalid city names and API errors.
- Use environment variables to protect the API key.
- Cache recent weather results to reduce unnecessary API requests.

## Technologies Used
- Python
- Requests
- Python-dotenv
- OpenWeather API

## Project Files
- `weather_app.py` — Main Python application.
- `.env` — Stores the private API key.
- `.gitignore` — Prevents sensitive and unnecessary files from being uploaded.
- `requirements.txt` — Lists required Python packages.

## Setup Instructions

1. Install Python.
2. Clone or download this repository.
3. Create and activate a virtual environment.
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Get an API key from https://openweathermap.org/api.
6. Create a `.env` file in the project folder and add:

   ```text
   OPENWEATHER_KEY=your_actual_api_key_here
   ```

7. Run the application:

   ```bash
   python weather_app.py
   ```

8. Enter a city name when prompted.

## Error Handling
The application handles missing API keys, invalid or inactive API keys, unknown cities, and network/API errors.

## API Key Security
The API key is stored in `.env` and should never be uploaded to GitHub. The `.gitignore` file excludes `.env` and the virtual environment.

## Testing
Test the application with at least five cities, such as Delhi, Mumbai, London, Tokyo, and New York.

## Screenshot
Add a screenshot of the application displaying actual weather information after testing.

## Author
Jagriti Singhal
