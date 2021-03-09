from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pokedex_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

###########################
# Authentication
###########################

from pokedex_app.models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

###########################
# Blueprints
###########################

# MUST not be named 'auth' and 'main' to avoid module naming conflict with unit tests
from pokedex_app.auth.routes import auth as auth_routes
from pokedex_app.main.routes import main as main_routes

app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)

with app.app_context():
    db.create_all()
