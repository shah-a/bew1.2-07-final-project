from pokedex_app import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    teams = db.relationship('Team', back_populates='user')

    def __str__(self):
        return f'<User: {self.username}>'

    def __repr__(self):
        return f'<User: {self.username}>'

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType, nullable=False)
    description = db.Column(db.Text, nullable=False)

    pokemon = db.relationship('Pokemon', back_populates='region')

    def __str__(self):
        return f'<Region: {self.name}>'

    def __repr__(self):
        return f'<Region: {self.name}>'

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType, nullable=False)
    description = db.Column(db.Text, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', back_populates='pokemon')

    teams = db.relationship(
        'Team', secondary='pokemon_teams', back_populates='pokemon'
    )

    def __str__(self):
        return f'<Pokemon: {self.name}>'

    def __repr__(self):
        return f'<Pokemon: {self.name}>'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='teams')

    pokemon = db.relationship(
        'Pokemon', secondary='pokemon_teams', back_populates='teams'
    )

    def __str__(self):
        return f'<Team: {self.name}>'

    def __repr__(self):
        return f'<Team: {self.name}>'

pokemon_teams_table = db.Table('pokemon_teams',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)
