#!/usr/bin/python3
import uuid
from flask import Flask, jsonify, request, abort
from model.city import City
from model.country import Country
import pycountry
from persistence.data_manager import DataManager
from persistence.database import db

app = Flask(__name__)
data_manager = DataManager()

def find_country_by_code(country_code):
    return pycountry.countries.get(alpha_2=country_code.upper())

def validate_city_data(data, is_update=False):
    if 'name' not in data or not data['name'].strip() or 'population' not in data or 'country_code' not in data:
        abort(400, description="Missing required fields: name, population, country_code")
    if not find_country_by_code(data['country_code']):
        abort(404, description=f"Country with code '{data['country_code']}' not found")
    if not is_update:
        existing_city = data_manager.query_all_by_filter(City, City.name == data['name'], City.country_code == data['country_code']).first()
        if existing_city:
            abort(409, description=f"City '{data['name']}' already exists in country '{data['country_code']}'")

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = [{"name": country.name, "iso_3166_1_alpha_2": country.alpha_2} for country in pycountry.countries]
    return jsonify(countries), 200

@app.route('/countries/<country_code>', methods=['GET'])
def get_country_by_code(country_code):
    country = find_country_by_code(country_code)
    if country:
        return jsonify({"id": str(uuid.uuid4()), "name": country.name, "iso_3166_1_alpha_2": country.alpha_2}), 200
    else:
        abort(404, description=f"Country with code '{country_code}' not found")

@app.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    if not find_country_by_code(country_code):
        abort(404, description=f"Country with code '{country_code}' not found")
    country_cities = data_manager.query_all_by_filter(City, City.country_code == country_code.upper())
    return jsonify([city.to_dict() for city in country_cities]), 200

@app.route('/cities', methods=['POST'])
def add_city():
    data = request.get_json()
    validate_city_data(data)
    city = City(name=data["name"], population=data["population"], country_code=data["country_code"].upper())
    data_manager.save(city)
    return jsonify(city.to_dict()), 201

@app.route('/cities', methods=['GET'])
def get_all_cities():
    cities = data_manager.query_all(City)
    return jsonify([city.to_dict() for city in cities]), 200

@app.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    city = data_manager.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        abort(404, description=f"City with ID '{city_id}' not found")

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = data_manager.get(City, city_id)
    if not city:
        abort(404, description=f"City with ID '{city_id}' not found")
    validate_city_data(data, is_update=True)

    city.name = data['name']
    city.population = data['population']
    city.country_code = data['country_code'].upper()
    data_manager.update(city)
    return jsonify(city.to_dict()), 200

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(City, city_id)
    if not city:
        abort(404, description=f"City with ID '{city_id}' not found")
    data_manager.delete(city)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
