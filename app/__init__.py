import logging
import sys

from flask import Flask, render_template

from app import auth, commands, main
from app.config import config
from app.extensions import bcrypt, csrf_protect, db, login_manager


def create_app():
    """Qysqa application factory."""
    app = Flask(__name__)
    app.config.from_object(config[app.config["ENV"]])
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    return None


def register_blueprints(app):
    """Register app blueprints."""
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    messages = {
        404: "Not Found",
        500: "Server Error",
    }

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("error.html", error, messages[error]), error_code

    for errcode in (404, 500):
        app.errorhandler(errcode)(render_error)
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure logger."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
