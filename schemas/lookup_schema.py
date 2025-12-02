from main import ma

class LookupSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

# single lookup schema
lookup_schema = LookupSchema()
# multiple lookup schema
lookups_schema = LookupSchema(many=True)