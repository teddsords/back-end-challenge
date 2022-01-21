from flask import Flask, render_template, request
import requests
from flask_caching import Cache

cache = Cache()

app = Flask(__name__)
cache.init_app(app)

file_open= open('api_key.txt', 'r')
api_key = file_open.read()

@app.route('/temperature/<city_name>')
def get_weather(city_name):
    url= f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    resp= requests.get(url).json()
    min_temp= round(resp['main']['temp_min'])
    max_temp= round(resp['main']['temp_max'])
    avg_temp= round(resp['main']['temp'])
    real_feel= round(resp['main']['feels_like'])
    city= resp['name']
    country= resp['sys']['country']

    return render_template("result.html", min_temp=min_temp, max_temp=max_temp, avg_temp=avg_temp,
    real_feel=real_feel, city=city, country=country)
    

if __name__ == "__main__":
    app.run(debug=True)
