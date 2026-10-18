# project5.py
# Weather App with Live Open Weather API

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_KEY")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather(city):
    '''Fetches current weather and 5-day forecast for the specified city.'''
    if not API_KEY:
        print("Error: API Key not found. Please set OPENWEATHER_KEY in your .env file.")
        return None, None
        
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    try:
        # Get Current Weather
        r_current = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        
        if r_current.status_code == 401:
            print("API error (401): Invalid API key. If newly created, wait a bit and try again.")
            return None, None
        elif r_current.status_code == 404:
            print(f"City not found: '{city}'. Please try a different name.")
            return None, None
            
        r_current.raise_for_status()
        current_data = r_current.json()
        
        # Get Forecast Weather
        r_forecast = requests.get(FORECAST_URL, params=params, timeout=10)
        r_forecast.raise_for_status()
        forecast_data = r_forecast.json()
        
        return current_data, forecast_data
        
    except requests.exceptions.RequestException as e:
        print(f"Network problem. Check your connection or API status: {e}")
        return None, None

def print_forecast(forecast_list):
    '''Extracts and prints one forecast entry per day.'''
    print("\n--- 5-Day Forecast ---")
    print(f"{'Date & Time':<20} | {'Temp (°C)':<10} | {'Conditions':<20}")
    print("-" * 55)
    
    # The API returns data in 3-hour increments. We'll pick one reading per day (e.g., around noon).
    # We can approximate this by picking every 8th record (8 * 3 hours = 24 hours)
    for i in range(0, len(forecast_list), 8):
        entry = forecast_list[i]
        date_str = entry.get('dt_txt', 'N/A')
        temp = entry.get('main', {}).get('temp', 'N/A')
        weather_desc = entry.get('weather', [{}])[0].get('description', 'N/A')
        print(f"{date_str:<20} | {temp:<10} | {weather_desc:<20}")

def main():
    print("Welcome to the OpenWeather App!")
    while True:
        city = input("\nEnter a City (or press Enter to quit): ").strip()
        if not city:
            print("Exiting application...")
            break
            
        current, forecast = fetch_weather(city)
        
        if current and forecast:
            name = current.get('name', 'Unknown')
            temp = current.get('main', {}).get('temp', 'N/A')
            humidity = current.get('main', {}).get('humidity', 'N/A')
            desc = current.get('weather', [{}])[0].get('description', 'N/A')
            wind_speed = current.get('wind', {}).get('speed', 'N/A')
            
            print(f"\n=== Current Weather in {name} ===")
            print(f"Temperature: {temp}°C")
            print(f"Humidity:    {humidity}%")
            print(f"Conditions:  {desc.capitalize()}")
            print(f"Wind Speed:  {wind_speed} m/s")
            
            forecast_list = forecast.get('list', [])
            if forecast_list:
                print_forecast(forecast_list)

if __name__ == '__main__':
    main()
