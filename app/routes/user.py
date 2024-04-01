from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, set_access_cookies, get_jwt, unset_jwt_cookies
from datetime import datetime, timedelta
from ..models.user import User
from ..database import db
from .response import response

user_blueprint = Blueprint("user",__name__)

def timestamp(time:timedelta):
    now = datetime.now()
    return datetime.timestamp(now + time)

@user_blueprint.after_app_request
def refresh(response):
    try:
        expiry = get_jwt()["exp"]
        if timestamp(timedelta(seconds=8)) > expiry:
            access_token = User.refresh_jwt_token(get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@user_blueprint.route("/api/user/register", methods=["POST"])
def register():
    data = request.json
    try:
        user = User(data["email"],data["password"])
        new_record_attempt = user.attempt_insert()
        if new_record_attempt:
            token = user.create_jwt_token()
            resp = jsonify(msg="Registration Successful", status=201)
            set_access_cookies(resp,token)
            return resp
        else:
            return response("Something went wrong.",400)
    except KeyError:
        return response("Please provide both email and password.",400)
    
@user_blueprint.route("/api/user/login", methods=["POST"])
def login():
    data = request.json
    try:
        user = User(data["email"],data["password"])
        retrieved_user= user.retrieve()

        if isinstance(retrieved_user, User):
            token = user.create_jwt_token()
            resp = jsonify(msg="Login successful", status=201)
            set_access_cookies(resp, token)
            return resp
        elif retrieved_user == "not found":
            return response("Email not found, please try again",400)
        else:
            return response(f"Incorrect Password, please try again. {retrieved_user}",400)
    except KeyError:
        return response("Please provide both email and password",400)