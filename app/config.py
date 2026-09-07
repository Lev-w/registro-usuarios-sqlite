from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = "usuarios.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY")
