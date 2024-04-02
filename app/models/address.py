"""
This class represents the Students' addresses model
"""
from ..database import db
from .abstractModel import AbstractModel

class Address(db.Model, AbstractModel):
    __tablename__ = "address"
    id = db.is_pk()
    student_id = db.is_fk("student.id")
    number = db.is_varchar_field(chars=10,can_be_null=True)
    house_name = db.is_varchar_field(can_be_null=True)
    road = db.is_varchar_field()
    city = db.is_varchar_field()
    state = db.is_varchar_field()
    country = db.is_varchar_field()
    zipcode = db.is_varchar_field()
    student = db.set_relationship(__tablename__,"Student")

    def __str__(self):
        return f"{self.number}, {self.house_name}, {self.road}, {self.city}, {self.state}, {self.country} - {self.zipcode}"

    def readDictionary(self, data: dict):
        self.student_id = data["student_id"]
        self.number = data["number"]
        self.house_name = data["house_name"]
        self.road = data["road"]
        self.city = data["city"]
        self.state = data["state"]
        self.country = data["country"]
        self.zipcode = data["zipcode"]

    def read_google_result(self, address_component:dict):
        """
        This method is used to read google JSON results
        """
        for component in address_component:
            if component["types"][0]=="postal_code":
                self.zipcode = component["long_name"]
            if component["types"][0]=="country":
                self.country = component["long_name"]
            if component["types"][0]=="administrative_area_level_1":
                self.state = component["long_name"]
            if component["types"][0]=="route":
                self.road = component["long_name"]
            if component["types"][0]=="street_number":
                self.number = component["long_name"]
            if component["types"][0]=="premise":
                self.house_name = component["long_name"]
