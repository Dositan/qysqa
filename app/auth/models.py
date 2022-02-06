from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Column, PkModel, db
from app.extensions import bcrypt


class User(UserMixin, PkModel):
    """App user model."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
