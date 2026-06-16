import requests
import json
from datetime import datetime

"""
Checklist:

1. Make output more cleaner
2. Find more paramaters to pull from the API

"""


with open("weather_codes.json", "r") as file:
    weather_codes = json.load(file)


print("Welcome to the Weather CLI!")
city = input("Please enter the city name: ")


def format_forecast_date(date_text):
    forecast_date = datetime.strptime(date_text, "%Y-%m-%d")
    month_text = forecast_date.strftime("%B")
    day_number = forecast_date.day
    day_of_week = forecast_date.strftime("%A")

    if 10 <= day_number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_number % 10, "th")

    return f"{day_of_week}, {month_text} {day_number}{suffix}"


#Open-Meteo's geocoding API to find that city
gecoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}" #using f-string to insert the city name into the URL
response = requests.get(gecoding_url) #This line sends a GET request to the geocoding API and stores the response in the variable 'response'
data = response.json() #This line converts the response from the API into a JSON format and stores it in the variable 'data'



#Need to figure out a way to structure this better, maybe a loop to print the city names and their corresponding admin1 (state/province) from the results list in the JSON data.


#Print enumerate list of city names
print(f"Here is the top ten results for \"{city}\":")
city_range = (0, 11)

for index, result in enumerate(data["results"][city_range[0]:city_range[1]], start=1):
    print(f"{index}. {result['name']}, {result['admin1']}")



city_selection = int(input("Please select the number corresponding to the correct city: "))
if city_selection < 1 or city_selection > 10:
    print("Invalid selection. Please select a number between 1 and 10.")
else:
    selected_city = data['results'][city_selection - 1] #This line selects the city from the results list based on the user's selection. The index is adjusted by subtracting 1 because list indices start at 0.
    #print(f"The latitude and longitude of {selected_city['name']} are: {selected_city['latitude']}, {selected_city['longitude']}")


latitude = selected_city['latitude'] #This line extracts the latitude of the city from the JSON data. 
longitude = selected_city['longitude'] #This line extracts the longitude of the city from the JSON data

# Use open Metro's forecast API with those coordinates and pull out simple weather values (e.g., temperature)

forecast_url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}" #Grabs the latitude and longitude from the selected city
    f"&longitude={longitude}"
    f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
    f"&temperature_unit=fahrenheit"
    f"&forecast_days=10"
)


forecast_data = requests.get(forecast_url).json() 
#Format forcast data into a more readable format for the user. 
format_forecast = []
for i, date in enumerate(forecast_data["daily"]["time"]):
    formatted_date = format_forecast_date(date)
    max_temp = forecast_data["daily"]["temperature_2m_max"][i]
    min_temp = forecast_data["daily"]["temperature_2m_min"][i]
    weather_code = forecast_data["daily"]["weather_code"][i]
    weather_description = weather_codes.get(str(weather_code), "Unknown weather code")
    format_forecast.append(f"{formatted_date}, Max Temp: {max_temp}F, Min Temp: {min_temp}F, Conditions: {weather_description}")
print(f"\n Here is the 10-Day Weather Forecast for {selected_city['name']}, {selected_city['admin1']}:")
for forecast in format_forecast: 
    print(f"\n{forecast}")




"Best example output:"

"""
========================================
  10-Day Weather Forecast
  Boise, Idaho
========================================

Put each day on its own "card"

Tuesday, June 16th
  Weather: Overcast
  High:    93.6°F
  Low:     60.4°F

Weather icons

☀ Clear sky
☁ Overcast
🌧 Light rain
⛈ Thunderstorm
❄ Snow

Round temperatures:

93.6°F → 94°F

Add spaces between each city in the search results to make it easier to read:

"""