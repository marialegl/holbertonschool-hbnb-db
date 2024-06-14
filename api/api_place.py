#!usr/bin/python3
from flask import Flask, jsonify, request
from model.place import Place
from persistence.data_manager import DataManager
from uuid import UUID

app = Flask(__name__)
data_manager = DataManager()

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False

@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()

    place = Place(
        name= data['name'],
        description= data['description'],
        address= data['address'],
        city= data['city'],
        latitude= data['latitude'],
        longitude= data['longitude'],
        host= data['host'],
        number_of_rooms= data['number_of_rooms'],
        number_bathrooms= data['number_bathrooms'],
        price_per_night= data['price_per_night'],
        max_guests= data['max_guests'],
        amenities= data['amenities']
    )

    data_manager.save(place)
    return jsonify(place.to_dict()), 201

@app.route('/places', methods=['GET'])
def get_places():
    places = list(data_manager.storage.get('Place', {}).values())
    return jsonify(places), 200

@app.route('/place/<place_id>', methods=['GET'])
def get_place_by_id(place_id):


    if not is_valid_uuid(place_id):
        return jsonify({"error": "Invalid user ID"}), 400
    
    place = data_manager.get(place_id, "Place")
    if place is None:
        return jsonify({"error": "Place not found"}), 404
    return jsonify(place), 200

@app.route("/place/<place_id>", methods=['PUT'])
def update_place(place_id):

    data = request.get_json()

    if not is_valid_uuid(place_id):
        return jsonify({"error": "Invalid place ID"}), 400

    place = Place(
        name= data['name'],
        description= data['description'],
        address= data['address'],
        city= data['city'],
        latitude= data['latitude'],
        longitude= data['longitude'],
        host= data['host'],
        number_of_rooms= data['number_of_rooms'],
        number_bathrooms= data['number_bathrooms'],
        price_per_night= data['price_per_night'],
        max_guests= data['max_guests'],
        amenities= data['amenities']
    )

    data_manager.update(place)
    return jsonify(place.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
