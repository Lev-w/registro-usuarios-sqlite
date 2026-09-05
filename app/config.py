from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = "usuarios.db"
SECRET_KEY = os.getenv("SECRET_KEY")