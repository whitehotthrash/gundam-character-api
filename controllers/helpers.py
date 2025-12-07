from flask import request, abort
from init import db
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

# To keep the controllers DRY, this helpers file contains common functions
# that are used in multiple controllers.

def get_json_or_empty():
    data = request.get_json()
    return data if data is not None else {}


def load_schema_or_abort(schema, data=None, session=None, partial=False):
    payload = data if data is not None else request.get_json()
    try:
        return schema.load(payload, session=session, partial=partial)
    except ValidationError as e:
        # Keep behavior consistent with existing controllers
        abort(400, description={"errors": e.messages})


def fetch_or_abort(model, id_, not_found_message=None, http_code=404):
    stmt = db.select(model).filter_by(id=id_)
    obj = db.session.scalar(stmt)
    if not obj:
        abort(http_code, description=not_found_message or f"{model.__name__} doesn't exist")
    return obj


def validate_ids_exist_or_abort(model, ids, name="Resource"):
    instances = []
    missing = []
    for _id in ids:
        inst = db.session.get(model, _id)
        if not inst:
            missing.append(_id)
        else:
            instances.append(inst)
    if missing:
        abort(404, description=f"{name} id(s) not found: {missing}")
    return instances


def commit_or_abort():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, description=f"Database error: {e}")
