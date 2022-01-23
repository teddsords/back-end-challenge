from flask import Blueprint, render_template
from .cache import cache
import os
import requests

temperature_get = Blueprint('temperature_get', __name__, template_folder= '../templates')

@temperature_get.route('/temperature/<string:city_name>')
def get_weather(city_name):
    city_name = city_name.lower()       # Lower string to have more control withou worring how the user wrote it
    cache_ttl = int(os.environ.get('CACHE_TTL'))     # Getting cache_ttl from environment variables, converting to int because it return string
    default_max_number = int(os.environ.get('DEFAULT_MAX_NUMBER'))  # Getting default max number from environment variables, converting to int because it return string
    
    keys = cache.get('id')              # Getting the ids from cache to verify if it was queried before
    if keys == None:                    # If there are no ids in cache
        keys = []                       # Create variable for storing them later on

    data = cache.get(city_name)         # Looking for data stored in cache
    if data == None:                    # If data is not stored, do the GET request

        api_key = os.environ.get('OPEN_WEATHER_API_KEY')    # Getting API key from environment variables
        url= f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'       # URL for making get request

        resp= requests.get(url).json()  # Getting response in JSON format
        
        weather = {                     # Formatting response into dict format
            'min_temp': round(resp['main']['temp_min']), 
            'max_temp': round(resp['main']['temp_max']),
            'temp': round(resp['main']['temp']),
            'real_feel': round(resp['main']['feels_like']),
            'city': resp['name'],
            'country': resp['sys']['country']
        }

        print('Got it by a get request') # Printing in console that we got it from a GET request
        
        while len(keys) >= default_max_number:      # If there are more than 5 cities in cache, we need to get rid of them until we have only 5
            keys.pop(0)                   # Getting rid of the older cities
    
        keys.append(city_name)            # Adding city name to the list
        cache.set(city_name, weather, timeout= cache_ttl)       # Adding weather data to cache
        cache.set('id', keys, timeout= cache_ttl)               # Adding city name to cache and using it as id
        return render_template("result.html", weather=weather)  # Rendering page
    
    else:       # Getting data from cache, since is already stored, there is no need to do a GET request once again, speeding up process
        print('Got it from cache')      # Printing in console that we got data from cache
        return render_template("result.html", weather=data)     # Rendering page with data from cache