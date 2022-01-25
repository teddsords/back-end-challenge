from flask import Flask
from routes.cache import cache
from routes.temperature_get import temperature_get
from routes.temperature_queried_cities import temperature_queried_cities
from flasgger import Swagger

app = Flask(__name__)   # Creating our Flask app
app.register_blueprint(temperature_get)     # Adding blueprint for supporting route in another file
app.register_blueprint(temperature_queried_cities)      # Same as before
app.config['CACHE_TYPE'] = 'simple' # Configuring cache type
cache.init_app(app)     # Initiating cache

swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=True)
