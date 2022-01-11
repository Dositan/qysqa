import click
from flask import Blueprint, redirect, render_template, request

from app import db

from .forms import ShortURLForm, URLForm
from .models import URL
from .token import gen_valid_token

bp = Blueprint("main", __name__)
bp.cli.short_help = "Make URL manipulations directly in the terminal"


@bp.route("/", methods=("GET", "POST"))
def index():
    """
    `/` endpoint

    Here a long URL is handled, returning a short URL as the result
    """
    form = URLForm()
    url = request.root_url

    if form.validate_on_submit():
        if form.token.data:
            db.session.add(URL(token=form.token.data, url=form.url.data))
            db.session.commit()

            result = f"{url}{form.token.data}"
            return render_template("main/url.html", result=result)

        # Token was not given
        else:
            token = gen_valid_token()
            db.session.add(URL(token=token, url=form.url.data))
            db.session.commit()

            result = f"{url}{token}"
            return render_template("main/url.html", result=result)
    else:
        return render_template("main/index.html", form=form)


@bp.route("/<token>")
def short_url(token):
    """
    `/<token>` endpoint

    Redirects to the original URL from a short one (using token)
    """
    query = URL.query.filter_by(token=token).first()

    # Query response returned None
    if not query:
        return (
            render_template(
                "main/error.html", error_code=404, error_message="Not Found"
            ),
            404,
        )
    else:
        query.clicks += 1
        db.session.commit()

        return redirect(query.url)


@bp.route("/about")
def about():
    """
    `/about` endpoint

    Displays static information about the project
    """
    return render_template("main/about.html")


@bp.route("/tracker", methods=("GET", "POST"))
def tracker():
    """
    `/tracker` endpoint

    Returns amount of clicks for the given short URL
    """
    form = ShortURLForm()

    if form.validate_on_submit():
        # Get the clicks of the given token
        token = form.url.data.split("/")[-1]
        clicks = URL.query.filter_by(token=token).first().clicks
        return render_template("main/clicks.html", clicks=clicks)
    else:
        return render_template("main/tracker.html", form=form)


@bp.route("/lookup", methods=("GET", "POST"))
def lookup():
    """
    `/lookup` endpoint

    Returns the original URL from a short one (using token)
    """
    form = ShortURLForm()

    if form.validate_on_submit():
        # Get the original url of the given token
        token = form.url.data.split("/")[-1]
        url = URL.query.filter_by(token=token).first().url
        return render_template("main/original-url.html", url=url)
    else:
        return render_template("main/lookup.html", form=form)


# Error handling routes
@bp.errorhandler(404)
def error_404(_):
    return (
        render_template("main/error.html", error_code=404, error_message="Not Found"),
        404,
    )


@bp.errorhandler(500)
def error_500(_):
    return (
        render_template(
            "main/error.html", error_code=500, error_message="Server Error"
        ),
        500,
    )


# Command-Line Interface
@bp.cli.command("shorten")
@click.argument("url")
def cmd_shorten(url: str):
    """Shorten URL"""
    token = gen_valid_token()
    db.session.add(URL(token=token, url=url))
    db.session.commit()

    result = f"localhost/{token}"
    click.secho(f"Here is your short URL: {result}", fg="green")


@bp.cli.command("tracker")
@click.argument("token")
def cmd_tracker(token: str):
    """Track URL"""
    clicks = URL.query.filter_by(token=token).first().clicks
    click.secho(f"URL has: {clicks} {'click' if clicks == 1 else 'clicks'}", fg="green")


@bp.cli.command("lookup")
@click.argument("token")
def cmd_lookup(token: str):
    """URL Lookup"""
    url = URL.query.filter_by(token=token).first().url
    click.secho(f"Original URL: {url}", fg="green")
