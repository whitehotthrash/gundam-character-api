from main import ma

# create the Participant Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class LookupSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "address", "phone")

# single participant schema, when one participant needs to be retrieved
lookup_schema = LookupSchema()
# multiple participant schema, when many participants need to be retrieved
lookups_schema = LookupSchema(many=True)