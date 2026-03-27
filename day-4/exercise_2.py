import sys
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL   = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_city_name():
    if len(sys.argv) >= 2:
        return " ".join(sys.argv[1:]).strip()
    city = input("Enter city name: ").strip()
    if not city:
        print("Error: City name cannot be empty.")
        sys.exit(1)
    return city


def safe_get(url, params, label):
    try:
        response = requests.get(url, params=params, timeout=10)
        if not response.ok:
            print(f"Error: {label} - HTTP {response.status_code}: {response.reason}")
            sys.exit(1)
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not reach Open-Meteo. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again later.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)


def geocode(city):
    data = safe_get(GEOCODING_URL, {"name": city, "count": 1, "language": "en"}, "Geocoding API")
    results = data.get("results")
    if not results:
        print(f"Error: City '{city}' not found. Try a different spelling or a nearby city.")
        sys.exit(1)
    location = results[0]
    return {
        "name":      location["name"],
        "country":   location.get("country", ""),
        "latitude":  location["latitude"],
        "longitude": location["longitude"],
        "timezone":  location.get("timezone", "UTC"),
    }


def fetch_weather(lat, lon, timezone):
    params = {
        "latitude":      lat,
        "longitude":     lon,
        "current":       "temperature_2m,windspeed_10m,weathercode",
        "timezone":      timezone,
        "forecast_days": 1,
    }
    data    = safe_get(WEATHER_URL, params, "Weather API")
    current = data.get("current", {})

    temp_c     = current.get("temperature_2m")
    wind_speed = current.get("windspeed_10m")
    wmo_code   = current.get("weathercode")

    if temp_c is None or wind_speed is None or wmo_code is None:
        print("Error: Incomplete weather data returned. Please try again.")
        sys.exit(1)

    return {
        "temp_c":      temp_c,
        "temp_f":      round(temp_c * 9 / 5 + 32, 1),
        "wind_speed":  wind_speed,
        "description": WMO_CODES.get(wmo_code, f"Unknown (code {wmo_code})"),
    }


def print_weather(location, weather):
    city_line = location["name"]
    if location["country"]:
        city_line += f", {location['country']}"

    print("\n" + "=" * 50)
    print(f"  {city_line}")
    print("=" * 50)
    print(f"  Condition   : {weather['description']}")
    print(f"  Temperature : {weather['temp_c']}C  /  {weather['temp_f']}F")
    print(f"  Wind Speed  : {weather['wind_speed']} km/h")
    print(f"  Coordinates : {location['latitude']}N, {location['longitude']}E")
    print("=" * 50 + "\n")


def main():
    city     = get_city_name()
    print(f"Looking up '{city}'...")
    location = geocode(city)
    print(f"Found: {location['name']}, {location['country']} ({location['latitude']}, {location['longitude']})")
    print("Fetching current weather...")
    weather  = fetch_weather(location["latitude"], location["longitude"], location["timezone"])
    print_weather(location, weather)


if __name__ == "__main__":
    main()