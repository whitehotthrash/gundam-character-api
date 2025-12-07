from datetime import date
from flask import Blueprint
from init import db
from models.character import Character
from models.lookup_tables import Affiliation, Occupation
import click

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    try:
        db.create_all()
        print("Tables created.")
    except Exception as e:
        raise click.ClickException(f"Failed to create tables: {e}")


@db_commands.cli.command("drop")
def drop_db():
    try:
        db.drop_all()
        print("Tables dropped.")
    except Exception as e:
        raise click.ClickException(f"Failed to drop tables: {e}")


@db_commands.cli.command("seed")
def seed_db():
    try:
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

        affiliation_assignments = {
          "Uso Ewin": ["League Militaire"],
          "Katejina Loos": ["Zanscare Empire"],
          "Cronicle Asher": ["Zanscare Empire"],
          "Marbet Fingerhat": ["League Militaire"],
          "Mahalia Merrill": ["League Militaire"],
          "Fuala Griffon": ["Zanscare Empire"],
          "Fonse Kagatie": ["Zanscare Empire"],
        }

        occupation_assignments = {
          "Uso Ewin": ["Mobile Suit Pilot"],
          "Katejina Loos": ["Mobile Suit Pilot"],
          "Cronicle Asher": ["Mobile Suit Pilot"],
          "Marbet Fingerhat": ["Mobile Suit Pilot"],
          "Mahalia Merrill": ["Mobile Suit Pilot"],
          "Fuala Griffon": ["Mobile Suit Pilot"],
          "Fonse Kagatie": ["Supreme Commander"],
        }
        
        for char_name, aff_list in affiliation_assignments.items():
          char = characters_by_name[char_name]
          for aff_name in aff_list:
            char.affiliations.append(affiliations[aff_name])

        for char_name, occ_list in occupation_assignments.items():
          char = characters_by_name[char_name]
          for occ_name in occ_list:
            char.occupations.append(occupations[occ_name])

        # Add all characters and lookups to session (relationships handled automatically)
        db.session.add_all(characters + list(affiliations.values()) + list(occupations.values()))
        db.session.commit()

        print("Database seeded with Victory Gundam characters, affiliations, and occupations.")
    except Exception as e:
        # Convert unexpected errors into clickable errors for the terminal
        raise click.ClickException(f"Failed to seed database: {e}")
