from flask import Blueprint, jsonify, request, abort
from init import db
from models.character import Character
from schemas.character_schema import character_schema

characters = Blueprint('characters', __name__, url_prefix="/characters")

# The GET routes endpoint
@characters.route("/", methods=["GET"])
def get_characters():
    # get all the characters from the database table
    stmt = db.select(Character)
    characters_list = db.session.scalars(stmt)
    # Convert the characters from the database into a JSON format and store them in result
    result = character_schema.dump(characters_list)
    # return the data in JSON format
    return jsonify(result)
  
# The POST route endpoint
@characters.route("/", methods=["POST"])  
def create_character():
    # Create a new character
    character_fields = character_schema.load(request.json)
    new_character = Character()
    new_character.name = character_fields["name"]
    new_character.birth_year = character_fields["birth_year"]
    new_character.classification = character_fields["classification"]
    new_character.place_of_birth = character_fields["place_of_birth"]
    new_character.rank = character_fields["rank"]
    new_character.status = character_fields["status"]
    db.session.add(new_character)
    db.session.commit()
    return jsonify(character_schema.dump(new_character))

# The DELETE route endpoint
@characters.route("/<int:id>/", methods=["DELETE"])
def delete_character(id):
    # find the character
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    # return an error if the character doesn't exist
    if not character:
        return abort(400, description= "Character doesn't exist")
    # Delete the character from the database and commit
    db.session.delete(character)
    db.session.commit()
    # return the character in the response
    return jsonify(character_schema.dump(character))