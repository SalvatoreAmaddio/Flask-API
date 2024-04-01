from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

class JWT(JWTManager):
    
    def set_secret_key(self, app:Flask, key):
        app.config["JWT_SECRET_KEY"] = key
    
    def set_cookie_security(self, app:Flask, value:bool):
        app.config["JWT_COOKIE_SECURE"] = value

    def set_token_location(self, app:Flask, value:dict):
        app.config["JWT_TOKEN_LOCATION"] = value

    def set_cookie_CSFR_protection(self, app:Flask, value:bool = True):
        app.config["JWT_COOKIE_CSRF_PROTECT"] = value

    def set_token_expiration(self, app:Flask, time:timedelta = timedelta(minutes=30)):
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = time

    def set_app(self, app:Flask):
        self.init_app(app)
    
