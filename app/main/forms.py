from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from .validators import validate_short_url, validate_token, validate_url


class URLForm(FlaskForm):
    """The regular URL form used in the `index` route."""

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
    """Form for short URLs."""

    url = StringField(
        validators=[
            DataRequired(),
            validate_short_url,
        ]
    )
    submit = SubmitField("Submit")
