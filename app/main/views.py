from flask import Blueprint, redirect, render_template, request
from flask_login import current_user

from app.database import db

from .forms import ShortURLForm, URLForm
from .models import URL
from .token import generate_token

bp = Blueprint("main", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    """
    `/` endpoint

    Here a long URL is handled, returning a short URL as the result
    """
    form = URLForm()
    url = request.root_url

    if form.validate_on_submit():
        user_id = None if current_user.is_anonymous else current_user.id
        if form.token.data:  # custom token given
            URL.create(token=form.token.data, url=form.url.data, user_id=user_id)
            result = f"{url}{form.token.data}"
            return render_template("main/url.html", result=result)
        else:
            token = generate_token()
            URL.create(token=token, url=form.url.data, user_id=user_id)
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
            render_template("error.html", error_code=404, error_message="Not Found"),
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
        return render_template("main/original.html", url=url)
    else:
        return render_template("main/lookup.html", form=form)
