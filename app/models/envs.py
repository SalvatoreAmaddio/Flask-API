from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_DEFAULT_PATH = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/mysql"
DB_PATH = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DB_HOST_PATH = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

