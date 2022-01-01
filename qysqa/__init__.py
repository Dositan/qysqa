import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from qysqa.config import get_config

__version__ = (0, 1, 0, "dev")

db = SQLAlchemy()
config = get_config()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    if (db_url := config.get("db_url")) is None:
        db_path = os.path.join(app.instance_path, "db.sqlite3")
        db_url = f"sqlite:///{db_path}"
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=config["secret_key"],
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # initialize Flask-SQLAlchemy and the init-db commands
    db.init_app(app)
    app.cli.add_command(init_db)

    # make "index" point at "/"
    app.add_url_rule("/", endpoint="index")

    return app


@click.command("init-db")
@with_appcontext
def init_db():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.secho("Initialized the database.", fg="green")
