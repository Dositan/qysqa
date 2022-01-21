"""Extensions module. Each extension is initialized in the app factory."""
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
bcrypt = Bcrypt()
