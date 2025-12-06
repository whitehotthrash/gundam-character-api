from init import ma
from models.junction_tables import CharacterAffiliation, CharacterOccupation


class CharacterAffiliationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterAffiliation
        load_instance = True
        include_fk = True


character_affiliation_schema = CharacterAffiliationSchema()
character_affiliations_schema = CharacterAffiliationSchema(many=True)


class CharacterOccupationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterOccupation
        load_instance = True
        include_fk = True


character_occupation_schema = CharacterOccupationSchema()
character_occupations_schema = CharacterOccupationSchema(many=True)
