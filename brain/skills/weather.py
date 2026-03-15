import requests

def get_weather(city):
    # Mapping for common cities (default Balurghat)
    cities = {
        "balurghat": (25.2167, 88.7667),
        "kolkata": (22.5726, 88.3639),
        "delhi": (28.6139, 77.2090),
        "mumbai": (19.0760, 72.8777)
    }
    
    city_lower = city.lower()
    if city_lower in cities:
        lat, lon = cities[city_lower]
    else:
        # Fallback to Balurghat for now, or suggest AI search for coords
        lat, lon = 25.2167, 88.7667
        
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_weather']
        
        return f"Weather for {city.capitalize()}:\nTemperature: {current['temperature']}°C\nWindspeed: {current['windspeed']} km/h\nWeathercode: {current['weathercode']}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
