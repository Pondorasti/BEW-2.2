from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager, login_manager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Auth
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from .models import User  # nopep8


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


bcrypt = Bcrypt(app)


from .routes import main, auth  # nopep8

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()
