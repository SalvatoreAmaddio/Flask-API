from flask import Blueprint
import sqlalchemy.exc as SQLError
from ..models.address import Address
from ..database import db
from ..models.student import Student
import requests
from .response import response
from flask_jwt_extended import jwt_required
from ..models.envs import GOOGLE_API_KEY

geocoding_blueprint = Blueprint("geocoding",__name__)

#https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding
def build_google_api_url(lat, long):
    return f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat.strip()},{long.strip()}&key={GOOGLE_API_KEY}&result_type=street_address&location_type=ROOFTOP"

@geocoding_blueprint.route(f"/api/geocoding/<int:record_id>",methods=["POST"])
@jwt_required()
def google_api(record_id):
    student = db.get_first(Student,record_id)
    
    if student is None:
        return response("Record not found, try with a different ID",404)
    
    lat = getattr(student,"lat")
    long = getattr(student,"long")
    api_response = requests.get(build_google_api_url(lat, long))
    data = api_response.json()
    results = data["results"]

    if len(results) == 0:
         return response("Google returned zero results. Sorry :(",{"lat":lat,"long":long, "student":str(student)},200)
    
    address_component = results[0]["address_components"]
    address = Address()
    address.student_id = record_id
    address.city = getattr(student,"city")
    try:
        address.read_google_result(address_component)
        db.flush()
        db.commit_new_record(address)
        return response("New address created", str(address), 201)
    except SQLError.SQLAlchemyError:
        return response(f"Something went wrong while fetching some mandatory data. Unfortunately this API is too complex with way too many variables. I cannot insert a new record. Sorry :(", 500)
    except KeyError:
        return response(f"Something went wrong while fetching the data. Unfortunately this API is too complex with way too many variables. Sorry :(", 500)