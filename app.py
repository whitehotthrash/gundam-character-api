from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    # creating our database object! This allows us to use our ORM
    db = SQLAlchemy(app)
    
    return app