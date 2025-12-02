from main import db

class Character(db.Model):
    # Core character table storing canonical bio information
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    birth_year = db.Column(db.Date, nullable=True)
    classification = db.Column(db.String(), nullable=False)
    place_of_birth = db.Column(db.String(), nullable=True)
    rank = db.Column(db.String(), nullable=True)
    status = db.Column(db.String(), nullable=False)