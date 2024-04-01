from ..serialiser import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AbstractSchema(SQLAlchemyAutoSchema):
    dumped_data = None

    class Meta:
        pass
     
    def __init__(self):
        super().__init__()
    
    def setDumpedData(self, data:dict, is_many = False):
        self.many = is_many
        self.dumped_data = self.dump(data)
