# Open Weather aPI back end challenge
Design and build a wrapper for the Open Weather API current weather data service that returns a city's temperature

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)


# PROJECT STRUCTURE
.
```bash
├── routes
│   ├── __init__.py
│   ├── cache.py
│   ├── temperature_get.py
│   ├── temperature_queried_cities.py
├── tests
│   ├── test_temperature_cache.py
│   ├── test_temperature_get.py
│── __init__.py
├── .gitignore
├── app.py   
├── README.md
└── requirements.txt
```

## Folders
* **back-end-challenge** - Main folder where all the files are located
* **routes** - Folder where endpoint files are located
* **tests** - Folder where tests files are located

## Files
* **back-end-challenge/__init__.py** - File used to create packages
* **back-end-challenge/.gitignore** - File used to ignore files and directories that should not be added to git
* **back-end-challenge/app.py** - File where Flask app is instantiated
* **back-end-challenge/requirements.txt** - File where dependencies are listed
* **routes/__init__.py** - File usedd to create package for importing
* **routes/cache.py** - File where cache is imported
* **routes/temperature_get.py** - File where '/temperature/{city_name}' endpoint is created
* **routes/temperature_queried_cities** - File where '/temperature' endpoint is created
* **tests/test_temperature_cahce.py** - File where '/temperature' endpoint is tested
* **tests/test_temperature_get** - File where '/temperature/{city_name}' endpoint is tested

## End points
1. localhost:5000/temperature?max=<default_max_number>
    - This endpoint gets data from cache of previosly queried cities. 
    - The cache has a time to live of 50 seconds, which is configured by an environment variable.
    - The cache has a maximum size of 5 cities to be stored.
    - The amount of cities to be retrieved from cache canbe specified by passing an integer as a parameter of a query. If the number is not provided, it will be considered the default maximum number of cities, which is defined by a environment variable.
  
2. localhost:5000/temperature/{city_name}
    - This endpoint receives a city name to be queried in the Open Weather API
    - The city name is required, since it is used to execute a GET method on the Open Weather  API
3. localhost:5000/apidocs/
    - This endpoint is where API documentarion can be found and tested
    - Documentarion for Models (ListOfWeathers and Weather) and their respective fields
 
 ## Run Locally
 This repository used the venv approach for executing the code, please follow the steps described below:
 1. Open cmd.
    ```cmd
    git clone https://github.com/teddsords/back-end-challenge.git
    CD back-end-challenge
    ```
 2. Create virtual environment
    ```cmd
    python -m venv env
    ```
 3. Install all dependencies
    ```cmd
    pip install -r requirements.txt
    ```
 4. Create a '.env' file to declare environment variables, for example:
    ```txt
    CACHE_TTL=50
    DEFAULT_MAX_NUMBER=5
    OPEN_WEATHER_API_KEY=API_SECRET_VALUE
    ```
    **Disclosure: PLEASE INSERT YOUR OPEN WEATHER API KEY**
    
 6. Run Flask application
    ```cmd
    python app.py
    ```
 5. Enter 'localhost:5000/apidocs/' by opening your favorite browser and test my API.
 

## TESTING
1. open cmd in back-end-challenge and activate virtual environment
    ```cmd
    venv\Scripts\activate.bat
    ```    
2. With virtual environment running, run automated tests
    ```cmd
    python -m pytest tests\
    ```
3. After running tests deactivate virtual environment
    ```cmd
    deactivate
     ```
