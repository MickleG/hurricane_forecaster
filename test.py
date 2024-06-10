import requests
import json

# URL for the NWS forecast data (adjust the endpoint as necessary)
url = 'https://api.weather.gov/gridpoints/MLB/25,69/forecast'

# URL for the NWS gridpoint location data
location_url = 'https://api.weather.gov/gridpoints/MLB/25,69'

# Send a request to the URL for forecast data
response = requests.get(url)

# Send a request to the URL for location data
location_response = requests.get(location_url)

# Check if the requests were successful
if response.status_code == 200 and location_response.status_code == 200:
    # Parse the JSON content
    data = response.json()
    location_data = location_response.json()
    
    # Extract location information based on the printed structure
    try:
        coordinates = location_data['geometry']['coordinates']
        latitude = coordinates[0][1] if len(coordinates) > 0 and len(coordinates[0]) > 1 else None
        longitude = coordinates[0][0] if len(coordinates) > 0 and len(coordinates[0]) > 0 else None

        location_info = {
            'latitude': latitude,
            'longitude': longitude
        }
    except KeyError as e:
        print(f"KeyError: {e}")
        location_info = {'latitude': None, 'longitude': None}
    
    # Extract relevant forecast data
    forecast_data = []
    for period in data['properties']['periods']:
        forecast_dict = {
            'startTime': period['startTime'],
            'endTime': period['endTime'],
            'temperature': period['temperature'],
            'temperatureUnit': period['temperatureUnit'],
            'windSpeed': period['windSpeed'],
            'windDirection': period['windDirection'],
            'shortForecast': period['shortForecast'],
            'detailedForecast': period['detailedForecast'],
            'location': location_info  # Add location information
        }
        forecast_data.append(forecast_dict)
    
    # Save the forecast data to a JSON file
    with open('hurricane_forecast.json', 'w') as json_file:
        json.dump(forecast_data, json_file, indent=4)
    
    print("Hurricane forecast data saved to hurricane_forecast.json")
else:
    print("Failed to retrieve data from the National Weather Service API")
