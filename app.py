from flask import Flask, render_template, request
import requests
from flask_caching import Cache

# Reading API key for OpenWeather
file_open= open('api_key.txt', 'r')
api_key = file_open.read()

cache_ttl = 50     # 300 seconds, since cache uses seconds for timeout
default_max_number = 5      # Defining the number of maximum cities that can be stored in cache

cache = Cache()     # Creating a cache object
app = Flask(__name__)   # Creating our Flask app
app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
cache.init_app(app)     # Initiating cache



@app.route('/temperature/<string:city_name>')
#@cache.memoize(timeout= cache_ttl)
def get_weather(city_name):
    
    url= f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    resp= requests.get(url).json()

    weather = {
        'min_temp': round(resp['main']['temp_min']), 
        'max_temp': round(resp['main']['temp_max']),
        'temp': round(resp['main']['temp']),
        'real_feel': round(resp['main']['feels_like']),
        'city': resp['name'],
        'country': resp['sys']['country']
    }

    return render_template("result.html", weather=weather)
    
@app.route('/temperature')
def get_weather_from_cache():
    # get data from cache using the number specified by the user or using the default max number
    #input_number = request.args.get('max')
    data = cache.get('weather')

    return data

if __name__ == "__main__":
    app.run(debug=True)
