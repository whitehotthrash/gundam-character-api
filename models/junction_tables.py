from main import db

class CharacterAffiliation(db.Model):

    __tablename__ = "character_affiliation"
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), primary_key=True
    )
    affiliation_id = db.Column(
        db.Integer, db.ForeignKey("affiliation.id"), primary_key=True
    )


class CharacterOccupation(db.Model):

    __tablename__ = "character_occupation"
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), primary_key=True
    )
    occupation_id = db.Column(
        db.Integer, db.ForeignKey("occupation.id"), primary_key=True
    )

