import requests
import json


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

# Need to ask for user input to select city

latitude = data['results'][0]['latitude'] #This line extracts the latitude of the city from the JSON data. 
longitude = data['results'][0]['longitude'] #This line extracts the longitude of the city from the JSON data
#print(f"The latitude and longitude of {city} are: {latitude}, {longitude}")

forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"

# Use open Metro's forecast API with those coordinates and pull out simple weather values (e.g., temperature)


"""
print(response.status_code)
if response.status_code == 200:
    print("Pass")
"""    