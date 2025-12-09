# Gundam Character API

A compact RESTful API that stores characters from the Mobile Suit Gundam universe, their affiliations, and occupations.

Built with Flask, SQLAlchemy and Marshmallow. The project is intended for local development and simple production deployment behind a WSGI server such as Gunicorn.

## Overview

Data model (summary):
- `Character` — core entity with attributes like `id`, `name`, `birth_year`, `classification`, `place_of_birth`, `rank`, `status`.
- `Affiliation` and `Occupation` — lookup tables to normalize repeated categorical values.
- `character_affiliation` and `character_occupation` — many-to-many join tables linking `Character` to lookups.

The design follows normalization best-practices to avoid duplicated textual values while keeping character data compact.

## Entity Relationship Diagram

![ERD](./assets/character_erd.drawio.png)

A character can have none, one or multiple affiliations.
A character can have none, one or multiple occupations.
Lookup tables are provided for affiliations and occupations.
Junction tables define the M:M relationships between characters and their affiliations/ occupations.

## Features

- Full CRUD for characters, affiliations and occupations.
- Many-to-many relationships managed by SQLAlchemy ORM.
- Validation and serialization via Marshmallow schemas.
- Centralized JSON error responses and clear HTTP status codes.
- `flask` CLI commands for DB create/drop/seed (development convenience).

## Technical prerequisites & technologies

- Python 3.10+ — the project is developed and tested on Python 3.10+. Use a virtual environment for local development.
- A SQL database: PostgreSQL is recommended for development and production. The database is referenced via the `DATABASE_URL` env var. Other SQL backends supported by SQLAlchemy may work but are not explicitly tested.
- Key libraries (from `requirements.txt`): `Flask`, `Flask-SQLAlchemy`, `flask-marshmallow`, `marshmallow`, `marshmallow-sqlalchemy`, `psycopg2-binary`, `SQLAlchemy`, `Werkzeug`.
- WSGI server for production: `gunicorn` (recommended).

This repository's `requirements.txt` pins the versions used during development; see that file for exact package versions.

## Production

This project includes a live production deployment using Neon and Render.

**Live Environment: https://gundam-character-api.onrender.com/characters/

## Quick start (local)

Prerequisites:
- Python 3.10+
- A SQL database (Postgres recommended) reachable via `DATABASE_URL`.

### PostgreSQL setup (install and create database)

These steps show how to install PostgreSQL and create the database and user the app needs. Pick the section matching your OS. The examples create a database named `gundam_api_db` and a DB user `admin` — adapt names and passwords to your environment.

Important SQL (run after installing Postgres):

```sql
-- create a role with password
CREATE ROLE admin WITH LOGIN PASSWORD '123456';
-- create the database owned by that role
CREATE DATABASE gundam_api_db OWNER admin;
-- grant privileges on the database
GRANT ALL PRIVILEGES ON DATABASE gundam_api_db TO admin;
```

Connection string example (set as `DATABASE_URL`):

```
postgresql+psycopg2://admin:123456@localhost:5432/gundam_api_db
```

macOS (Homebrew)

```bash
# install Postgres via Homebrew
brew update
brew install postgresql

# start Postgres (launchctl / services)
brew services start postgresql

# create role and db using psql
createuser -s postgres || true
psql -d postgres -c "CREATE ROLE admin WITH LOGIN PASSWORD '123456';"
psql -d postgres -c "CREATE DATABASE gundam_api_db OWNER admin;"
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE gundam_api_db TO admin;"
```

Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# start/enable service
sudo systemctl enable --now postgresql

# create role and db as the postgres superuser
sudo -u postgres psql -c "CREATE ROLE admin WITH LOGIN PASSWORD '123456';"
sudo -u postgres psql -c "CREATE DATABASE gundam_api_db OWNER admin;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gundam_api_db TO admin;"
```

Fedora / CentOS / RHEL (dnf)

```bash
sudo dnf install -y postgresql-server postgresql-contrib

# initialize DB (may vary by distribution)
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql

sudo -u postgres psql -c "CREATE ROLE admin WITH LOGIN PASSWORD '123456';"
sudo -u postgres psql -c "CREATE DATABASE gundam_api_db OWNER admin;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gundam_api_db TO admin;"
```

Windows

Option A — Installer (recommended):

- Download the Windows installer from https://www.postgresql.org/download/windows/ and run it. The installer also includes `psql` and StackBuilder.
- Use the pgAdmin UI or open `psql` and run the SQL commands above to create the user and database.

Option B — Chocolatey (if you like Chocolate):

```powershell
choco install postgresql
# after install, initialize and start service via Services or use pg_ctl as instructed by the installer
# run psql (may need to add psql to PATH) and execute SQL statements above
```

Option C — WSL (Windows Subsystem for Linux)

If you use WSL, follow the Ubuntu/Debian instructions inside your WSL shell. Then set `DATABASE_URL` in Windows or in the same environment where you run Flask.

Testing the connection

```bash
# list databases
psql "postgresql://admin:123456@localhost:5432/gundam_api_db" -c "\l"

# connect to the db
psql "postgresql://admin:123456@localhost:5432/gundam_api_db"
```

### Application setup

1. Clone and open the project root (the API code lives in this repository):

```bash
git clone https://github.com/whitehotthrash/gundam-character-api.git
cd gundam-character-api
```

2. Create a virtual environment and install dependencies.

macOS / Linux (bash/zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows (cmd.exe):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

3. Set environment variables (example). On Windows use PowerShell `setx` or set in the session with `$env:DATABASE_URL = '...'`.

macOS / Linux / Windows (bash / PowerShell example):

```bash
export DATABASE_URL=postgresql+psycopg2://admin:123456@localhost:5432/gundam_api_db
export FLASK_APP=main:create_app
export FLASK_ENV=development
```

PowerShell session example:

```powershell
$env:DATABASE_URL = 'postgresql+psycopg2://admin:123456@localhost:5432/gundam_api_db'
$env:FLASK_APP = 'main:create_app'
$env:FLASK_ENV = 'development'
```

4. Initialize the database and (optionally) seed development data:

```bash
flask db create
flask db seed
```

5. Run the development server:

```bash
flask run
```

API base: `http://127.0.0.1:5000/`

## API Endpoints (summary)

Base path: `/characters/`

Characters
- `GET /characters/` — list characters (200)
- `GET /characters/<id>/` — retrieve a character (200)
- `POST /characters/` — create a character (201)
  - Accepts optional `affiliation_ids` and `occupation_ids` arrays to link lookups
- `PUT /characters/<id>/` — replace a character (200)
- `PATCH /characters/<id>/` — modify a character (200)
- `DELETE /characters/<id>/` — delete a character (204)

Lookups (Affiliations & Occupations)
- `GET /lookups/affiliations/` — list affiliations (200)
- `GET /lookups/affiliations/<id>/` — get one affiliation (200)
- `POST /lookups/affiliations/` — create affiliation (201)
- `PUT /lookups/affiliations/<id>/` — replace affiliation (200)
- `PATCH /lookups/affiliations/<id>/` — modify affiliation (200)
- `DELETE /lookups/affiliations/<id>/` — delete affiliation (204)

Same endpoints are available under `/lookups/occupations/` for occupations.

## Example Usage

GET /characters/1/

```json
{
  "affiliations": [
    {
      "id": 1,
      "name": "League Militaire"
    }
  ],
  "birth_year": "0140-04-17",
  "classification": "newtype",
  "id": 1,
  "name": "Uso Ewin",
  "occupations": [
    {
      "id": 1,
      "name": "Mobile Suit Pilot"
    }
  ],
  "place_of_birth": "Earth",
  "rank": "Pilot",
  "status": "Alive"
}
```

POST /characters/
```json
{
  "affiliation_ids": [1],
  "birth_year": "0058-04-17",
  "classification": "newtype",
  "name": "Amuro Ray",
  "occupation_ids": [1],
  "place_of_birth": "Earth",
  "rank": "Pilot",
  "status": "Killed In Action"
}
```

PATCH /characters/8
```json
{
  "affiliation_ids": [2],
  "occupation_ids": [2]
}
```

DELETE /characters/8
Expected return message:
```json
{
  "success": "character deleted"
}
```

## Validation & Sanitisation

- Marshmallow schemas enforce types and structure for requests and responses.
- `affiliation_ids` / `occupation_ids` are validated to exist before being applied to relationships.
- Centralized error handlers return consistent JSON error payloads for validation and HTTP errors.

## Acknowledgements

This project is built on and relies on the following open-source software and tools:

**Database & ORM**
- [PostgreSQL](https://www.postgresql.org/) — A powerful, open source object-relational database system. Licensed under the PostgreSQL License (permissive, similar to BSD). See [PostgreSQL License](https://www.postgresql.org/about/licence/).
- [SQLAlchemy](https://www.sqlalchemy.org/) — The Python SQL toolkit and Object Relational Mapper. Licensed under the MIT License. See [SQLAlchemy License](https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE).

**Web Framework & Serialization**
- [Flask](https://flask.palletsprojects.com/) — A lightweight WSGI web application framework. Licensed under the BSD 3-Clause License. See [Flask License](https://github.com/pallets/flask/blob/main/LICENSE.rst).
- [Marshmallow](https://marshmallow.readthedocs.io/) — An ORM/ODM/framework-agnostic library for converting complex data types. Licensed under the MIT License. See [Marshmallow License](https://github.com/marshmallow-code/marshmallow/blob/dev/LICENSE).
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/) — Flask integration for Marshmallow. Licensed under the MIT License. See [flask-marshmallow License](https://github.com/marshmallow-code/flask-marshmallow/blob/dev/LICENSE).

**Database Drivers & Utilities**
- [psycopg2](https://www.psycopg.org/) — The most popular PostgreSQL database adapter for Python. Licensed under the GNU Lesser General Public License (LGPL). See [psycopg2 License](https://github.com/psycopg/psycopg2/blob/master/LICENSE).
- [python-dotenv](https://github.com/theskimmingstone/python-dotenv) — Reads key-value pairs from a .env file and adds them to the environment. Licensed under the BSD 3-Clause License. See [python-dotenv License](https://github.com/theskimmingstone/python-dotenv/blob/master/LICENSE).

**Production Deployment**
- [Gunicorn](https://gunicorn.org/) — A Python WSGI HTTP Server for UNIX. Licensed under the MIT License. See [Gunicorn License](https://github.com/benoitc/gunicorn/blob/master/LICENSE).

**Development Dependencies**
- [Werkzeug](https://werkzeug.palletsprojects.com/) — A utility library for WSGI applications. Licensed under the BSD 3-Clause License. See [Werkzeug License](https://github.com/pallets/werkzeug/blob/main/LICENSE.rst).

### Fair Use & Attribution

All dependencies used in this project are open-source and are used in accordance with their respective licenses. The project does not modify, redistribute, or claim ownership of any of these tools. We encourage you to review the license of each dependency for detailed terms and conditions.

If you use this project or derivative works, please:
- Acknowledge the use of open-source components and their authors.
- Comply with the license terms of each dependency (particularly the LGPL requirement for psycopg2 if you distribute the application).
- Include a copy of relevant licenses with any distribution.

Sample seed data (character names, affiliations, occupations) used during development was created for demonstration purposes and is inspired by the Mobile Suit Gundam universe for illustrative use only.
