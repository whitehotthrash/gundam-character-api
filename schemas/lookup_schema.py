from marshmallow import Schema, fields


class LookupSchema(Schema):
    id = fields.Int()
    name = fields.Str()


affiliation_schema = LookupSchema()
affiliations_schema = LookupSchema(many=True)

occupation_schema = LookupSchema()
occupations_schema = LookupSchema(many=True)
