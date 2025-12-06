from flask import Blueprint, jsonify, request, abort
from init import db
from models.character import Character
from schemas.character_schema import character_schema, CharacterSchema
from models.lookup_tables import Affiliation, Occupation

characters = Blueprint("characters", __name__, url_prefix="/characters")


@characters.route("/", methods=["GET"])
def get_characters():
    # get all the characters from the database table
    characters_list = Character.query.all()
    # Convert the characters from the database into a JSON format and store them in result
    result = CharacterSchema(many=True).dump(characters_list)
    # return the data in JSON format
    return jsonify(result)


@characters.route("/", methods=["POST"])
def create_character():
    # Create a new character
    # from schemas.lookup_schema import affiliation_schema
    character = character_schema.load(request.json, session=db.session)
    # data = request.get_json()
    
    # new_affiliation = affiliation_schema.load(data, session=db.session)
    
    # affiliations = Affiliation.query.get(new_affiliation.id)
    # character.affiliations = affiliations
    
    db.session.add(character)
    db.session.commit()
    
    return jsonify(character_schema.dump(character)), 201


@characters.route("/<int:id>/", methods=["DELETE"])
def delete_character(id):
    
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(400, description="Character doesn't exist")
    
    db.session.delete(character)
    db.session.commit()
    
    return jsonify(character_schema.dump(character))
