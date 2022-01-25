from flask import Blueprint, request
from .cache import cache
import os
import requests
from dotenv import  load_dotenv
from models.models import Weather
from typing import Union
load_dotenv()

temperature_get = Blueprint('temperature_get', __name__, template_folder= '../templates')

@temperature_get.route('/temperature/<string:city_name>')
def get_weather(city_name: str)-> Union[Weather, str]:

    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: city_name
        in: path
        type: string
        required: true
    definitions:
      Weather:
        type: object
        properties:
          city_name:
            type: string
          country:
            type: string
          min_temp:
            type: integer
          max_temp:
            type: integer
          temp:
            type: integer
          real_feel:
            type: integer
    responses:
      200:
        description: Weather object with information retrieved from Open Weather API
        schema:
          $ref: '#/definitions/Weather'
        examples:
          Weather:
            city_name: 
                value: Itajai
            country: BR
            min_temp: 22
            max_temp: 34
            temp: 28
            real_feel: 30
      404:
        description: HTTP error Not Found       
    """
    city_name = city_name.lower()       # Lower string to have more control withou worring how the user wrote it
    cache_ttl = int(os.getenv('CACHE_TTL'))     # Getting cache_ttl from environment variables, converting to int because it return string
    default_max_number = int(os.getenv('DEFAULT_MAX_NUMBER'))  # Getting default max number from environment variables, converting to int because it return string
    
    keys = cache.get('id')              # Getting the ids from cache to verify if it was queried before
    if keys == None:                    # If there are no ids in cache
        keys = []                       # Create variable for storing them later on

    data: Weather = cache.get(city_name)         # Looking for data stored in cache
    if data == None:                    # If data is not stored, do the GET request

        api_key = os.getenv('OPEN_WEATHER_API_KEY')    # Getting API key from environment variables
        url= f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'       # URL for making get request

        resp= requests.get(url).json()  # Getting response in JSON format
        
        if resp['cod'] == 200:
            weather= Weather(min_temp=round(resp['main']['temp_min']),
            max_temp= round(resp['main']['temp_max']),
            temp= round(resp['main']['temp']),
            real_feel=round(resp['main']['feels_like']),
            city_name= resp['name'],
            country= resp['sys']['country'])

            print('Got it by a get request') # Printing in console that we got it from a GET request
            
            while len(keys) >= default_max_number:      # If there are more than 5 cities in cache, we need to get rid of them until we have only 5
                keys.pop(0)                   # Getting rid of the older cities
        
            keys.append(city_name)            # Adding city name to the list
            cache.set(city_name, weather, timeout= cache_ttl)       # Adding weather data to cache
            cache.set('id', keys, timeout= cache_ttl)               # Adding city name to cache and using it as id
            return weather.dict() 
            
        else:
            return resp, resp['cod']

    else:       # Getting data from cache, since is already stored, there is no need to do a GET request once again, speeding up process
        print('Got it from cache')      # Printing in console that we got data from cache
        weather = Weather(min_temp=round(data.min_temp),
            max_temp= round(data.max_temp),
            temp= round(data.temp),
            real_feel=round(data.real_feel),
            city_name= data.city_name,
            country= data.country)
        return weather.dict()