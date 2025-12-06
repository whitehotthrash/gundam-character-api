from flask import Flask
from init import db, ma

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")
    
    # initialising our database object with the flask app
    db.init_app(app)
    ma.init_app(app)
    
    from commands import db_commands
    app.register_blueprint(db_commands)
    
    # import the controllers and activate the blueprints
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app