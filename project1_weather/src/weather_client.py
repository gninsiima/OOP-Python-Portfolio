import time
import requests
import urllib.request
import urllib.parse
import json
from typing import Dict, Any, List, Optional
import pandas as pd

class WeatherAPIError(Exception):
    """Custom exception raised when weather or geocoding API requests fail permanently."""
    pass

def urllib_geocode_demo(city_name: str, contact_email: str) -> Dict[str, Any]:
    """Part A.1: Geocodes using standard library urllib only."""
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "format": "json"}
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": f"AcademicProject ({contact_email})"}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))

def make_robust_request(url: str, params: Optional[Dict[str, Any]] = None, 
                        headers: Optional[Dict[str, str]] = None, 
                        timeout: int = 5, max_retries: int = 3) -> Dict[str, Any]:
    """Part C.1: Makes an HTTP GET request with exponential backoff retry logic and error handling."""
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            status_code = getattr(e.response, 'status_code', None)
            if status_code and 400 <= status_code < 500 and status_code != 429:
                raise WeatherAPIError(f"Client error {status_code}: {e}") from e
            
            if attempt == max_retries:
                raise WeatherAPIError(f"Request failed after {max_retries} attempts: {e}") from e
            
            time.sleep(delay)
            delay *= 2.0
    raise WeatherAPIError("Maximum retry attempts exhausted.")

def geocode_location(name: str, contact_email: str) -> List[Dict[str, Any]]:
    """Geocodes a location name using Open-Meteo Geocoding API with error handling."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 5, "language": "en", "format": "json"}
    headers = {"User-Agent": f"AcademicStudentProject ({contact_email})"}
    
    data = make_robust_request(url, params=params, headers=headers)
    results = data.get("results", [])
    if not results:
        raise WeatherAPIError(f"No locations found for query: '{name}'")
    return results

def get_forecast(lat: float, lon: float, days: int, contact_email: str) -> Dict[str, Any]:
    """Retrieves weather forecast from Open-Meteo Forecast API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto",
        "forecast_days": days
    }
    headers = {"User-Agent": f"AcademicStudentProject ({contact_email})"}
    return make_robust_request(url, params=params, headers=headers)

def decode_weather_code(code: int) -> str:
    """Decodes WMO weather interpretation codes into human-readable descriptions."""
    mapping = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 95: "Thunderstorm"
    }
    return mapping.get(code, f"Unknown code ({code})")

def process_forecast_to_dataframe(forecast_data: Dict[str, Any]) -> pd.DataFrame:
    """Converts raw Open-Meteo JSON forecast into a structured pandas DataFrame."""
    daily = forecast_data.get("daily", {})
    if not daily:
        raise ValueError("Forecast data missing 'daily' section.")
    
    df = pd.DataFrame({
        "Date": daily.get("time", []),
        "Weather Code": daily.get("weathercode", []),
        "Max Temp (°C)": daily.get("temperature_2m_max", []),
        "Min Temp (°C)": daily.get("temperature_2m_min", []),
        "Precipitation (mm)": daily.get("precipitation_sum", []),
        "Max Wind Speed (km/h)": daily.get("windspeed_10m_max", [])
    })
    df["Condition"] = df["Weather Code"].apply(decode_weather_code)
    return df