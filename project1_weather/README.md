# Weather Forecast API (Mini-Project 1)

A robust, modular Python application designed to query weather forecast data from a third-party REST API, process meteorological metrics, and analyze trends using Pandas.

## Features
- **API Integration:** Securely fetches real-time and forecasted weather data via HTTP requests.
- **Robust Error Handling:** Custom exception handling for network failures, timeouts, and invalid locations.
- **Data Analysis & Visualization:** Processes weather payloads into Pandas DataFrames for analytical insights.
- **Tested & Verified:** Comprehensive unit tests using `pytest` and mock fixtures.

## Project Structure
project1_weather/
├── src/
│   ├── init.py
│   └── weather_client.py
├── tests/
│   ├── fixtures/
│   └── test_weather.py
├── notebooks/
│   └── project1_weather.ipynb
├── requirements.txt
└── README.md
## Summary of findings
Data Flow Resilience: Decoupling user input validation from the external API client layer ensures that malformed inputs fail fast locally, preventing unnecessary network traffic and reducing latency.

Licensing Constraints: Public weather APIs rely heavily on tiered rate limits and require strict copyright attribution. Real-world commercial deployment necessitates aggressive local caching (e.g., Redis) to prevent hitting quota caps and incurring unexpected scaling costs.

Error Management: Explicit timeout enforcement and defensive exception handling successfully mitigate application lockups caused by network instability or invalid query parameters (404 and 429 HTTP statuses).

Privacy Governance: Transmitting location queries exposes user telemetry. Adhering to data minimization principles (querying by generalized regions rather than exact GPS coordinates) helps safeguard user privacy against third-party logging.