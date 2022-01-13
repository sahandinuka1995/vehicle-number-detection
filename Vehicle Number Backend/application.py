from dataclasses import dataclass

from flask import Flask, request, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import pytesseract as tess
from werkzeug.utils import secure_filename, redirect
import os
import urllib.request
import cv2
from flask_awscognito import AWSCognitoAuthentication

application = Flask(__name__)
UPLOAD_FOLDER = 'data/vehicles/'
cors = CORS(application)

# application.config[s
#     'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@aaxunchuu0gulp.c8pmpqzflrw9.us-east-1.rds.amazonaws.com:3306/ebdb"
application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/ebdb"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['CORS_HEADERS'] = 'Content-Type'
application.secret_key = "secret key"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

application.config['AWS_DEFAULT_REGION'] = 'eu-west-1'
application.config['AWS_COGNITO_DOMAIN'] = 'https://sahan-flask-app.auth.us-east-1.amazoncognito.com'
application.config['AWS_COGNITO_USER_POOL_ID'] = 'us-east-1_XL5t7GWlN'
application.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = 'gmkkii61vfqi4b1s1iismls9t'
application.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = 'stgbv3b1bpucrpb7fh6g7rbv3nh0dv4g4pi5b1740o9b36mi02r'
application.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5000/success'

aws_auth = AWSCognitoAuthentication(application)


@dataclass
class Vehicle(db.Model):
    id: int
    name: str
    vehicleNo: str
    model: str
    colour: str
    type: str
    # image: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    vehicleNo = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.String(100), unique=False, nullable=False)
    colour = db.Column(db.String(100), unique=False, nullable=False)
    type = db.Column(db.String(100), unique=False, nullable=False)

    # image = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, name, vehicleNo, model, colour, type):
        self.name = name
        self.vehicleNo = vehicleNo
        self.model = model
        self.colour = colour
        self.type = type
        # self.image = image

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/")
def hello_world():
    return "<p>Welcome!</p>"


def getAllVehicles():
    all = Vehicle.query.all()

    return make_response(jsonify({
        "success": True,
        "status": "200",
        "data": all
    }), 200)


import boto3

s3 = boto3.resource('s3')

client = boto3.client(
    's3',
    aws_access_key_id="AKIAVWQ26W5I5VEIOOU2",
    aws_secret_access_key="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"
)


def addNewVehicle(data):
    vehicle = Vehicle(name=data.form['name'], vehicleNo=data.form['vehicleNo'], model=data.form['model'],
                      colour=data.form['colour'],
                      type=data.form['type'])

    db.session.add(vehicle)
    db.session.commit()
    try:
        # vehicle = Vehicle(name=data.form['name'], vehicleNo=data.form['vehicleNo'], model=data.form['model'], colour=data.form['colour'],
        #                   type=data.form['type'])
        #
        # db.session.add(vehicle)
        # db.session.commit()

        return make_response(jsonify({
            "success": True,
            "msg": "Vehicle update successfully!",
            "status": "200",
        }), 200)

    except:
        return errorResponse()


def updateVehicle(data):
    try:
        vehicle = Vehicle.query.filter_by(id=data['id']).first()
        vehicle.name = data['name']
        vehicle.vehicleNo = data['vehicleNo']
        vehicle.model = data['model']
        vehicle.colour = data['colour']
        vehicle.type = data['type']
        db.session.commit()

        return make_response(jsonify({
            "success": "true",
            "msg": "Vehicle update successfully!",
            "status": "200"
        }), 200)
    except:
        return errorResponse()


def deleteVehicle(data):
    try:
        Vehicle.query.filter_by(id=request.args.get('id')).delete()
        db.session.commit()
        return make_response(jsonify({
            "success": "true",
            "msg": "Vehicle deleted successfully!",
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
        result = addNewVehicle(request)

    elif request.method == 'PUT':
        data = request.get_json()
        result = updateVehicle(data)

    elif request.method == 'DELETE':
        data = request.get_json()
        result = deleteVehicle(data)

    return result


@application.route("/getNumber", methods=['POST'])
@cross_origin()
def imageToText():
    result = ''

    if request.method == 'POST':
        try:
            file = request.files['file']

            file_name = secure_filename(file.filename)
            file.save(file_name)

            bucket_name = "sample-bucket-sahan"
            response = client.upload_file(file_name, bucket_name, file_name, ExtraArgs={
                'ACL': 'public-read'
            })

            bucket_name = "sample-bucket-sahan"
            res = client.download_file(bucket_name, file_name, '/New_Project_2.jpg')

            tess.pytesseract.tesseract_cmd = r'D:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
            from PIL import Image

            img = Image.open(file_name)
            text = tess.image_to_string(img)

            return make_response(jsonify({
                "success": True,
                "status": "200",
                "data": text
            }), 200)

        except:
            return errorResponse()

    return result


@application.route("/dashboard", methods=['GET'])
@cross_origin()
def dashboard():
    try:
        vehicle = Vehicle.query.filter_by().count()
        return make_response(jsonify({
            "success": "true",
            "data": {
                "noOfVehicles": vehicle
            },
            "status": "200"
        }), 200)
    except:
        return errorResponse()


@application.route('/auth')
@cross_origin()
@aws_auth.authentication_required
def index():
    claims = aws_auth.claims  # also available through g.cognito_claims
    return jsonify({'claims': claims})


@application.route('/success')
@cross_origin()
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return redirect('http://localhost:3000/dashboard?token=' + access_token)


@application.route('/sign_in')
@cross_origin()
def sign_in():
    return redirect(aws_auth.get_sign_in_url())
