from flask import current_app, request
from wtforms import ValidationError

from app.database import db

from .models import URL


def validate_url(_, url):
    # Ensure url is not too short or long
    if len(url.data) < 4 or len(url.data) > 2000:
        return

    # If url contains spaces or does not have any dots
    if " " in url.data or "." not in url.data:
        raise ValidationError("Invalid URL")

    # If url starts with a dot
    if (
        url.data.lower().startswith("http://.")
        or url.data.lower().startswith("https://.")
        or url.data.startswith(".")
    ):
        raise ValidationError("Invalid URL")

    # If url starts with a slash
    if (
        url.data.lower().startswith("http:///")
        or url.data.lower().startswith("https:///")
        or url.data.startswith("/")
    ):
        raise ValidationError("Invalid URL")

    # If url ends with a dot and it is the only dot
    if url.data.endswith(".") and url.data.count(".") == 1:
        raise ValidationError("Invalid URL")

    # If url contains website domain
    if request.root_url in url.data.lower():
        raise ValidationError("Invalid URL")

    # If URL does not start with http(s)://
    if not (url.data.lower().startswith("http://")) and not (
        url.data.lower().startswith("https://")
    ):
        url.data = "http://" + url.data


def validate_token(_, token):
    # Make sure the token is not too short or long
    if len(token.data) < 6 or len(token.data) > 16:
        return

    # Check if custom token does not conflict with app endpoints
    for route_name in current_app.url_map.iter_rules():
        if token.data == str(route_name).split("/")[1]:
            raise ValidationError("Token name is reserved by website endpoints.")

    for char in token.data:
        # If it is not a valid character
        if not (char.isalpha()) and not (char.isdigit()) and char not in ("_", "-"):
            raise ValidationError("Token contains invalid characters")

    if db.session.query(
        db.session.query(URL).filter_by(token=token.data).exists()
    ).scalar():
        raise ValidationError("Token already exists")


def validate_short_url(_, short_url):
    APP_URL = request.root_url

    # Ensure short url is not too short or long
    if (
        len(short_url.data) < len(APP_URL) + 7
        or len(short_url.data) > len(APP_URL) + 25
    ):
        return

    # If the start of short url is not valid
    if (
        not (short_url.data.lower().startswith(APP_URL + "/"))
        and not (short_url.data.lower().startswith("http://" + APP_URL + "/"))
        and not (short_url.data.lower().startswith("https://" + APP_URL + "/"))
    ):
        raise ValidationError("Invalid short URL")

    # Get the token of the short url
    if short_url.data.lower().startswith(APP_URL + "/"):
        token = short_url.data[len(APP_URL) + 1 :]

    elif short_url.data.lower().startswith("http://" + APP_URL + "/"):
        token = short_url.data[len(APP_URL) + 8 :]

    elif short_url.data.lower().startswith("https://" + APP_URL + "/"):
        token = short_url.data[len(APP_URL) + 9 :]

    if not db.session.query(
        db.session.query(URL).filter_by(token=token).exists()
    ).scalar():
        raise ValidationError("This short URL does not exist.")

    # After all the validation is done set the forms url value as the token
    short_url.data = token
