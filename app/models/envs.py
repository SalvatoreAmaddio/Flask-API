from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DB_ROOT = os.getenv('DB_ROOT')
DB_NAME = os.getenv("DB_NAME")
DB_PATH = DB_ROOT + DB_NAME
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

