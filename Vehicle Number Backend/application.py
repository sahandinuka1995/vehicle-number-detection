from dataclasses import dataclass

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
cors = CORS(application)

# application.config[s
#     'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@aaxunchuu0gulp.c8pmpqzflrw9.us-east-1.rds.amazonaws.com:3306/ebdb"
application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/ebdb"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['CORS_HEADERS'] = 'Content-Type'


@dataclass
class Vehicle(db.Model):
    id: int
    name: str
    vehicleNo: str
    model: str
    colour: str
    type: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    vehicleNo = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.String(100), unique=False, nullable=False)
    colour = db.Column(db.String(100), unique=False, nullable=False)
    type = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, name, vehicleNo, model, colour, type):
        self.name = name
        self.vehicleNo = vehicleNo
        self.model = model
        self.colour = colour
        self.type = type

    def __repr__(self):
        return f"['name'=>{self.name}, 'vehicleNo'=>{self.vehicleNo}, 'model'=>{self.model}, 'colour'=>{self.colour}, 'type'=>{self.type}]"


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
    return "<p>Welcome!</p>"


def getAllVehicles():
    try:
        vehicle = Vehicle.query.filter_by().order_by(Vehicle.id.desc()).all()
        return make_response(jsonify({
            "success": "true",
            "status": "200",
            "data": vehicle
        }), 200)
    except:
        return errorResponse()


def addNewVehicle(data):
    try:
        vehicle = Vehicle(name=data['name'], vehicleNo=data['vehicleNo'], model=data['model'],
                          colour=data['colour'],
                          type=data['type'])
        print(vehicle)
        db.session.add(vehicle)
        db.session.commit()

        return make_response(jsonify({
            "success": "true",
            "msg": "Vehicle added successfully!",
            "status": "200"
        }), 200)
    except:
        return errorResponse()


def errorResponse():
    return make_response(jsonify({
        "success": "false",
        "msg": "Something went wrong",
        "status": "500"
    }), 500)


@application.route("/vehicle", methods=['POST', 'GET', 'PATCH', 'PUT', 'DELETE'])
@cross_origin()
def vehicle():
    result = ''

    if request.method == 'GET':
        result = getAllVehicles()

    elif request.method == 'POST':
        data = request.get_json()
        result = addNewVehicle(data)

    return result
