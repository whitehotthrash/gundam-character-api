from init import ma
from marshmallow import Schema, fields
from schemas.lookup_schema import affiliations_schema, occupations_schema, LookupSchema


class CharacterSchema(ma.SQLAlchemyAutoSchema):
  id = fields.Int()
  name = fields.Str()
  birth_year = fields.Date()
  classification = fields.Str()
  place_of_birth = fields.Str()
  rank = fields.Str()
  status = fields.Str()
  affiliations = fields.Nested(affiliations_schema, many=True)
  occupations = fields.Nested(occupations_schema, many=True)
  affiliation_ids = fields.List(fields.Int(), load_only=True)
  occupation_ids = fields.List(fields.Int(), load_only=True)


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)