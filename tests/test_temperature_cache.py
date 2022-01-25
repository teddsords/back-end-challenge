from flask import Flask
from routes.temperature_queried_cities import temperature_queried_cities
from routes.temperature_get import temperature_get
from routes.cache import cache
import json
from flask_caching import request
from models.models import Weather, ListOfWeathers


def test_getting_temperature_from_cache():
    '''
    GIVEN a list of city names to query
    WHEN requesting weather via GET method
    THEN weather is then retrieved from cache
    '''

    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.register_blueprint(temperature_queried_cities)
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)

    client = app.test_client()
    city_names = ['London', 'Berlin', 'Milan', 'Tegucigalpa', 'Concord', 'Blumenau']

    for city in city_names:
        response = client.get(f'/temperature/{city}')

    response = client.get('/temperature')
    data= ListOfWeathers(**json.loads(response.get_data(as_text=True)))

    assert city_names[1] == data.weathers[0].city_name
    assert city_names[2] == data.weathers[1].city_name
    assert city_names[3] == data.weathers[2].city_name
    assert city_names[4] == data.weathers[3].city_name
    assert city_names[5] == data.weathers[4].city_name
    assert len(data.weathers) == 5
    
def test_getting_temperature_from_cache_with_argument():
    '''
    GIVEN a list of city names to query and a query argument
    WHEN requesting weather via GET method and afterwards get given argument from cache
    THEN weather is then retrieved from cache
    '''

    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.register_blueprint(temperature_queried_cities)
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)

    client = app.test_client()
    city_names = ['London', 'Berlin', 'Milan', 'Tegucigalpa']

    for city in city_names:
        response = client.get(f'/temperature/{city}')
    
    response = client.get('/temperature?max=3')
    data= ListOfWeathers(**json.loads(response.get_data(as_text=True))) 

    assert city_names[0] == data.weathers[0].city_name
    assert city_names[1] == data.weathers[1].city_name
    assert city_names[2] == data.weathers[2].city_name
    assert len(data.weathers) == 3

def test_no_data_to_show():
    '''
    GIVEN no parameter and no data to sow
    WHEN entering endpoint
    THEN no data to show message is displayed
    '''

    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.register_blueprint(temperature_queried_cities)
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)
    client = app.test_client()
    response = client.get('/temperature')

    assert response.status_code == 404