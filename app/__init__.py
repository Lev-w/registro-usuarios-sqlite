from flask import Flask
from dotenv import load_dotenv
import os
from app.helpers.errors import register_error_handlers
import app.modules.db.db as db

load_dotenv()

def create_app():
    app = Flask(__name__)

    from app.modules.routes import main

    app.register_blueprint(main)

    register_error_handlers(app)

    app.secret_key = os.getenv("SECRET_KEY")

    return app