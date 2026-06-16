import requests
import json
from datetime import datetime

"""
App workflow:

1. Ask the user for a city name.
2. Use Open-Meteo's geocoding API to search for that city.
3. Extract latitude and longitude from the geocoding results.
4. Use Open-Meteo's forecast API with those coordinates.
5. Pull out basic weather values (e.g., temperature).
6. Print the weather information clearly in the terminal.

This script is a simple command-line weather client using Open-Meteo APIs.
"""


print("Welcome to the Weather CLI!")
city = input("Please enter the city name: ")


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
    print(f"You selected: {selected_city['name']}, {selected_city['admin1']}")
    print(f"The latitude and longitude of {selected_city['name']} are: {selected_city['latitude']}, {selected_city['longitude']}")


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


now = datetime.now()
day_text = now.strftime("%d")
month_text = now.strftime("%m")


forecast_data = requests.get(forecast_url).json() 
print(forecast_data["daily"]["time"])
print(forecast_data["daily"]["temperature_2m_max"])

print(forecast_data["daily"]["weather_code"])


#Format forcast data into a more readable format for the user. 
format_forecast = []
for i in range(len(forecast_data["daily"]["time"])):
    date = forecast_data["daily"]["time"][i]
    max_temp = forecast_data["daily"]["temperature_2m_max"][i]
    min_temp = forecast_data["daily"]["temperature_2m_min"][i]
    weather_code = forecast_data["daily"]["weather_code"][i]
    format_forecast.append(f"Date: {date}, Max Temp: {max_temp}°F, Min Temp: {min_temp}°F, Weather Code: {weather_code}")
print(f"\n1 Here is the 10-Day Weather Forecast for {selected_city['name']}:")
for forecast in format_forecast:
    print(forecast)