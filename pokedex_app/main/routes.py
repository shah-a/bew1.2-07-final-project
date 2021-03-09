from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from pokedex_app import db
from pokedex_app.models import Region
from pokedex_app.main.forms import RegionForm, TeamForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def homepage():
    regions = Region.query.all()
    return render_template('main/home.html', regions=regions)

@main.route('/new_region', methods=['GET', 'POST'])
def new_region():
    return "new region"

@main.route('/region/<region_name>', methods=['GET', 'POST'])
def region_details(region_name):
    return f"{region_name} details"

@main.route('/new_pokemon', methods=['GET', 'POST'])
def new_pokemon():
    return "new pokemon"

@main.route('/pokemon/<pokemon_name>', methods=['GET'])
def pokemon_details(pokemon_name):
    return f"{pokemon_name} details"

@main.route('/new_team', methods=['GET', 'POST'])
@login_required
def new_team():
    return "new team"

@main.route('/my_teams', methods=['GET'])
@login_required
def my_teams():
    return "my teams"

@main.route('/my_teams/<team_id>', methods=['GET'])
@login_required
def team_details(team_id):
    return (f"team id: {team_id}")
