from init import ma

class LookupSchema(ma.Schema):
  class Meta:
    fields = ("id", "name")

affiliation_schema = LookupSchema()
affiliations_schema = LookupSchema(many=True)

occupation_schema = LookupSchema()
occupations_schema = LookupSchema(many=True)