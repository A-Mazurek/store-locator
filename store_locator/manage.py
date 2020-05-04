import json
import sys
import requests
from typing import List, Dict, Any
from api.utils import read_file
from api.config import STORAGE_FOLDER, DATA_FILE


def get_coordinates(postcodes: List[Dict[str, str]]) -> List[Dict[str, Dict[str, Any]]]:
    """
        Fetch latitude and longitude for every postcode from api.postcodes.io.
    """
    payload = {'postcodes': [x['postcode'] for x in postcodes]}
    try:
        response = requests.post('https://api.postcodes.io/postcodes', data=payload)
        return response.json()['result']
    except Exception as e:
        print(e)


def merge_postcode_and_coordinates(
    postcodes: List[Dict[str, str]], response: List[Dict[str, Dict[str, Any]]]
) -> List[Dict[str, str]]:
    """
        Add latitude and longitude  to the original postcodes data.
    """
    response.sort(key=lambda x: x['query'])
    postcodes.sort(key=lambda x: x['postcode'])
    for coordinates, postcode in zip(response, postcodes):
        assert coordinates['query'] == postcode['postcode']

        if result := coordinates.get('result', None):
            lat = result['latitude']
            lon = result['longitude']
        else:
            lat = lon = None
        postcode['latitude'] = lat
        postcode['longitude'] = lon
    return postcodes


def save_to_file(data: List[Dict[str, str]]) -> None:
    with open(f'{STORAGE_FOLDER}/{DATA_FILE}', 'w') as f:
        json.dump(data, f)


def import_data(file_name):
    postcodes = read_file(file_name)

    response = get_coordinates(postcodes)

    data = merge_postcode_and_coordinates(postcodes, response)

    save_to_file(data)

    print("All postcodes has been imported")


if __name__ == "__main__":
    import_data(sys.argv[2])
