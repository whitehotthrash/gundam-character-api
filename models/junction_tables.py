from init import db

character_affiliation = db.Table(
    "character_affiliation",
    db.Column(
        "character_id",
        db.Integer,
        db.ForeignKey("character.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "affiliation_id",
        db.Integer,
        db.ForeignKey("affiliation.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

character_occupation = db.Table(
    "character_occupation",
    db.Column(
        "character_id",
        db.Integer,
        db.ForeignKey("character.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "occupation_id",
        db.Integer,
        db.ForeignKey("occupation.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
