#!/usr/bin/python3
from flask import Flask, jsonify, request

from model.amenities import Amenities
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()


@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if 'name' not in data or not data['name'].strip():
        return jsonify({"error": "Name is required"}), 400

    # Crear una nueva instancia de `Amenities`
    amenity = Amenities(name=data['name'])
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201


@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = data_manager.query_all(Amenities)  # Usar la clase en lugar del nombre
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(Amenities, amenity_id)  # Usar la clase en lugar del nombre
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404
    return jsonify(amenity.to_dict()), 200


@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(Amenities, amenity_id)  # Usar la clase en lugar del nombre
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404

    if 'name' not in data or not data['name'].strip():
        return jsonify({"error": "Name is required"}), 400

    amenity.name = data['name']
    data_manager.update(amenity)
    return jsonify(amenity.to_dict()), 200


@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(Amenities, amenity_id)  # Usar la clase en lugar del nombre
    if not amenity:
        return jsonify({"error": "Amenity not found"}), 404
    data_manager.delete(amenity)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
