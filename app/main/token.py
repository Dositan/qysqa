import secrets

from app.database import db

from .models import URL

TOKEN_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_-"


def generate_token():
    """A way to generate random, unique 6-digit tokens.
    
    Has a DB check whether the generated token already exists.
    """
    while True:
        token = "".join(secrets.choice(TOKEN_CHARS) for _ in range(6))

        # If token does not exist in the database
        if not db.session.query(
            db.session.query(URL).filter_by(token=token).exists()
        ).scalar():
            break

    return token
