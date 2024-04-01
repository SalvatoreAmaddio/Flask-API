from ..serialiser import ma
from ..models.student import Student
from .address_schema import AddressSchema
from .abstractSchema import AbstractSchema

class StudentSchema(AbstractSchema):

    class Meta:
        model = Student
        fields = ("id","name","nationality","city","lat","long","gender","age","english_grade","math_grade","sciences_grade","languages_grade")
    
    addresses = ma.Nested(AddressSchema, many=True)

    def __init__(self):
        super().__init__()

