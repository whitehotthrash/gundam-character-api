from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from commands import db_commands

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")
    
    # initialising our database object with the flask app
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(db_commands)

    return app