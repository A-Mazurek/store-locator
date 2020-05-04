# Stores Locator

Data provided for this app takes only 904 bytes in total. It is a static list of cites. I dicided that it is too smnall to include any kind of database. Instead the initial data is combined with coordinates and stored back as a json file. To reduce the response time it is cached in flask simple memory cache for an hour.

## Setup

To build this app locally use:
```bash
docker-compose build
```
Then you can start it with:
```bash
docker-compose up
```
Data Import
```bash
docker-compose run --rm web python manage.py import_data data_storage/stores.json
```
File should be in a json format.
It will load the list of cities, and fetch the coordinates for all of them from [postcode.io](https://postcodes.io/)

## Usage

#### Endpoints

##### List Stores

GET `/cities/`
It will list all cities present in the app, ordered by postcode.

##### List Stores In Range

GET `/cities/in-range/`
It will list all cities in the given range from the given postcode.
Expected parameters:
- postcode - valid postcode from around the world.
- range - a distance from the postcode in kilometers

###### Full Example

`/cities/in-range/?postcode=WC2R%202LS&range=500`

#### Management commands

##### Data Import

```bash
docker-compose run --rm web python manage.py import_data <file_fath/file_name>
```
File should be in a json format.
It will load the list of cities, and fetch the coordinates for all of them from [postcode.io](https://postcodes.io/)

### Dependencies

```bash
Flask==1.1.2
Flask-Caching==1.8.0
flask-marshmallow==0.12.0
Flask-RESTful==0.3.8
Flask-Script==2.0.6
geopy==1.21.0
requests==2.23.0
```

### Third party API's

- [postcode.io](https://postcodes.io/)

### Updating dependencies

Modify `requirements.in` file and run the command below, to pin down the dependecies versions.
```bash
docker-compose run --rm web pip-compile --generate-hashes requirements.in --output-file requirements.txt
```