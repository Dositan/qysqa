import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from app.config import config

__version__ = (1, 0, 0, "beta")

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[app.config["ENV"]])

    # initialize Flask-SQLAlchemy and the init-db commands
    db.init_app(app)
    app.cli.add_command(init_db)

    from . import main

    app.register_blueprint(main.bp)

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
