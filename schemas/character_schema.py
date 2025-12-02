from main import ma

class CharacterSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "birth_year", "classification", "place_of_birth", "rank", "status")

# single character schema
character_schema = CharacterSchema()
# multiple character schema
characters_schema = CharacterSchema(many=True)