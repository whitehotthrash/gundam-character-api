from datetime import date
from flask import Blueprint
from init import db
from models.character import Character
from models.lookup_tables import Affiliation, Occupation
from models.junction_tables import CharacterAffiliation, CharacterOccupation

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created.")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped.")


@db_commands.cli.command("seed")
def seed_db():
    # Characters from Mobile Suit Victory Gundam, UC 0153 era
    characters = [
        Character(
            name="Uso Ewin",
            birth_year=date(140, 4, 17),
            classification="newtype",
            place_of_birth="Earth",
            rank="Pilot",
            status="Alive",
        ),
        Character(
            name="Katejina Loos",
            birth_year=date(136, 1, 20),
            classification="oldtype",
            place_of_birth="Earth",
            rank="Pilot",
            status="Alive",
        ),
        Character(
            name="Cronicle Asher",
            birth_year=date(133, 7, 1),
            classification="oldtype",
            place_of_birth="Side 1",
            rank="Lieutenant",
            status="Killed In Action",
        ),
        Character(
            name="Marbet Fingerhat",
            birth_year=date(129, 9, 29),
            classification="oldtype",
            place_of_birth="Earth",
            rank="Lieutenant",
            status="Alive",
        ),
        Character(
            name="Mahalia Merrill",
            birth_year=date(134, 10, 10),
            classification="oldtype",
            place_of_birth="Earth",
            rank="Ensign",
            status="Killed In Action",
        ),
        Character(
            name="Fuala Griffon",
            birth_year=date(132, 12, 23),
            classification="oldtype",
            place_of_birth="Side 1",
            rank="Commander",
            status="Killed In Action",
        ),
        Character(
            name="Fonse Kagatie",
            birth_year=date(88, 3, 5),
            classification="oldtype",
            place_of_birth="Jupiter Colony",
            rank="Supreme Commander",
            status="Killed In Action",
        ),
    ]

    # Lookup tables
    affiliation_names = [
        "League Militaire",
        "Zanscare Empire",
    ]
    occupation_names = [
        "Mobile Suit Pilot",
        "Commander",
        "Supreme Commander",
    ]

    affiliations = {name: Affiliation(name=name) for name in affiliation_names}
    occupations = {name: Occupation(name=name) for name in occupation_names}

    # Persist base records and get primary keys
    db.session.add_all(
        characters + list(affiliations.values()) + list(occupations.values())
    )
    db.session.flush()

    characters_by_name = {c.name: c for c in characters}

    # Junction: character <> affiliation
    character_affiliations = [
        CharacterAffiliation(
            character_id=characters_by_name["Uso Ewin"].id,
            affiliation_id=affiliations["League Militaire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Katejina Loos"].id,
            affiliation_id=affiliations["Zanscare Empire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Cronicle Asher"].id,
            affiliation_id=affiliations["Zanscare Empire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Marbet Fingerhat"].id,
            affiliation_id=affiliations["League Militaire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Mahalia Merrill"].id,
            affiliation_id=affiliations["League Militaire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Fuala Griffon"].id,
            affiliation_id=affiliations["Zanscare Empire"].id,
        ),
        CharacterAffiliation(
            character_id=characters_by_name["Fonse Kagatie"].id,
            affiliation_id=affiliations["Zanscare Empire"].id,
        ),
    ]

    # Junction: character <> occupation
    character_occupations = [
        CharacterOccupation(
            character_id=characters_by_name["Uso Ewin"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Katejina Loos"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Cronicle Asher"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Marbet Fingerhat"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Mahalia Merrill"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Fuala Griffon"].id,
            occupation_id=occupations["Mobile Suit Pilot"].id,
        ),
        CharacterOccupation(
            character_id=characters_by_name["Fonse Kagatie"].id,
            occupation_id=occupations["Supreme Commander"].id,
        ),
    ]

    db.session.add_all(character_affiliations + character_occupations)
    db.session.commit()
    print(
        "Database seeded with Victory Gundam characters, affiliations, and occupations."
    )
