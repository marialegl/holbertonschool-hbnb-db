#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.amenities import Amenities
from persistence.data_manager import DataManager


app = Flask(__name__)
data_manager = DataManager()
app.config['data_manager'] = data_manager  

@app.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    amenity = Amenities(name=data['name'], place=data.get('place', ''))
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = list(data_manager.storage.get("Amenities", {}).values())
    return jsonify(amenities), 200

@app.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity), 200

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")
    amenity_instance = Amenities(**amenity)
    data_manager.update(amenity_instance)
    return jsonify(amenity_instance.to_dict()), 200

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")
    data_manager.delete(amenity_id, 'Amenities')
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
