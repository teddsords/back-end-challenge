from flask import Blueprint, render_template
from flask_caching import request
from .cache import cache
import json

temperature_queried_cities = Blueprint('temperature_queried_cities', __name__, template_folder='../templates')

@temperature_queried_cities.route('/temperature')
def get_weather_from_cache():
    # get data from cache using the number specified by the user or using the default max number
    input_number = request.args.get('max')      # Returns None if no number is provided

    if input_number == None:        # There is no need to use default number because it is done in /temperature/<city_name> route

        data = cache.get('id')
        if data == None:
            return json.dumps('No data to show'), 404

        datas = []
        for key in data:
            if cache.get(key) != None:
                datas.append(cache.get(key))

        return json.dumps(datas)

    else:       # Return the amount of queried cities specified in query

        data = cache.get('id')
        if data == None:
            return json.dumps('No data to show'), 404

        datas = []
        for x in range(int(input_number)):
            city = data[x]
            if cache.get(city) != None:
                datas.append(cache.get(city))

        return json.dumps(datas)