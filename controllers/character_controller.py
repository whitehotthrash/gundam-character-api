from flask import Blueprint, jsonify, request, abort
from init import db
from models.character import Character
from schemas.character_schema import character_schema, CharacterSchema

characters = Blueprint("characters", __name__, url_prefix="/characters")


# The GET routes endpoint
@characters.route("/", methods=["GET"])
def get_characters():
    # get all the characters from the database table
    characters_list = Character.query.all()
    # Convert the characters from the database into a JSON format and store them in result
    result = CharacterSchema(many=True).dump(characters_list)
    # return the data in JSON format
    return jsonify(result)


# The POST route endpoint
@characters.route("/", methods=["POST"])
def create_character():
    # Create a new character
    # Deserialize JSON into a Character instance
    character = character_schema.load(request.json, session=db.session)
    # Add to DB and commit
    db.session.add(character)
    db.session.commit()
    # Serialize and return the new character
    return jsonify(character_schema.dump(character))


# The DELETE route endpoint
@characters.route("/<int:id>/", methods=["DELETE"])
def delete_character(id):
    # find the character
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    # return an error if the character doesn't exist
    if not character:
        return abort(400, description="Character doesn't exist")
    # Delete the character from the database and commit
    db.session.delete(character)
    db.session.commit()
    # return the character in the response
    return jsonify(character_schema.dump(character))
