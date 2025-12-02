from main import db

class Affiliation(db.Model):
    __tablename__ = "affiliation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)


class Occupation(db.Model):
    __tablename__ = "occupation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
