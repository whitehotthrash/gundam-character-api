from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
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

    # Centralised error handlers return JSON responses
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {"error": e.description}
        return jsonify(response), e.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        # Marshmallow validation error
        return jsonify({"errors": e.messages}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        app.logger.exception(e)
        return jsonify({"error": "Internal server error"}), 500

    return app