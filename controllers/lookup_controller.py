from flask import Blueprint, jsonify, request
from init import db
from models.lookup_tables import Affiliation, Occupation
from schemas.lookup_schema import (
    affiliation_schema,
    affiliations_schema,
    occupation_schema,
    occupations_schema,
)
from controllers.helpers import (
    load_schema_or_abort,
    commit_or_abort,
    get_json_or_empty,
    fetch_or_abort,
)

lookups = Blueprint("lookups", __name__, url_prefix="/lookups")


# GET endpoint for affiliations
@lookups.route("/affiliations/", methods=["GET"])
def get_affiliations():
    stmt = db.select(Affiliation)
    affiliations_list = db.session.scalars(stmt)
    result = affiliations_schema.dump(affiliations_list)
    return jsonify(result), 200


# GET single affiliation
@lookups.route("/affiliations/<int:id>/", methods=["GET"])
def get_affiliation(id):
    affiliation = fetch_or_abort(Affiliation, id, not_found_message="Affiliation doesn't exist")
    return jsonify(affiliation_schema.dump(affiliation)), 200


# GET endpoint for occupations
@lookups.route("/occupations/", methods=["GET"])
def get_occupations():
    stmt = db.select(Occupation)
    occupations_list = db.session.scalars(stmt)
    result = occupations_schema.dump(occupations_list)
    return jsonify(result), 200


# GET single occupation
@lookups.route("/occupations/<int:id>/", methods=["GET"])
def get_occupation(id):
    occupation = fetch_or_abort(Occupation, id, not_found_message="Occupation doesn't exist")
    return jsonify(occupation_schema.dump(occupation)), 200


# POST endpoint for occupations
@lookups.route("/occupations/", methods=["POST"])
def create_occupation():
    occupation_fields = load_schema_or_abort(occupation_schema, data=request.json)

    new_occupation = Occupation()
    new_occupation.name = occupation_fields["name"]
    db.session.add(new_occupation)
    commit_or_abort()

    return jsonify(occupation_schema.dump(new_occupation)), 201


# POST endpoint for affiliations
@lookups.route("/affiliations/", methods=["POST"])
def create_affiliation():
    affiliation_fields = load_schema_or_abort(affiliation_schema, data=request.json)

    new_affiliation = Affiliation()
    new_affiliation.name = affiliation_fields["name"]
    db.session.add(new_affiliation)
    commit_or_abort()

    return jsonify(affiliation_schema.dump(new_affiliation)), 201


# DELETE endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["DELETE"])
def delete_affiliation(id):
    affiliation = fetch_or_abort(Affiliation, id, not_found_message="Affiliation doesn't exist", http_code=400)
    db.session.delete(affiliation)
    commit_or_abort()
    return jsonify({"success": "affiliation deleted"}), 200


# DELETE endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["DELETE"])
def delete_occupation(id):
    occupation = fetch_or_abort(Occupation, id, not_found_message="Occupation doesn't exist", http_code=400)
    db.session.delete(occupation)
    commit_or_abort()
    return jsonify({"success": "occupation deleted"}), 200


# PUT endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["PUT"])
def update_affiliation(id):
    affiliation = fetch_or_abort(Affiliation, id, not_found_message="Affiliation doesn't exist")
    affiliation_fields = load_schema_or_abort(affiliation_schema, data=request.json)
    affiliation.name = affiliation_fields["name"]
    commit_or_abort()
    return jsonify(affiliation_schema.dump(affiliation)), 200


# PATCH endpoint for affiliations
@lookups.route("/affiliations/<int:id>/", methods=["PATCH"])
def patch_affiliation(id):
    affiliation = fetch_or_abort(Affiliation, id, not_found_message="Affiliation doesn't exist")
    data = get_json_or_empty()
    if not data:
        return jsonify(affiliation_schema.dump(affiliation)), 200

    if "name" in data:
        affiliation_fields = load_schema_or_abort(affiliation_schema, data={"name": data["name"]})
        affiliation.name = affiliation_fields["name"]

    commit_or_abort()
    return jsonify(affiliation_schema.dump(affiliation)), 200


# PUT endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["PUT"])
def update_occupation(id):
    occupation = fetch_or_abort(Occupation, id, not_found_message="Occupation doesn't exist")
    occupation_fields = load_schema_or_abort(occupation_schema, data=request.json)
    occupation.name = occupation_fields["name"]
    commit_or_abort()
    return jsonify(occupation_schema.dump(occupation)), 200


# PATCH endpoint for occupations
@lookups.route("/occupations/<int:id>/", methods=["PATCH"])
def patch_occupation(id):
    occupation = fetch_or_abort(Occupation, id, not_found_message="Occupation doesn't exist")
    data = get_json_or_empty()
    if not data:
        return jsonify(occupation_schema.dump(occupation)), 200

    if "name" in data:
        occupation_fields = load_schema_or_abort(occupation_schema, data={"name": data["name"]})
        occupation.name = occupation_fields["name"]

    commit_or_abort()
    return jsonify(occupation_schema.dump(occupation)), 200
