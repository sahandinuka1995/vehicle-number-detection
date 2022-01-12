from dataclasses import dataclass

from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import pytesseract as tess
from werkzeug.utils import secure_filename
import os
import urllib.request
import cv2

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


@dataclass
class Vehicle(db.Model):
    id: int
    name: str
    vehicleNo: str
    model: str
    colour: str
    type: str
    image: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    vehicleNo = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.String(100), unique=False, nullable=False)
    colour = db.Column(db.String(100), unique=False, nullable=False)
    type = db.Column(db.String(100), unique=False, nullable=False)
    image = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, name, vehicleNo, model, colour, type, image):
        self.name = name
        self.vehicleNo = vehicleNo
        self.model = model
        self.colour = colour
        self.type = type
        self.image = image

    def __repr__(self):
        return f"['name'=>{self.name}, 'vehicleNo'=>{self.vehicleNo}, 'model'=>{self.model}, 'colour'=>{self.colour}, 'type'=>{self.type}, 'image'=>{self.image}]"


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
    return render_template('index.html')


def addNewVehicle(data):
    # try:
    #     # vehicle = Vehicle(name=data['name'], vehicleNo=data['vehicleNo'], model=data['model'],
    #     #                   colour=data['colour'],
    #     #                   type=data['type'])
    #
    #     # print(data['image'])
    #     # file = data.files['file']
    #     # print(data.files['image'])
    #     # filename = secure_filename(file.filename)
    #     # file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
    #     # print(vehicle)
    #     # f = request.files['file']
    #
    #
    #     # db.session.add(vehicle)
    #     # db.session.commit()
    #
    #     return make_response(jsonify({
    #         "success": "true",
    #         "msg": "Vehicle added successfully!",
    #         "status": "200"
    #     }), 200)
    # except:
    #     return errorResponse()

    import pytesseract

    tess.pytesseract.tesseract_cmd = r'D:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    img = cv2.imread("1.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        print(text)

        # Appending the text into file
        # file.write(text)
        # file.write("\n")
        #
        # # Close the file
        # file.close

    return make_response(jsonify({
        "success": "true",
        "msg": "Vehicle added successfully!",
        "status": "200"
    }), 200)


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
