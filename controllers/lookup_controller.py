from flask import Blueprint, jsonify, request, abort
from init import db
from models.lookup_tables import Affiliation, Occupation
from schemas.lookup_schema import (
    affiliation_schema,
    affiliations_schema,
    occupation_schema,
    occupations_schema,
)
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

lookups = Blueprint("lookups", __name__, url_prefix="/lookups")


# GET endpoint for affiliations
@lookups.route("/affiliations/", methods=["GET"])
def get_affiliations():
    stmt = db.select(Affiliation)
    affiliations_list = db.session.scalars(stmt)
    result = affiliations_schema.dump(affiliations_list)
    return jsonify(result)


# GET single affiliation
@lookups.route("/affiliations/<int:id>/", methods=["GET"])
def get_affiliation(id):
    stmt = db.select(Affiliation).filter_by(id=id)
    affiliation = db.session.scalar(stmt)
    if not affiliation:
        return abort(404, description="Affiliation doesn't exist")
    return jsonify(affiliation_schema.dump(affiliation))


# GET endpoint for occupations
@lookups.route("/occupations/", methods=["GET"])
def get_occupations():
    stmt = db.select(Occupation)
    occupations_list = db.session.scalars(stmt)
    result = occupations_schema.dump(occupations_list)
    return jsonify(result)


# GET single occupation
@lookups.route("/occupations/<int:id>/", methods=["GET"])
def get_occupation(id):
    stmt = db.select(Occupation).filter_by(id=id)
    occupation = db.session.scalar(stmt)
    if not occupation:
        return abort(404, description="Occupation doesn't exist")
    return jsonify(occupation_schema.dump(occupation))


# POST endpoint for occupations
@lookups.route("/occupations/", methods=["POST"])
def create_occupation():
    try:
        occupation_fields = occupation_schema.load(request.json)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})

    new_occupation = Occupation()
    new_occupation.name = occupation_fields["name"]
    db.session.add(new_occupation)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(occupation_schema.dump(new_occupation))


# POST endpoint for affiliations
@lookups.route("/affiliations/", methods=["POST"])
def create_affiliation():
    try:
        affiliation_fields = affiliation_schema.load(request.json)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})

    new_affiliation = Affiliation()
    new_affiliation.name = affiliation_fields["name"]
    db.session.add(new_affiliation)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(affiliation_schema.dump(new_affiliation))


# DELETE endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["DELETE"])
def delete_affiliation(id):
    stmt = db.select(Affiliation).filter_by(id=id)
    affiliation = db.session.scalar(stmt)
    if not affiliation:
        return abort(400, description="Affiliation doesn't exist")
    db.session.delete(affiliation)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")
    return jsonify(affiliation_schema.dump(affiliation))


# DELETE endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["DELETE"])
def delete_occupation(id):
    stmt = db.select(Occupation).filter_by(id=id)
    occupation = db.session.scalar(stmt)
    if not occupation:
        return abort(400, description="Occupation doesn't exist")
    db.session.delete(occupation)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")
    return jsonify(occupation_schema.dump(occupation))


# PUT endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["PUT"])
def update_affiliation(id):
    stmt = db.select(Affiliation).filter_by(id=id)
    affiliation = db.session.scalar(stmt)
    if not affiliation:
        return abort(404, description="Affiliation doesn't exist")
    
    try:
        affiliation_fields = affiliation_schema.load(request.json)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})

    affiliation.name = affiliation_fields["name"]
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(affiliation_schema.dump(affiliation)), 200


# PATCH endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["PATCH"])
def patch_affiliation(id):
    stmt = db.select(Affiliation).filter_by(id=id)
    affiliation = db.session.scalar(stmt)
    if not affiliation:
        return abort(404, description="Affiliation doesn't exist")
    
    data = request.get_json()
    if not data:
        return jsonify(affiliation_schema.dump(affiliation)), 200
    
    if "name" in data:
        try:
            affiliation_fields = affiliation_schema.load({"name": data["name"]})
        except ValidationError as e:
            return abort(400, description={"errors": e.messages})
        affiliation.name = affiliation_fields["name"]
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")
    return jsonify(affiliation_schema.dump(affiliation)), 200


# PUT endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["PUT"])
def update_occupation(id):
    stmt = db.select(Occupation).filter_by(id=id)
    occupation = db.session.scalar(stmt)
    if not occupation:
        return abort(404, description="Occupation doesn't exist")
    
    try:
        occupation_fields = occupation_schema.load(request.json)
    except ValidationError as e:
        return abort(400, description={"errors": e.messages})

    occupation.name = occupation_fields["name"]
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")

    return jsonify(occupation_schema.dump(occupation)), 200


# PATCH endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["PATCH"])
def patch_occupation(id):
    stmt = db.select(Occupation).filter_by(id=id)
    occupation = db.session.scalar(stmt)
    if not occupation:
        return abort(404, description="Occupation doesn't exist")
    
    data = request.get_json()
    if not data:
        return jsonify(occupation_schema.dump(occupation)), 200
    
    if "name" in data:
        try:
            occupation_fields = occupation_schema.load({"name": data["name"]})
        except ValidationError as e:
            return abort(400, description={"errors": e.messages})
        occupation.name = occupation_fields["name"]
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return abort(500, description=f"Database error: {e}")
    return jsonify(occupation_schema.dump(occupation)), 200
