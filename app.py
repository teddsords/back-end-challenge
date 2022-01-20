from flask import Flask
import requests

app = Flask(__name__)

api_key= 'b0e2f7b304d5e48c71b8c9501255bdf8'
min_temp= 0
max_temp= 0
avg_temp= 0
real_feel= 0
city= 'None'
country= 'None'

@app.route('/temperature/<city_name>')
def get_weather(city_name):
    url= f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    resp= requests.get(url).json()
    min_temp= resp['main']['temp_min']
    max_temp= resp['main']['temp_max']
    avg_temp= resp['main']['temp']
    real_feel= resp['main']['feels_like']
    city= resp['name']
    country= resp['sys']['country']

    resp_dict= {
        'minimum temperature': min_temp,
        'maximum temperature': max_temp,
        'average temperature': avg_temp,
        'real feel': real_feel,
        'city': city,
        'country': country
    }
    return   resp_dict

if __name__ == "__main__":
    app.run(debug=True)
