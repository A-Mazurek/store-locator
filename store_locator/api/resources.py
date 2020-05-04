import requests

from typing import Dict, List, Any, Tuple
from .config import STORAGE_FOLDER, DATA_FILE
from .utils import read_file
from .serializers import CitesList, CitesInRangeList
from flask_restful import Resource
from .cache import cache
from flask import request
from geopy.distance import geodesic
from marshmallow import ValidationError


class ListCitiesBase(Resource):
    schema = CitesList(many=True)

    @cache.cached(key_prefix='stores_data')
    def get_data(self) -> List[Dict[str, str]]:
        return read_file(f'{STORAGE_FOLDER}/{DATA_FILE}')

    def get(self) -> List[Dict[str, Any]]:
        data = self.get_data()
        return self.schema.dump(data)


class ListCities(ListCitiesBase):
    """
        Returns a list of all cities.
    """

    pass


class ListCitiesInRange(ListCitiesBase):
    """
        Return list of cities within a given range.
        postcode: string
        range: float - range in kilometers
    """
    schema = CitesInRangeList(many=True)

    def get_data(self) -> List[Dict[str, Any]]:
        data = super().get_data()
        self.set_postcode_and_range()
        lat, lon = self.fetch_lat_and_lon()
        cities_in_range = self.find_cities_in_range((lat, lon), data)
        return cities_in_range

    def set_postcode_and_range(self) -> None:
        self.postcode = request.args.get('postcode')
        try:
            self.range = float(request.args.get('range'))
        except ValueError:
            self.raise_validation_error(f'"range": {request.args.get("range")} is not a valid number.')

    def raise_validation_error(self, message: str) -> None:
        raise ValidationError(message)

    def fetch_lat_and_lon(self) -> Tuple[float, float]:
        response = requests.get(f'https://api.postcodes.io/postcodes/{self.postcode}')
        if response.status_code == 200:
            result = response.json()['result']
            return result['latitude'], result['longitude']
        else:
            self.raise_validation_error(f'"postcode": {self.postcode} is not a valid postcode.')

    def find_cities_in_range(
        self, coordinates: Tuple[float, float], data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        cities_in_range = []
        for city in data:
            distance = geodesic(coordinates, (city['latitude'], city['longitude'])).kilometers
            if distance <= self.range:
                city['distance'] = f'{distance} km'
                city['distance_float'] = distance
                cities_in_range.append(city)
        cities_in_range.sort(key=lambda x: x['distance_float'])
        return cities_in_range
