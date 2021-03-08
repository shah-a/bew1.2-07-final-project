from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pokedex_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

# TODO: Add authentication setup code here!



###########################
# Blueprints
###########################

from pokedex_app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from pokedex_app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()
