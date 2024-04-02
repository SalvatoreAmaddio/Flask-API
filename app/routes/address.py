"""
This class defines the route for address API
"""
from flask import Blueprint
from ..models.address import Address
from ..schemas.address_schema import AddressSchema
from .abstractRoute import AbstractRoute
from flask_jwt_extended import jwt_required

class AddressApi(AbstractRoute):
    def __init__(self):
        super().__init__(Address, schema=AddressSchema(), record=Address(), api_path="/api/address")

    def fields(self):
        return "student_id, number, house_name, road, city, state, country, zipcode"

address_api = AddressApi()

address_blueprint = Blueprint("address",__name__)

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