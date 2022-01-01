from flask import Blueprint, render_template, redirect

from qysqa import config, db
from qysqa.main.forms import ShortURLForm, URLForm
from qysqa.main.models import URL
from qysqa.main.token import gen_valid_token

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    form = URLForm()

    if form.validate_on_submit():
        if form.token.data:
            db.session.add(URL(token=form.token.data, url=form.url.data))
            db.session.commit()

            result = f"{config['url']}/{form.token.data}"
            return render_template("main/url.html", result=result)

        # Else if a token was not given
        else:
            token = gen_valid_token()
            db.session.add(URL(token=token, url=form.url.data))
            db.session.commit()

            # Return the url page with the shortened url
            result = f"{config['url']}/{token}"
            return render_template("main/url.html", result=result)
    else:
        return render_template("main/index.html", form=form, config=config)


# Shortened url route
@bp.route("/<token>")
def short_url(token):
    query = URL.query.filter_by(token=token).first()

    # If the query response was empty
    if not query:
        # Return the error page with a 404 not found error
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


@bp.route("/tracker", methods=["GET", "POST"])
def tracker():
    form = ShortURLForm()

    if form.validate_on_submit():
        # Get the clicks of the given token
        clicks = URL.query.filter_by(token=form.url.data).first().clicks

        return render_template("main/clicks.html", clicks=clicks)

    else:
        return render_template("main/tracker.html", form=form)


@bp.route("/lookup", methods=["GET", "POST"])
def lookup():
    # Create a instance of the form
    form = ShortURLForm()

    # If the form was valid
    if form.validate_on_submit():
        # Get the original url of the given token
        url = URL.query.filter_by(token=form.url.data).first().url

        # Return the original url page with the url
        return render_template("main/original-url.html", url=url)

    # Else if the form was invalid or not submitted
    else:
        return render_template("main/lookup.html", form=form)


# Removed url route
@bp.route("/removed")
def removed():
    return render_template("main/removed.html")


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
