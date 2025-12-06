from init import ma
from models.character import Character


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        ordered = True


# single character schema
character_schema = CharacterSchema()
# multiple character schema
characters_schema = CharacterSchema(many=True)
