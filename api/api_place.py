#!usr/bin/python3
from flask import Flask, jsonify, request
from model.place import Place
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

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
    pass

if __name__ == '__main__':
    app.run(debug=True)
