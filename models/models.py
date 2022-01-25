from lib2to3.pytree import Base
from typing import List
from pydantic import BaseModel

class Weather(BaseModel):
    city_name: str
    country: str
    max_temp: int
    min_temp: int
    real_feel: int
    temp: int

class ListOfWeathers(BaseModel):
    weathers: List[Weather]