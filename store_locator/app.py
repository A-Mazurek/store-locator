from __future__ import absolute_import
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from app.api.config import APP_CONFIG
from app.api.resources import ListCities, ListCitiesInRange
from app.api.cache import cache


app = Flask("store_locator")
app.config.from_mapping(APP_CONFIG)

api = Api(app)
ma = Marshmallow(app)
cache.init_app(app)


api.add_resource(ListCities, '/cities/')
api.add_resource(ListCitiesInRange, '/cities/in-range/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
