from typing import Union
from flask import Blueprint, render_template
from flask_caching import request
from .cache import cache
import json
from models.models import ListOfWeathers


temperature_queried_cities = Blueprint('temperature_queried_cities', __name__, template_folder='../templates')

@temperature_queried_cities.route('/temperature')
def get_weather_from_cache()-> Union[ListOfWeathers, str]:
    """Endpoint returning a ListOfWeathers which contains a list of Weather in which weather information is contained
    ---
    parameters:
      - name: max
        in: query
        type: integer
        required: false
    definitions:
        ListOfWeathers:
            type: object
            properties:
                weathers:
                    type: array
                    items: 
                        $ref: '#/definitions/Weather' 
    responses:
      200:
        description: ListOfWeathers object with Weathers array retrieved from cache
        schema:
          $ref: '#/definitions/ListOfWeathers'
        examples:
          ListOfWeathers:
            weathers:
                city_name: Itajai
                country: BR
                min_temp: 22
                max_temp: 34
                temp: 28
                real_feel: 30
      404:
        description: HTTP error Not Found       
    """
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

        weathers= ListOfWeathers(weathers= datas)
        return weathers.dict()

    else:       # Return the amount of queried cities specified in query

        data = cache.get('id')
        if data == None:
            return json.dumps('No data to show'), 404

        datas = []
        for x in range(int(input_number)):
            city = data[x]
            if cache.get(city) != None:
                datas.append(cache.get(city))

        weathers= ListOfWeathers(weathers= datas)
        return weathers.dict()