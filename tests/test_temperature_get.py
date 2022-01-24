from flask import Flask
from routes.temperature_get import temperature_get
from routes.cache import cache
import json
import time

def test_temperature_get():
    '''
    GIVEN a city name for querying 
    WHEN requesting via GET method
    THEN weather is returned
    '''

    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
    cache.init_app(app)
    client = app.test_client()
    city_name = 'London'
    url = f'/temperature/{city_name}'

    response = client.get(url)
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 
    assert city_name.lower() == data['city'].lower()
    assert  isinstance(data['min_temp'], int)
    assert  isinstance(data['max_temp'], int)
    assert  isinstance(data['temp'], int)
    assert  isinstance(data['real_feel'], int)

def test_temperature_not_found():
    '''
    GIVEN a non-existing city name for querying
    WHEN requesting via GET method
    THEN HTTP error
    '''
    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
    cache.init_app(app)
    client = app.test_client()
    city_name = '!@#$%'
    url = f'/temperature/{city_name}'

    response = client.get(url)

    assert response.status_code == 404

def test_temperature_from_cache():
    '''
    GIVEN a city name to query
    WHEN request, wait for 2 seconds
    THEN get weather from cache
    '''

    app = Flask(__name__)
    app.register_blueprint(temperature_get)
    app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
    cache.init_app(app)
    client = app.test_client()
    city_name = 'Itajai'
    url = f'/temperature/{city_name}'

    response = client.get(url)
    data = json.loads(response.get_data(as_text=True))

    time.sleep(2)

    response = client.get(url)
    data_cache = json.loads(response.get_data(as_text=True))

    assert data == data_cache
