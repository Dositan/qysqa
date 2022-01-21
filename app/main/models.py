from app.database import Column, PkModel, db, reference_col, relationship


class URL(PkModel):
    """Short URLs that a user creates."""

    __tablename__ = "urls"
    token = Column(db.String(16), index=True, unique=True, nullable=False)
    url = Column(db.String(2000), nullable=False)
    clicks = Column(db.Integer, nullable=False, default=0)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="urls")

    def __repr__(self):
        return f"URL(id='{self.id}' token='{self.token}' clicks='{self.clicks}'"

    def __str__(self) -> str:
        return self.url
