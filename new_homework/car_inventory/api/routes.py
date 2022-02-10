from flask import Blueprint, jsonify, request
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema
api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

# create car route
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    price = request.json['price']
    location = request.json['location']
    ext_color = request.json['ext_color']
    int_color = request.json['int_color']
    odometer = request.json['odometer']
    vin = request.json['vin']
    user_token = current_user_token.token

    # print(f'BIG TESTER: {current_user_token.token}')

    car = Car(year,make,model, price,location,ext_color,int_color, odometer,vin,user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve  all cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve one car
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# update a car
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id) # GET car INSTANCE

    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.price = request.json['price']
    car.location = request.json['location']
    car.ext_color = request.json['ext_color']
    car.int_color = request.json['int_color']
    car.odometer = request.json['odometer']
    car.vin = request.json['vin']
    # car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# delete a car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)