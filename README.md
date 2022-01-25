# back-end-challenge
Design and build a wrapper for the Open Weather API current weather data service that returns a city's temperature

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

# TESTING
1. activate venv
venv\Scripts\activate.bat

2. To run automated tests 
python -m pytest tests\

3. After running tests deactivate venv
deactivatede
