"""
This class represents the Students model
"""
from ..database import db
from .abstractModel import AbstractModel

class Student(db.Model, AbstractModel):
    __tablename__ = "student"
    id = db.is_pk()
    name = db.is_varchar_field()
    nationality = db.is_varchar_field()
    city = db.is_varchar_field()
    lat = db.is_varchar_field()
    long = db.is_varchar_field()
    gender = db.is_varchar_field()
    age = db.is_varchar_field()
    english_grade = db.is_int_field()
    math_grade = db.is_int_field()
    sciences_grade = db.is_int_field()
    languages_grade = db.is_int_field()

    def __str__(self):
        return f"StudentID: {self.id}; Name: {self.name}; Nationality: {self.nationality}"
        
    def readDictionary(self, data: dict):
        self.name = data["name"]
        self.nationality = data["nationality"]
        self.city = data["city"]
        self.lat = data["lat"]
        self.long = data["long"]
        self.gender = data["gender"]
        self.age = data["age"]
        self.english_grade = data["english_grade"]
        self.math_grade = data["math_grade"]
        self.sciences_grade = data["sciences_grade"]
        self.languages_grade = data["languages_grade"]