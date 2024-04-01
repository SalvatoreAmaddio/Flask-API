from flask import request
from ..database import db
from .response import *
import sqlalchemy
from ..schemas.abstractSchema import AbstractSchema
from ..models.abstractModel import AbstractModel
from abc import abstractmethod

class AbstractRoute():
        
        def __init__(self, entity, schema:AbstractSchema, record:AbstractModel, api_path:str):
                self._entity = entity
                self._schema = schema
                self._record = record
                self._api_path = api_path
                self.__record_not_found = "Record not found, try with a different ID"
                self.__record_updated = "Record successfully updated"
                self.__required_fields_err = f"Field(s) not found Error: Please ensure you've specified all required fields as follow: {self.fields()}. Check your spelling also."
                self.__pk_err = "You have attempt to alter the value of a autoincremented primary or provide a foreign key's value that does not exist."

        @abstractmethod
        def fields(self):
                pass

        @property
        def api_path(self):
                return self._api_path

        @property
        def record(self):
                return self._record

        @property
        def entity(self):
                return self._entity

        @property
        def schema(self):
                return self._schema

        def all_records(self):
                records = db.get_all_records(self.entity)
                if len(records) <= 0:
                        return response("No Data",200)
                self.schema.setDumpedData(records, is_many=True)
                return response(self.schema.dumped_data, 200)
        
        def single_record(self, record_id):
                try:
                        record = db.get_first(self.entity, record_id)
                        if record is None:
                                return response(self.__record_not_found,404)
                        self.schema.setDumpedData(record)
                        return response(self.schema.dumped_data, 200)
                except Exception as e:
                        return response(str(record), 400)
        
        def post_record(self):
                data = request.json
                try:
                        self.record.readDictionary(data)
                        db.commit_new_record(self.record)
                        return response("New record created", data, 201)
                except sqlalchemy.exc.IntegrityError:
                        return response(self.__pk_err, 400)
                except KeyError:
                        return response(self.__required_fields_err, 400)
        
        def patch_record(self, record_id):
                record = db.get_first(self.entity, record_id)
                if record is None:
                        return response(self.__record_not_found,404)
    
                data = request.json
                try:
                        for key, value in data.items():
                                if not hasattr(record, key):
                                        raise KeyError
                                else:
                                        setattr(record, key, value)
                                        db.commit()

                        record = db.get_first(self.entity, record_id)
                        self.schema.setDumpedData(record)
                        return response(self.__record_updated, self.schema.dumped_data, 200)
                except sqlalchemy.exc.IntegrityError:
                        return response(self.__pk_err, 400)
                except KeyError:
                        return response(f"Field not found Error: Please ensure you've specified one or more field as follow: {self.fields()}. Check your spelling also.", 400)

        def put_record(self, record_id):
                old_record = db.get_first(self.entity, record_id)
                if old_record is None:
                        return response(self.__record_not_found,404)
    
                data = request.json
                try:
                        self.record.readDictionary(data) #check if all fields have been provided
                        for key, value in data.items(): #loop through to update old_student based on the JSON
                                if not hasattr(old_record, key):
                                        raise KeyError
                                else:
                                        setattr(old_record, key, value)
                                        db.commit()
                        self.schema.setDumpedData(old_record)
                        return response(self.__record_updated, self.schema.dumped_data, 200)
                except sqlalchemy.exc.IntegrityError:
                        return response(self.__pk_err, 400)
                except KeyError:
                        return response(self.__required_fields_err, 400)

        def delete_record(self, record_id):
                record = db.get_first(self.entity, record_id)
                if record is None:
                        return response(self.__record_not_found,404)
                
                db.commit_delete_record(record)
                return response(f"Record with ID:{record_id} successfully deleted", 200)