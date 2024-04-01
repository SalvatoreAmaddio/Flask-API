from ..models.address import Address
from .abstractSchema import AbstractSchema

class AddressSchema(AbstractSchema):

    class Meta:
        model = Address
        fields = ("id","student_id","number","house_name","road","city","state","country","zipcode")

    def __init__(self, many = False):
        super().__init__(many)