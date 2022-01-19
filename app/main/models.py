from app.extensions import db


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), index=True, unique=True, nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"URL(id='{self.id}' token='{self.token}' clicks='{self.clicks}'"

    def __str__(self) -> str:
        return self.url
