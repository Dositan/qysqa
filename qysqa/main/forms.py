from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional

from qysqa import db
from qysqa.main.models import URL


def validate_url(_, field):
    # Make sure url is not too short or long
    if len(field.data) < 4 or len(field.data) > 2000:
        return

    # If url contains spaces or does not have any dots
    if " " in field.data or not "." in field.data:
        raise ValidationError("Invalid URL")

    # If the url starts with a dot after http:// or after https:// or just starts with a dot
    if (
        field.data.lower().startswith("http://.")
        or field.data.lower().startswith("https://.")
        or field.data.startswith(".")
    ):
        raise ValidationError("Invalid URL")

    # If the url starts with a slash after http:// or after https:// or just starts with a slash
    if (
        field.data.lower().startswith("http:///")
        or field.data.lower().startswith("https:///")
        or field.data.startswith("/")
    ):
        raise ValidationError("Invalid URL")

    # If the url ends with a dot and it is the only dot
    if field.data.endswith(".") and field.data.count(".") == 1:
        raise ValidationError("Invalid URL")

    # If the url contains the website domain
    if request.root_url in field.data.lower():
        raise ValidationError("Invalid URL")

    # If the URL does not start with http:// and https://
    if not (field.data.lower().startswith("http://")) and not (
        field.data.lower().startswith("https://")
    ):
        field.data = "http://" + field.data


def validate_token(_, field):
    # Make sure the token is not too short or long
    if len(field.data) < 6 or len(field.data) > 16:
        return

    if field.data in ("tracker", "lookup", "removed"):
        raise ValidationError("Token name is reserved by website endpoints.")

    for char in field.data:
        # If it is not a valid character
        if (
            not (char.isalpha())
            and not (char.isdigit())
            and char != "_"
            and char != "-"
        ):
            raise ValidationError("Token contains invalid characters")

    if db.session.query(
        db.session.query(URL).filter_by(token=field.data).exists()
    ).scalar():
        raise ValidationError("Token already exists")


def validate_short_url(_, field):
    APP_URL = request.root_url

    # Make sure the short url is not too short or long
    if len(field.data) < len(APP_URL) + 7 or len(field.data) > len(APP_URL) + 25:
        return

    # If the start of the short url is not valid
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


class URLForm(FlaskForm):
    url = StringField(
        validators=[
            DataRequired(),
            Length(min=4, max=2000, message="Invalid URL length"),
            validate_url,
        ]
    )
    token = StringField(
        validators=[
            Optional(),
            Length(min=6, max=16, message="Invalid token length"),
            validate_token,
        ]
    )
    submit = SubmitField("Shorten")


class ShortURLForm(FlaskForm):
    url = StringField(
        validators=[
            DataRequired(),
            validate_short_url,
        ]
    )
    submit = SubmitField("Submit")
