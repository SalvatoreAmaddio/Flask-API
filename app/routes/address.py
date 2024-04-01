from flask import Blueprint, request
import sqlalchemy.exc as SQLError
from ..models.address import Address
from ..schemas.address_schema import AddressSchema
from .abstractRoute import AbstractRoute
from ..database import db
from ..models.student import Student
import requests
from .response import response
from flask_jwt_extended import jwt_required

class AddressApi(AbstractRoute):
    def __init__(self):
        super().__init__(Address, schema=AddressSchema(), record=Address(), api_path="/api/address")

    def fields(self):
        return "student_id, number, house_name, road, city, state, country, zipcode"

address_api = AddressApi()

address_blueprint = Blueprint("address",__name__)

#https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding
def build_google_api_url(lat, long):
    key = "AIzaSyD_VXrKBFlwiym7lXKhMw8qGsnJdtH60J0"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat.strip()},{long.strip()}&key={key}&result_type=street_address&location_type=ROOFTOP"
    return url

@address_blueprint.route(f"/api/geocoding/<int:record_id>",methods=["POST"])
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

@address_blueprint.route(address_api.api_path,methods=["GET"])
@jwt_required()
def all_records():
    return address_api.all_records()

@address_blueprint.route(f"{address_api.api_path}/<int:record_id>",methods=["GET"])
@jwt_required()
def single_record(record_id):
    return address_api.single_record(record_id)

@address_blueprint.route(address_api.api_path,methods=["POST"])
@jwt_required()
def post_record():
    return address_api.post_record()
    
@address_blueprint.route(f"{address_api.api_path}/<int:record_id>",methods=["PATCH"])
@jwt_required()
def patch_record(record_id):
    return address_api.patch_record(record_id) 
   
@address_blueprint.route(f"{address_api.api_path}/<int:record_id>",methods=["PUT"])
@jwt_required()
def put_record(record_id):
    return address_api.put_record(record_id)

@address_blueprint.route(f"{address_api.api_path}/<int:record_id>",methods=["DELETE"])
@jwt_required()
def delete_record(record_id):
    return address_api.delete_record(record_id)