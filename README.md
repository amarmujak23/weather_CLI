# weather-CLI

A small, dependency-light command line weather application that uses the Open-Meteo APIs to
look up cities and display a 10-day forecast.

## Features

- Search for a city name (the app shows the top 10 geocoding results).
- Select a city from the numbered list to view a 10-day forecast (high/low temps and weather description).
- Option to re-open the original top-10 list to select another city, or exit/restart the program.

## Requirements

- Python 3.8 or newer
- Internet access (the app calls external APIs)
- Packages listed in `requirements.txt` (the project uses `requests`)

## Installation

1. Clone or download the repository.
2. Optionally create a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
source .venv/bin/activate    # macOS / Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Files of interest

- `weather_CLI.py`: main CLI script to run.
- `weather_codes.json`: mapping of Open-Meteo weather codes to readable descriptions.

## Usage

Run the script from the project root:

```bash
python weather_CLI.py
```

Typical interaction:

1. Enter a city name when prompted.
2. The script prints the top 10 matching locations (numbered 1–10).
3. Enter the number corresponding to the correct city to fetch its 10-day forecast.
4. After viewing the forecast you will be asked:
	 - "Would you like to view the original list of cities again? y/n:"
		 - `y`: the 1–10 list is displayed again so you can choose another city.
		 - `n`: you will be asked "Please Enter to exit the program or type 'restart' to select another city:" —
			 press Enter to quit, or type `restart` to relaunch the script and start over.

## Example

Enter `San Francisco` at the city prompt. When the top-10 list appears, type the number (for example `1`) and press Enter.
The program prints a formatted 10-day forecast including high/low temperatures and a human-friendly weather description.

## Troubleshooting

- If the geocoding service returns no results, try a more specific name (e.g., add country or state).
- Network errors: check connectivity and retry.
- If forecasts fail to load, verify the Open-Meteo service is reachable and the coordinates returned by geocoding are valid.

