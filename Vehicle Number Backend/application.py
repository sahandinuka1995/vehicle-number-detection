from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
import json
import base64

application = Flask(__name__)

application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@aaxunchuu0gulp.c8pmpqzflrw9.us-east-1.rds.amazonaws.com:3306/ebdb"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    number = db.Column(db.String(120), unique=False, nullable=False)
    regdate = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def __init__(self, id, name, number, regdate):
        self.id = id
        self.name = name
        self.number = number
        self.regdate = regdate


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
    print(vehicle)
    for i in vehicle:
        print(i.name)

    return make_response(jsonify({
        "success": "true",
        "status": "200",
        "data": ''
    }), 200)


@application.route("/all-vehicle/")
def all_vehicle():
    vehicles = Vehicle.query.filter_by().all()
    print(json.dumps(vehicles))
    return make_response(jsonify({
        "success": "true",
        "status": "200",
        "data": ''
    }), 200)


@application.route("/add-vehicle/")
def add_vehicle():
    name = request.args.get('name')
    number = request.args.get('number')
    regdate = request.args.get('regdate')

    vehicle = Vehicle(name=name, number=number, regdate=regdate)
    db.session.add(vehicle)
    db.session.commit()

    return make_response(jsonify({
        "success": "true",
        "msg": "Vehicle added successfully!",
        "status": "200",
        "data": {
            "name": name,
            "number": number,
            "regDate": regdate
        }
    }), 200)


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
