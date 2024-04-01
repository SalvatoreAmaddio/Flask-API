from flask import Flask, jsonify
from .database import db
from .routes.student import student_blueprint
from .routes.address import address_blueprint
from .routes.user import user_blueprint
from .serialiser import ma
from .security import jwt

is_connected = False

db.create_schema("root:root@localhost/","flaskAssessment")
app = Flask(__name__)

app.register_blueprint(student_blueprint)
app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)

db.set_connection_string(app,"root:root@localhost/flaskAssessment")
db.set_app(app)
ma.init_app(app)

jwt.set_secret_key(app,"123456789010")
jwt.set_cookie_security(app,False) #to change to true
jwt.set_token_location(app,["cookies"])
jwt.set_cookie_protection(app)
jwt.set_token_expiration(app)
jwt.set_app(app)

with app.app_context():
        db.create_tables()

is_connected = db.check_connection()

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"msg": "Please login"}), 401

@jwt.expired_token_loader
def custom_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Your session has expired, please login again."}), 401  