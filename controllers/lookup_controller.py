from flask import Blueprint, jsonify, request, abort
from init import db
from models.lookup_tables import Affiliation, Occupation
from schemas.lookup_schema import (
    affiliation_schema,
    affiliations_schema,
    occupation_schema,
    occupations_schema,
)

lookups = Blueprint("lookups", __name__, url_prefix="/lookups")


# GET endpoint for affiliations
@lookups.route("/affiliations/", methods=["GET"])
def get_affiliations():
    stmt = db.select(Affiliation)
    affiliations_list = db.session.scalars(stmt)
    result = affiliations_schema.dump(affiliations_list)
    return jsonify(result)


# GET endpoint for occupations
@lookups.route("/occupations/", methods=["GET"])
def get_occupations():
    stmt = db.select(Occupation)
    occupations_list = db.session.scalars(stmt)
    result = occupations_schema.dump(occupations_list)
    return jsonify(result)


# POST endpoint for occupations
@lookups.route("/occupations/", methods=["POST"])
def create_occupation():
    occupation_fields = occupation_schema.load(request.json)
    new_occupation = Occupation()
    new_occupation.name = occupation_fields["name"]
    db.session.add(new_occupation)
    db.session.commit()
    return jsonify(occupation_schema.dump(new_occupation))


# POST endpoint for affiliations
@lookups.route("/", methods=["POST"])
def create_affiliation():
    affiliation_fields = affiliation_schema.load(request.json)
    new_affiliation = Affiliation()
    new_affiliation.name = affiliation_fields["name"]
    db.session.add(new_affiliation)
    db.session.commit()
    return jsonify(affiliation_schema.dump(new_affiliation))


# DELETE endpoint for affiliations
@lookups.route("/<int:id>/", methods=["DELETE"])
def delete_affiliation(id):
    stmt = db.select(Affiliation).filter_by(id=id)
    affiliation = db.session.scalar(stmt)
    if not affiliation:
        return abort(400, description="Affiliation doesn't exist")
    db.session.delete(affiliation)
    db.session.commit()
    return jsonify(affiliation_schema.dump(affiliation))


# DELETE endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["DELETE"])
def delete_occupation(id):
    stmt = db.select(Occupation).filter_by(id=id)
    occupation = db.session.scalar(stmt)
    if not occupation:
        return abort(400, description="Occupation doesn't exist")
    db.session.delete(occupation)
    db.session.commit()
    return jsonify(occupation_schema.dump(occupation))
