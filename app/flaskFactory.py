from flask import Flask, jsonify
from .database import db
from .routes.student import student_blueprint
from .routes.address import address_blueprint
from .routes.user import user_blueprint
from .routes.geocoding import geocoding_blueprint
from .serialiser import ma
from .security import jwt
from .models.envs import *
from .models.user import User
from .upload_data import upload_student_data

is_connected = False

db.create_schema(DB_DEFAULT_PATH, DB_NAME)

app = Flask(__name__)

app.register_blueprint(student_blueprint)
app.register_blueprint(address_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(geocoding_blueprint)

db.set_connection_string(app,DB_PATH)
db.set_app(app)
ma.init_app(app)

jwt.set_secret_key(app,SECRET_KEY)
jwt.set_cookie_security(app, False)
jwt.set_token_location(app,["cookies"])
jwt.set_cookie_CSFR_protection(app,False)
jwt.set_token_expiration(app)
jwt.set_app(app)

with app.app_context():
        db.create_tables()
        User.create_default_user()
        upload_student_data()

is_connected = db.check_connection()

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"msg": "Please login"}), 401

@jwt.expired_token_loader
def custom_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Your session has expired, please login again."}), 401  