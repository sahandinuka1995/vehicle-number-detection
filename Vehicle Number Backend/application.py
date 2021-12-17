from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
import json
from json import JSONEncoder
import base64
from flask_cors import CORS, cross_origin

application = Flask(__name__)
cors = CORS(application)

# application.config[
#     'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@aaxunchuu0gulp.c8pmpqzflrw9.us-east-1.rds.amazonaws.com:3306/ebdb"
application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/ebdb"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['CORS_HEADERS'] = 'Content-Type'


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    vehicleNo = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.String(100), unique=False, nullable=False)
    colour = db.Column(db.String(100), unique=False, nullable=False)
    type = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def __init__(self, name, vehicleNo, model, colour, type):
        self.name = name
        self.vehicleNo = vehicleNo
        self.model = model
        self.colour = colour
        self.type = type

    def toString(self):
        return self.name + '' + self.vehicleNo + '' + self.model + '' + self.colour + '' + self.type


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    vehicleNo = db.Column(db.String(200), unique=False, nullable=False)

    def __init__(self, id, email, password, vehicleNo):
        self.id = id
        self.email = email
        self.password = password
        self.vehicleNo = vehicleNo


db.create_all()
db.session.commit()


@application.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@application.route("/search-vehicle/")
def search_vehicle():
    name = request.args.get('name')

    vehicle = Vehicle.query.filter_by().all()
    print(Vehicle.toString(vehicle))

    return make_response(jsonify({
        "success": "true",
        "status": "200",
        "data": ''
    }), 200)


@application.route("/all-vehicle/")
@cross_origin()
def all_vehicle():
    vehicles = Vehicle.query.filter_by().all()
    for i in vehicles:
        print(type(i))

    return make_response(jsonify({
        "success": "true",
        "status": "200",
        "data": ''
    }), 200)


@application.route("/add-vehicle", methods=['POST'])
@cross_origin()
def add_vehicle():
    data = request.get_json()
    result = ''
    try:
        vehicle = Vehicle(name=data['name'], vehicleNo=data['vehicleNo'], model=data['model'], colour=data['colour'],
                          type=data['type'])
        db.session.add(vehicle)
        db.session.commit()

        result = make_response(jsonify({
            "success": "true",
            "msg": "Vehicle added successfully!",
            "status": "200"
        }), 200)
    except:
        result = make_response(jsonify({
            "success": "false",
            "msg": "Something went wrong",
            "status": "500"
        }), 500)

    return result


@application.route('/register/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    vehicleNo = request.form.get('vehicleNo')

    user = User(email=email, password=base64.b64encode(password), vehicleNo=vehicleNo)
    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({
        "success": "true",
        "msg": "User added successfully!",
        "status": "200"
    }), 200)
