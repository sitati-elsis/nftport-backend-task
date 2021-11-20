from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
from .models import *

def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False, static_folder=None)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        print("Creating tables")
        db.create_all()  # Create sql tables for our data models
        print("Finished creating tab;es")
        return app