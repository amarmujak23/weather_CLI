import requests
import json
from datetime import datetime
import os

def clear():
    # 'nt' means Windows, 'posix' means Mac or Linux
    os.system('cls' if os.name == 'nt' else 'clear')


with open("weather_codes.json", "r", encoding='utf-8') as file:
    weather_codes = json.load(file)

city = input("Please enter the city name: ")
clear()

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


def print_city_list():
    print(f"Here is the top ten results for \"{city}\":")
    print()
    city_range = (0, 11)
    for index, result in enumerate(data["results"][city_range[0]:city_range[1]], start=1):
        print(f"{index}. {result['name']}, {result.get('admin1', '')}")
    print()

def fetch_and_format_forecast(selected_city):
    latitude = selected_city['latitude']
    longitude = selected_city['longitude']
    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
        f"&temperature_unit=fahrenheit"
        f"&forecast_days=10"
    )
    forecast_data = requests.get(forecast_url).json()
    format_forecast = []
    for i, date in enumerate(forecast_data["daily"]["time"]):
        formatted_date = format_forecast_date(date)
        rounded_max_temp = round(forecast_data["daily"]["temperature_2m_max"][i])
        rounded_min_temp = round(forecast_data["daily"]["temperature_2m_min"][i])
        weather_code = forecast_data["daily"]["weather_code"][i]
        weather_description = weather_codes.get(str(weather_code), "Unknown weather code")
        card = f"{formatted_date}\n  Weather: {weather_description}\n  High:    {rounded_max_temp}°F\n  Low:     {rounded_min_temp}°F"
        format_forecast.append(card)
    return format_forecast

def display_forecast(selected_city, format_forecast):
    clear()
    print("========================================")
    print("  10-Day Weather Forecast")
    print()
    print(f"  {selected_city['name']}, {selected_city.get('admin1', '')}")
    print("========================================")
    print()
    for forecast in format_forecast:
        print(forecast)
        print()

# Main selection loop: allow user to re-display the original 1-10 list and choose another city
while True:
    print_city_list()
    try:
        city_selection = int(input("Please select the number corresponding to the correct city: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 10.")
        continue
    if city_selection < 1 or city_selection > 10:
        print("Invalid selection. Please select a number between 1 and 10.")
        continue

    selected_city = data['results'][city_selection - 1]
    format_forecast = fetch_and_format_forecast(selected_city)
    display_forecast(selected_city, format_forecast)

    output_input_1 = input("Would you like to view the original list of cities again? y/n: ")
    if output_input_1.lower() == 'y':
        clear()
        continue
    elif output_input_1.lower() == 'n':
        output_input = input("Please Enter to exit the program or type 'restart' to select another city: ")
        if output_input.lower() == 'restart':
            clear()
            os.system('python weather_CLI.py')
            break
        else:
            break
    else:
        # any other input, exit
        break



# Future improvements:
# - Add error handling for API requests (e.g., network issues, invalid responses)
# - Implement a search feature to filter cities by country or region
# - Add more weather details (e.g., humidity, wind speed) to the forecast display