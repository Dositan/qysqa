from flask import request
from wtforms import ValidationError

from app import db

from .models import URL


def validate_url(_, field):
    # Ensure url is not too short or long
    if len(field.data) < 4 or len(field.data) > 2000:
        return

    # If url contains spaces or does not have any dots
    if " " in field.data or not "." in field.data:
        raise ValidationError("Invalid URL")

    # If url starts with a dot
    if (
        field.data.lower().startswith("http://.")
        or field.data.lower().startswith("https://.")
        or field.data.startswith(".")
    ):
        raise ValidationError("Invalid URL")

    # If url starts with a slash
    if (
        field.data.lower().startswith("http:///")
        or field.data.lower().startswith("https:///")
        or field.data.startswith("/")
    ):
        raise ValidationError("Invalid URL")

    # If url ends with a dot and it is the only dot
    if field.data.endswith(".") and field.data.count(".") == 1:
        raise ValidationError("Invalid URL")

    # If url contains website domain
    if request.root_url in field.data.lower():
        raise ValidationError("Invalid URL")

    # If URL does not start with http(s)://
    if not (field.data.lower().startswith("http://")) and not (
        field.data.lower().startswith("https://")
    ):
        field.data = "http://" + field.data


def validate_token(_, field):
    # Make sure the token is not too short or long
    if len(field.data) < 6 or len(field.data) > 16:
        return

    if field.data in ("about", "tracker", "lookup"):
        raise ValidationError("Token name is reserved by website endpoints.")

    for char in field.data:
        # If it is not a valid character
        if not (char.isalpha()) and not (char.isdigit()) and char not in ("_", "-"):
            raise ValidationError("Token contains invalid characters")

    if db.session.query(
        db.session.query(URL).filter_by(token=field.data).exists()
    ).scalar():
        raise ValidationError("Token already exists")


def validate_short_url(_, field):
    APP_URL = request.root_url

    # Ensure short url is not too short or long
    if len(field.data) < len(APP_URL) + 7 or len(field.data) > len(APP_URL) + 25:
        return

    # If the start of short url is not valid
    if (
        not (field.data.lower().startswith(APP_URL + "/"))
        and not (field.data.lower().startswith("http://" + APP_URL + "/"))
        and not (field.data.lower().startswith("https://" + APP_URL + "/"))
    ):
        raise ValidationError("Invalid short URL")

    # Get the token of the short url
    if field.data.lower().startswith(APP_URL + "/"):
        token = field.data[len(APP_URL) + 1 :]

    elif field.data.lower().startswith("http://" + APP_URL + "/"):
        token = field.data[len(APP_URL) + 8 :]

    elif field.data.lower().startswith("https://" + APP_URL + "/"):
        token = field.data[len(APP_URL) + 9 :]

    if not db.session.query(
        db.session.query(URL).filter_by(token=token).exists()
    ).scalar():
        raise ValidationError("This short URL does not exist.")

    # After all the validation is done set the forms url value as the token
    field.data = token
