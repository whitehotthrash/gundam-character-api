from init import db
from models.junction_tables import character_affiliation, character_occupation

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    birth_year = db.Column(db.Date, nullable=True)
    classification = db.Column(db.String(), nullable=False)
    place_of_birth = db.Column(db.String(), nullable=True)
    rank = db.Column(db.String(), nullable=True)
    status = db.Column(db.String(), nullable=False)

    affiliations = db.relationship(
        "Affiliation",
        secondary=character_affiliation,
        back_populates="characters"
    )
    occupations = db.relationship(
        "Occupation",
        secondary=character_occupation,
        back_populates="characters"
    )