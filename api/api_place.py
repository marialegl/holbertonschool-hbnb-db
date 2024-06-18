#!usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.place import Place
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

# Helper function to find city and amenities by ID
def find_city(city_id):
    return data_manager.get(city_id, 'City')

def find_amenities(amenity_ids):
    return [data_manager.get(amenity_id, 'Amenity') for amenity_id in amenity_ids]

# Helper function to include detailed city and amenities information in place data
def add_detailed_info(place):
    city = find_city(place['city'])
    amenities = find_amenities([amenity['id'] for amenity in place['amenities']])
    place['city'] = city
    place['amenities'] = amenities
    return place

# Validation functions
def validate_coordinates(latitude, longitude):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        abort(400, description="Invalid geographical coordinates")

def validate_non_negative_integer(value, field_name):
    if not isinstance(value, int) or value < 0:
        abort(400, description=f"{field_name} must be a non-negative integer")

def validate_price(price):
    if not isinstance(price, (int, float)) or price < 0:
        abort(400, description="Price per night must be a valid non-negative numerical value")

def validate_city_id(city_id):
    if not find_city(city_id):
        abort(400, description="Invalid city_id, city does not exist")

def validate_amenity_ids(amenity_ids):
    for amenity_id in amenity_ids:
        if not data_manager.get(amenity_id, 'Amenity'):
            abort(400, description=f"Invalid amenity_id {amenity_id}, amenity does not exist")

# Endpoint to create a new place
@app.route('/places', methods=['POST'])
def create_place():
    data = request.json
    if not data:
        abort(400, description="Invalid input")

    # Validate inputs
    validate_coordinates(data.get('latitude'), data.get('longitude'))
    validate_non_negative_integer(data.get('number_of_rooms'), 'number_of_rooms')
    validate_non_negative_integer(data.get('number_of_bathrooms'), 'number_of_bathrooms')
    validate_non_negative_integer(data.get('max_guests'), 'max_guests')
    validate_price(data.get('price_per_night'))
    validate_city_id(data.get('city_id'))
    validate_amenity_ids(data.get('amenity_ids', []))

    new_place = Place(
        name=data.get('name'),
        description=data.get('description'),
        address=data.get('address'),
        city=find_city(data.get('city_id')),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        host=data.get('host_id'),
        number_of_rooms=data.get('number_of_rooms'),
        number_bathrooms=data.get('number_of_bathrooms'),
        price_per_night=data.get('price_per_night'),
        max_guests=data.get('max_guests'),
        amenities=find_amenities(data.get('amenity_ids', []))
    )

    data_manager.save(new_place)

    return jsonify(new_place.to_dict()), 201

# Endpoint to get a list of all places
@app.route('/places', methods=['GET'])
def get_places():
    places = data_manager.get_all()
    detailed_places = [add_detailed_info(place) for place in places]
    return jsonify(detailed_places), 200

# Endpoint to get details of a specific place
@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")
    detailed_place = add_detailed_info(place)
    return jsonify(detailed_place), 200

# Endpoint to update an existing place
@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.json
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    # Validate inputs
    if 'latitude' in data or 'longitude' in data:
        validate_coordinates(data.get('latitude', place['latitude']), data.get('longitude', place['longitude']))
    if 'number_of_rooms' in data:
        validate_non_negative_integer(data.get('number_of_rooms'), 'number_of_rooms')
    if 'number_of_bathrooms' in data:
        validate_non_negative_integer(data.get('number_of_bathrooms'), 'number_of_bathrooms')
    if 'max_guests' in data:
        validate_non_negative_integer(data.get('max_guests'), 'max_guests')
    if 'price_per_night' in data:
        validate_price(data.get('price_per_night'))
    if 'city_id' in data:
        validate_city_id(data.get('city_id'))
    if 'amenity_ids' in data:
        validate_amenity_ids(data.get('amenity_ids', []))

    place['name'] = data.get('name', place['name'])
    place['description'] = data.get('description', place['description'])
    place['address'] = data.get('address', place['address'])
    place['city'] = find_city(data.get('city_id')) if data.get('city_id') else place['city']
    place['latitude'] = data.get('latitude', place['latitude'])
    place['longitude'] = data.get('longitude', place['longitude'])
    place['number_of_rooms'] = data.get('number_of_rooms', place['number_of_rooms'])
    place['number_of_bathrooms'] = data.get('number_of_bathrooms', place['number_of_bathrooms'])
    place['price_per_night'] = data.get('price_per_night', place['price_per_night'])
    place['max_guests'] = data.get('max_guests', place['max_guests'])
    place['amenities'] = find_amenities(data.get('amenity_ids')) if data.get('amenity_ids') else place['amenities']
    place['host'] = data.get('host_id', place['host'])

    data_manager.update(place)

    return jsonify(place), 200

# Endpoint to delete a place
@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    data_manager.delete(place_id, 'Place')

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
