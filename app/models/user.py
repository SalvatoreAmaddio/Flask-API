from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import OperationalError, IntegrityError
import time

class User(db.Model):
    __tablename__ = "user"
    id = db.is_pk()
    email = db.is_varchar_field(100,is_unique=True)
    password = db.is_varchar_field(255)
    num_tries = 5
    user_is_registered = False

    def __init__(self, email, pswd):
        self.email = email
        self.__pwd = pswd
        self.password = generate_password_hash(pswd)

    
    def retrieve(self):
        try:
            user = db.where_first(User, email=self.email)
            if user:
                if check_password_hash(getattr(user,"password"), self.__pwd):
                    return user
                else:
                    return "wrong password"
            else:
                return "User not found"
        except Exception as e:
            return f"Exception{e}"
    
    def create_jwt_token(self):
        return create_access_token(self.email)
    
    @staticmethod
    def refresh_jwt_token(func):
        return create_access_token(identity=func())
    
    def attempt_insert(self):
        while self.num_tries > 0:
            try:
                db.commit_new_record(self)
                self.user_is_registered = True
                break
            except OperationalError:
                db.rollback()
                self.num_tries -=1
                time.sleep(1)
            except IntegrityError:
                db.rollback()
                return False
        
        if not self.user_is_registered:
            return None
        else:
            return True

