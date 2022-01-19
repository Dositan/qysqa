"""Extensions module. Each extension is initialized in the app factory."""
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf_protect = CSRFProtect()
