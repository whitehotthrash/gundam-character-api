from main import ma

class CharacterAffiliationSchema(ma.Schema):
    class Meta:
        fields = ("character_id", "affiliation_id")


character_affiliation_schema = CharacterAffiliationSchema()
character_affiliations_schema = CharacterAffiliationSchema(many=True)


class CharacterOccupationSchema(ma.Schema):
    class Meta:
        fields = ("character_id", "occupation_id")


character_occupation_schema = CharacterOccupationSchema()
character_occupations_schema = CharacterOccupationSchema(many=True)