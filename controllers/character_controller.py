from flask import Blueprint, jsonify, request, abort
from init import db
from models.character import Character
from schemas.character_schema import character_schema, CharacterSchema
from models.lookup_tables import Affiliation, Occupation
from models.junction_tables import character_affiliation, character_occupation
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

characters = Blueprint("characters", __name__, url_prefix="/characters")


@characters.route("/", methods=["GET"])
def get_characters():
    # get all the characters from the database table
    characters_list = Character.query.all()
    # Convert the characters from the database into a JSON format and store them in result
    result = CharacterSchema(many=True).dump(characters_list)
    # return the data in JSON format
    return jsonify(result)

@characters.route("/<int:id>/", methods=["GET"])
def get_character(id):
    # get a single character from the database
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    if not character:
        return abort(404, description="Character doesn't exist")
    result = character_schema.dump(character)
    return jsonify(result)

@characters.route("/", methods=["POST"])
def create_character():
    # Create a new character
    data = request.get_json()
    try:
        character_fields = character_schema.load(data, session=db.session)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})
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
        for affiliation_id in character_fields["affiliation_ids"]:
            affiliation = Affiliation.query.get(affiliation_id)
            if not affiliation:
                db.session.rollback()
                return abort(404, description=f"Affiliation with id {affiliation_id} not found")
            new_character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        for occupation_id in character_fields["occupation_ids"]:
            occupation = Occupation.query.get(occupation_id)
            if not occupation:
                db.session.rollback()
                return abort(404, description=f"Occupation with id {occupation_id} not found")
            new_character.occupations.append(occupation)
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(character_schema.dump(new_character)), 201


@characters.route("/<int:id>/", methods=["PUT"])
def update_character(id):
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(404, description="Character doesn't exist")
    
    data = request.get_json()
    try:
        character_fields = character_schema.load(data, session=db.session, partial=False)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})
    
    character.name = character_fields["name"]
    character.birth_year = character_fields["birth_year"]
    character.classification = character_fields["classification"]
    character.place_of_birth = character_fields["place_of_birth"]
    character.rank = character_fields["rank"]
    character.status = character_fields["status"]
    
    # Handle affiliations
    if "affiliation_ids" in character_fields:
        character.affiliations.clear()
        for affiliation_id in character_fields["affiliation_ids"]:
            affiliation = Affiliation.query.get(affiliation_id)
            if not affiliation:
                db.session.rollback()
                return abort(404, description=f"Affiliation with id {affiliation_id} not found")
            character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        character.occupations.clear()
        for occupation_id in character_fields["occupation_ids"]:
            occupation = Occupation.query.get(occupation_id)
            if not occupation:
                db.session.rollback()
                return abort(404, description=f"Occupation with id {occupation_id} not found")
            character.occupations.append(occupation)
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(character_schema.dump(character)), 200


@characters.route("/<int:id>/", methods=["PATCH"])
def patch_character(id):
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(404, description="Character doesn't exist")
    
    data = request.get_json()
    try:
        character_fields = character_schema.load(data, session=db.session, partial=True)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})
    
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
        for affiliation_id in character_fields["affiliation_ids"]:
            affiliation = Affiliation.query.get(affiliation_id)
            if not affiliation:
                db.session.rollback()
                return abort(404, description=f"Affiliation with id {affiliation_id} not found")
            character.affiliations.append(affiliation)
    
    # Handle occupations
    if "occupation_ids" in character_fields:
        character.occupations.clear()
        for occupation_id in character_fields["occupation_ids"]:
            occupation = Occupation.query.get(occupation_id)
            if not occupation:
                db.session.rollback()
                return abort(404, description=f"Occupation with id {occupation_id} not found")
            character.occupations.append(occupation)
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(character_schema.dump(character)), 200


@characters.route("/<int:id>/", methods=["DELETE"])
def delete_character(id):
    
    stmt = db.select(Character).filter_by(id=id)
    character = db.session.scalar(stmt)
    
    if not character:
        return abort(400, description="Character doesn't exist")
    
    db.session.delete(character)
    db.session.commit()
    
    return jsonify(character_schema.dump(character))
