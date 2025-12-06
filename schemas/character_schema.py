from init import ma
from models.character import Character
# from marshmallow import fields
# from schemas.lookup_schema import affiliations_schema


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    # affiliations = fields.List(fields.Integer(), load_only=True)
    # affiliations = fields.Nested(affiliations_schema, only=["id"], many=True)
    # affiliations = ma.Nested(affiliations_schema, only=["id"])
    # occupations  = fields.List(fields.Integer(), load_only=True)
    class Meta:
        model = Character
        load_instance = True
        ordered = True
        include_relationships = False


# single character schema
character_schema = CharacterSchema()
# multiple character schema
characters_schema = CharacterSchema(many=True)
