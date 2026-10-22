import pytest
import json
from pathlib import Path
import pandas as pd
from src.weather_client import decode_weather_code, process_forecast_to_dataframe, WeatherAPIError

def load_sample_fixture():
    fixture_path = Path("tests/fixtures/forecast_sample.json")
    if fixture_path.exists():
        with open(fixture_path, "r") as f:
            return json.load(f)
    return {
        "daily": {
            "time": ["2026-10-20"],
            "weathercode": [0],
            "temperature_2m_max": [20.0],
            "temperature_2m_min": [10.0],
            "precipitation_sum": [0.0],
            "windspeed_10m_max": [10.0]
        }
    }

def test_weather_code_decoding():
    """Test 1: Verify correct WMO weather code mapping."""
    assert decode_weather_code(0) == "Clear sky"
    assert decode_weather_code(61) == "Slight rain"
    assert "Unknown" in decode_weather_code(999)

def test_dataframe_processing_structure():
    """Test 2: Verify dataframe columns and shape from sample JSON."""
    data = load_sample_fixture()
    df = process_forecast_to_dataframe(data)
    
    assert isinstance(df, pd.DataFrame)
    assert "Date" in df.columns
    assert "Condition" in df.columns
    assert "Max Temp (°C)" in df.columns
    assert len(df) == len(data["daily"]["time"])

def test_dataframe_values_correctness():
    """Test 3: Verify parsed values match source data."""
    data = load_sample_fixture()
    df = process_forecast_to_dataframe(data)
    
    assert df.loc[0, "Max Temp (°C)"] == data["daily"]["temperature_2m_max"][0]
    assert df.loc[0, "Condition"] == "Clear sky"

def test_missing_daily_section_raises_error():
    """Test 4: Verify error handling when 'daily' key is absent."""
    invalid_data = {"latitude": 0.0, "longitude": 0.0}
    with pytest.raises(ValueError, match="Forecast data missing 'daily' section."):
        process_forecast_to_dataframe(invalid_data)

def test_empty_dataframe_handling():
    """Test 5: Verify behavior with empty time series."""
    empty_data = {"daily": {"time": [], "weathercode": [], "temperature_2m_max": [], "temperature_2m_min": [], "precipitation_sum": [], "windspeed_10m_max": []}}
    df = process_forecast_to_dataframe(empty_data)
    assert df.empty