"""
This class is design to work with a MySQL Database only.
It has not been tested to work with other Databases
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.orm import backref
from enum import Enum
from sqlalchemy import create_engine, func
from sqlalchemy_utils import database_exists, create_database

class FKOptions(Enum):
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    SET_NULL = "SET NULL"
    NO_ACTION = "NO ACTION"

class RelationshipOptions(Enum):
    NONE = "None"
    UPDATE_DELETE_CASCADE = 'all, delete-orphan'
    SAVE_UPDATE = 'save-update'
    SAVE_UPDATE_MERGE = 'save-update, merge'
    MERGE = 'merge'
    EXPUNGE = 'expunge'
    DELETE = 'delete'
    DELETE_ORPHAN = 'delete-orphan'
    REFRESH_EXPIRE = 'refresh-expire'
    ALL = 'all'


class pyMySQL(SQLAlchemy):
    version = None

    def __init__(self):
        super().__init__()

    def set_app(self, app:Flask):
        """
        It connects the Flask App to the ORM

        Args:
            value: the flask app
        """
        self.init_app(app)

    def set_connection_string(self, app:Flask, connection_string:str):
        """
        It connects the Flask App to the ORM

        IMPORTANT:
            call this method before db.set_app(app).

        Args:
            app: the flask app
            connection_string: the connection string to pass.

        For Example:
            db.set_connection_string(app, "root:root@localhost/flaskAssessment")
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{connection_string}"

    def create_schema(self, dbDefaultPath, dbName):
        """
        It creates a new Schema if it does not exist.

        Note:
        call this method before app.config

        Args:
            dbDefaultPath: a connection string to connect to the database engine by using its default database.
            dbName: the name of the database to create.

        For Example:
            db.create_schema("root:root@localhost/mysql","flaskAssessment")
        """
        engine = create_engine(f'mysql+pymysql://{dbDefaultPath}')
        conn = engine.connect()
        sql_cmd = text(f"CREATE DATABASE IF NOT EXISTS {dbName}")
        conn.execute(sql_cmd)
        conn.close()

    def create_tables(self):
        """
        It creates tables into the Database.

        Tables are created based on the settings of their blueprint classes.

        If tables already exist, this method has no effect.

        For Example:
               with app.app_context():
                    db.create_tables()

        """
        self.create_all()
        self.session.commit()

    def add_new_record(self, record):
        """
        It adds a new record to the session waiting for a commit command to be executed
        
        Args:
            record: an object that derives from db.Model
        """
        self.session.add(record)

    def commit_new_record(self, record):
        """
        It adds a new record and commit the changes
        
        Args:
            record: an object that derives from db.Model
        """
        self.session.add(record)
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def flush(self):
        self.session.flush()

    def to_delete_record(self, record):
        """
        It notes that a record should be deleted and wait for a commit command to be executed
        
        Args:
            record: an object that derives from db.Model
        """
        self.session.delete(record)

    def commit_delete_record(self, record):
        """
        It deletes a record and commit the changes
        
        Args:
            record: an object that derives from db.Model
        """
        self.session.delete(record)
        self.session.commit()

    def where(self, entity, **kwargs):
        """
        It fetches a set of records based upon conditions
        
        Args:
            entity: an Class that derives from db.Model

        For Example:
            db.where(User, id=5, name='John')

        Returns:
            A Query object which is iterable.
        """
        return self.session.query(entity).filter_by(**kwargs).all()

    def where_first(self, entity, **kwargs):
        """
        It returns the first record based on your criteria
        
        Args:
            entity: an Class that derives from db.Model
            **kwargs: a set of parameters

        For Example:
            db.where_first(User, id=5, name='John')

        Returns:
            An instance of the Entity
        """
        return self.session.query(entity).filter_by(**kwargs).first()

    def get_all_records(self, entity):
        """
        It returns all records.

        Args:
             entity: a Class that derives from db.Model

        Returns:
            A Query object which is iterable
        """
        return self.session.query(entity).all()

    def get_first(self, entity, recordID:int):
        """
        It returns the first record by using its Primary Key
        
        Args:
            entity: a Class that derives from db.Model
            recordID: Primary Key value

        For Example:
            db.get_first(User, id=5)

        Returns:
            An instance of the Entity
        """
        return self.session.query(entity).filter_by(id=recordID).first()
    
    def commit(self):
        """
        It commits changes to the database.

        Use this method when dealing with Update CRUD operations.

        or when adding/deleting multiple records at once. 

        For Example:

            user = db.get_first(User,3) #get User whose id is 3

            user.name = "Bo" #change name of the user to Bo

            db.commit() #save changes to the database
        """
        self.session.commit()

    def is_fk(self, parentTablePK: str, onDelete = FKOptions.CASCADE, onUpdate = FKOptions.CASCADE):
        """
        It tells the ORM that the field is a Foreign Key

        please not this method is designed for Integers
                
        Args:
            parentTablePK: the name of the parent table and its primary key,
            onDelete: the option of the FK on delete; default value is Cascade,
            onUpdate: the option of the FK on update; default value is Cascade

        For Example:
            user_id = db.is_fk(user.id)
        """
        return self.Column(self.Integer, self.ForeignKey(parentTablePK, ondelete = onDelete.value, onupdate = onUpdate.value), nullable=False)

    def is_varchar_field(self, chars:int = 30, can_be_null:bool = False, is_unique:bool = False):
        """
        It tells the ORM that the field is of VARCHAR.
        
        Args:
            chars: the number of characters; default is 30.
            can_be_null: tells if the value is nullable or not; default is False.
            is_unique: tells if the value is unique and therefore no duplicates are allowed; default is False
        For Example:
            FirstName = db.is_varchar_field()
        """
        return self.Column(self.String(chars), nullable = can_be_null, unique = is_unique)

    def is_int_field(self, can_be_null:bool = False, is_unique:bool = False):
        """
        It tells the ORM that the field is an Integer.
        
        Args:
            can_be_null: tells if the value is nullable or not; default is False.
            is_unique: tells if the value is unique and therefore no duplicates are allowed; default is False
        For Example:
            Age = db.is_int_field()
        """
        return self.Column(self.Integer, nullable = can_be_null, unique = is_unique)

    def is_float_field(self, can_be_null:bool = False, is_unique:bool = False):
        """
        It tells the ORM that the field is an float.
        
        Args:
            can_be_null: tells if the value is nullable or not; default is False.
            is_unique: tells if the value is unique and therefore no duplicates are allowed; default is False
        For Example:
            Age = db.is_float_field()
        """
        return self.Column(self.Float, nullable = can_be_null, unique = is_unique)

    def is_pk(self):
        """
        It tells the ORM that the field is a Primary Key.
        
        N.B.: this method is meant for integers PrimaryKey with Auto Increment.

        For Example:
            ID = db.is_pk()
        """
        return self.Column(self.Integer, primary_key=True, autoincrement=True)
    
    def set_relationship(self, class_name: str, table_name: str, isOneToOne=True, options:RelationshipOptions = RelationshipOptions.UPDATE_DELETE_CASCADE): 
        """
        It sets the relationship that exists between the Parent Table and the Child Table.

        Args:
            class_name: the name of Parent Model.
            table_Name: the name of the table in the database.
            isOneToOne: it sets if the Relationship is One to One; default is True
            fk_options: a FKOPtions enum that sets Foreing Keys actions; default is UPDATE_DELETE_CASCADE.

        IMPORTANT:
            call this method on model where the FK is declared.
            Not tested for One to Many scenarios.

        For Example:

            class ChildModel(db.Model):
                __tablename__ = "childtable"
                id = db.is_pk()
                
                parent_id = db.is_fk("parent.id")

                ...

                parent = set_relationship(__tablename__, 'ParentModel')
        """
        isOneToOne = not isOneToOne
        return self.relationship(table_name, backref = backref(class_name, uselist=isOneToOne, cascade = options.value))

    def record_count(self,entity):
        return self.session.query(func.count('*')).select_from(entity).scalar()

    def check_connection(self):
        """
        It checks if the connection was successful.

        Returns:
            A string telling the Version of the Database or an Error Message about why the connection failed.
        """
        try:
            sql_cmd = text("SELECT VERSION()")
            with self.engine.connect() as connection:
                result = connection.execute(sql_cmd)
                self.version = result.fetchone()
                return True
        except Exception as e:
            return f"Database connection failed: {e}"
