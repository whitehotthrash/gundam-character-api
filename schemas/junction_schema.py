from main import ma

# create the Participant Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class JunctionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "address", "phone")

# single participant schema, when one participant needs to be retrieved
junction_schema = JunctionSchema()
# multiple participant schema, when many participants need to be retrieved
junctions_schema = JunctionSchema(many=True)