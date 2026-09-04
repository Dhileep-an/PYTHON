import requests

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    if not city_name.strip():
        print("Error: City name cannot be empty.")
        return

    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp_c = data['main']['temp']
        temp_f = (temp_c * 9/5) + 32
        humidity = data['main']['humidity']
        condition = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']

        print("\n" + "="*30)
        print(f" Weather for: {data['name']}, {data['sys']['country']}")
        print("="*30)
        print(f" Temperature : {temp_c:.1f}°C / {temp_f:.1f}°F")
        print(f" Condition   : {condition}")
        print(f" Humidity    : {humidity}%")
        print(f" Wind Speed  : {wind_speed} m/s")
        print("="*30 + "\n")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: City '{city_name}' not found. Please check spelling.")
        elif response.status_code == 401:
            print("Error: Invalid API Key. Please verify your OpenWeatherMap key.")
        else:
            print(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again later.")
    except requests.exceptions.RequestException as req_err:
        print(f"Network error occurred: {req_err}")

def main():
    print("--- Python Weather App ---")
    while True:
        city = input("Enter city name or ZIP code (or 'quit' to exit): ").strip()
        if city.lower() == 'quit':
            print("Exiting weather app.")
            break
        get_weather(city)

if __name__ == "__main__":
    main()
