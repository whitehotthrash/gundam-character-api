from flask import Blueprint, jsonify, request, abort
from init import db
from models.character import Character
from schemas.character_schema import character_schema, CharacterSchema
from models.lookup_tables import Affiliation, Occupation
from controllers.helpers import (
    load_schema_or_abort,
    validate_ids_exist_or_abort,
    commit_or_abort,
    get_json_or_empty,
    fetch_or_abort,
)

characters = Blueprint("characters", __name__, url_prefix="/characters")


@characters.route("/", methods=["GET"])
def get_characters():
    # get all the characters from the database table
    characters_list = Character.query.all()
    # Convert the characters from the database into a JSON format and store them in result
    result = CharacterSchema(many=True).dump(characters_list)
    # return the data in JSON format
    return jsonify(result), 200

@characters.route("/<int:id>/", methods=["GET"])
def get_character(id):
    # get a single character from the database
    character = fetch_or_abort(Character, id, not_found_message="Character doesn't exist")
    result = character_schema.dump(character)
    return jsonify(result), 200

@characters.route("/", methods=["POST"])
def create_character():
    # Create a new character
    data = request.get_json()
    character_fields = load_schema_or_abort(character_schema, data=data, session=db.session)
    new_character = Character(
        name=character_fields["name"],
        birth_year=character_fields["birth_year"],
        classification=character_fields["classification"],
        place_of_birth=character_fields["place_of_birth"],
        rank=character_fields["rank"],
        status=character_fields["status"]
    )
    
    db.session.add(new_character)

    # Handle affiliations
    if "affiliation_ids" in character_fields:
        affs = validate_ids_exist_or_abort(Affiliation, character_fields["affiliation_ids"], "Affiliation")
        for affiliation in affs:
            new_character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        occs = validate_ids_exist_or_abort(Occupation, character_fields["occupation_ids"], "Occupation")
        for occupation in occs:
            new_character.occupations.append(occupation)
    
    commit_or_abort()

    return jsonify(character_schema.dump(new_character)), 201


@characters.route("/<int:id>/", methods=["PUT"])
def update_character(id):
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    if not character:
        return abort(404, description="Character doesn't exist")
    
    data = get_json_or_empty()
    character_fields = load_schema_or_abort(character_schema, data=data, session=db.session, partial=False)
    
    character.name = character_fields["name"]
    character.birth_year = character_fields["birth_year"]
    character.classification = character_fields["classification"]
    character.place_of_birth = character_fields["place_of_birth"]
    character.rank = character_fields["rank"]
    character.status = character_fields["status"]
    
    # Handle affiliations
    if "affiliation_ids" in character_fields:
        character.affiliations.clear()
        affs = validate_ids_exist_or_abort(Affiliation, character_fields["affiliation_ids"], "Affiliation")
        for affiliation in affs:
            character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        character.occupations.clear()
        occs = validate_ids_exist_or_abort(Occupation, character_fields["occupation_ids"], "Occupation")
        for occupation in occs:
            character.occupations.append(occupation)
    
    commit_or_abort()

    return jsonify(character_schema.dump(character)), 200


@characters.route("/<int:id>/", methods=["PATCH"])
def patch_character(id):
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(404, description="Character doesn't exist")
    
    data = get_json_or_empty()
    character_fields = load_schema_or_abort(character_schema, data=data, session=db.session, partial=True)
    
    if "name" in character_fields:
        character.name = character_fields["name"]
    if "birth_year" in character_fields:
        character.birth_year = character_fields["birth_year"]
    if "classification" in character_fields:
        character.classification = character_fields["classification"]
    if "place_of_birth" in character_fields:
        character.place_of_birth = character_fields["place_of_birth"]
    if "rank" in character_fields:
        character.rank = character_fields["rank"]
    if "status" in character_fields:
        character.status = character_fields["status"]
    
    # Handle affiliations
    if "affiliation_ids" in character_fields:
        character.affiliations.clear()
        affs = validate_ids_exist_or_abort(Affiliation, character_fields["affiliation_ids"], "Affiliation")
        for affiliation in affs:
            character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        character.occupations.clear()
        occs = validate_ids_exist_or_abort(Occupation, character_fields["occupation_ids"], "Occupation")
        for occupation in occs:
            character.occupations.append(occupation)
    
    commit_or_abort()

    return jsonify(character_schema.dump(character)), 200


@characters.route("/<int:id>/", methods=["DELETE"])
def delete_character(id):
    
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(400, description="Character doesn't exist")
    
    db.session.delete(character)
    commit_or_abort()

    return "", 204


# @characters.route("/418/", methods=["GET"])
# def teapot():
#     return jsonify({"I'm a teapot": "Want some tea?"}), 418
