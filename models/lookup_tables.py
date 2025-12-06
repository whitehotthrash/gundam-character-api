from init import db
from models.junction_tables import character_affiliation, character_occupation

class Affiliation(db.Model):
    __tablename__ = "affiliation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    characters = db.relationship(
        "Character",
        secondary=character_affiliation,
        back_populates="affiliations"
    )

class Occupation(db.Model):
    __tablename__ = "occupation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    characters = db.relationship(
        "Character",
        secondary=character_occupation,
        back_populates="occupations"
    )