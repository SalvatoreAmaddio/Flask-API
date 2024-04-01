from ..serialiser import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AbstractSchema(SQLAlchemyAutoSchema):
    dumped_data = None

    class Meta:
        pass
     
    def __init__(self, is_many = False):
        super().__init__(many = is_many)
    
    def setDumpedData(self, data:dict):
        self.dumped_data = self.dump(data)
