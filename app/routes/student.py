from flask import Blueprint
from ..models.student import Student
from ..schemas.student_schema import StudentSchema
from .abstractRoute import AbstractRoute
from flask_jwt_extended import jwt_required

student_blueprint = Blueprint("student",__name__)

class StudentApi(AbstractRoute):
    def __init__(self):
        super().__init__(Student, schema=StudentSchema(), record=Student(), api_path="/api/student")

    def fields(self):
        return "name, nationality, city, lat, long, gender, age, english_grade, math_grade, sciences_grade, languages_grade."

student_api = StudentApi()

@student_blueprint.route(student_api.api_path,methods=["GET"])
@jwt_required()
def all_records():
    return student_api.all_records()

@student_blueprint.route(f"{student_api.api_path}/<int:record_id>",methods=["GET"])
@jwt_required()
def single_record(record_id):
    return student_api.single_record(record_id)

@student_blueprint.route(student_api.api_path,methods=["POST"])
@jwt_required()
def post_record():
    return student_api.post_record()
    
@student_blueprint.route(f"{student_api.api_path}/<int:record_id>",methods=["PATCH"])
@jwt_required()
def patch_record(record_id):
    return student_api.patch_record(record_id) 
   
@student_blueprint.route(f"{student_api.api_path}/<int:record_id>",methods=["PUT"])
@jwt_required()
def put_record(record_id):
    return student_api.put_record(record_id)

@student_blueprint.route(f"{student_api.api_path}/<int:record_id>",methods=["DELETE"])
@jwt_required()
def delete_record(record_id):
    return student_api.delete_record(record_id)