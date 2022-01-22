from flask import Flask, render_template
import requests
from flask_caching import Cache, request
import os

cache = Cache()     # Creating a cache object
app = Flask(__name__)   # Creating our Flask app
app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
cache.init_app(app)     # Initiating cache


@app.route('/temperature/<string:city_name>')
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

    
@app.route('/temperature')
def get_weather_from_cache():
    # get data from cache using the number specified by the user or using the default max number
    input_number = request.args.get('max')      # Returns None if no number is provided

    if input_number == None:        # There is no need to use default number because it is done in /temperature/<city_name> route

        data = cache.get('id')
        if data == None:
            return '<h1>No data to show </h1>'
        print(data)

        datas = []
        for key in data:
            if cache.get(key) != None:
                datas.append(cache.get(key))

        print(datas)
        return render_template("cache_result.html", weather=datas)

    else:       # Return the amount of queried cities specified in query

        data = cache.get('id')
        if data == None:
            return '<h1>No data to show </h1>'
        print(data)

        datas = []
        for x in range(int(input_number)):
            city = data[x]
            if cache.get(city) != None:
                datas.append(cache.get(city))

        print(datas)
        return render_template("cache_result.html", weather=datas)

if __name__ == "__main__":
    app.run(debug=True)
