"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask.cli import with_appcontext

from app.extensions import db
from app.main.models import URL
from app.main.token import gen_valid_token


@click.command("init-db")
@with_appcontext
def init_db():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.secho("Initialized the database.", fg="green")


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [arg for arg in root_files + root_directories]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = []
    black_args = []
    if check:
        isort_args.append("--check")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")


@click.command()
@click.argument("url")
def shorten(url: str):
    """Shorten your really long URL."""
    token = gen_valid_token()
    db.session.add(URL(token=token, url=url))
    db.session.commit()

    result = f"localhost/{token}"
    click.secho(f"Here is your short URL: {result}", fg="green")


@click.command()
@click.argument("token")
def tracker(token: str):
    """Get the amount of clicks on a certain URL."""
    clicks = URL.query.filter_by(token=token).first().clicks
    click.secho(f"URL has: {clicks} {'click' if clicks == 1 else 'clicks'}", fg="green")


@click.command()
@click.argument("token")
def lookup(token: str):
    """Get the original URL from a short one."""
    url = URL.query.filter_by(token=token).first().url
    click.secho(f"Original URL: {url}", fg="green")
