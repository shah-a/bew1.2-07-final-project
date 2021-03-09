from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from pokedex_app import db
from pokedex_app.models import Region, Pokemon, Team
from pokedex_app.main.forms import PokemonForm, RegionForm, TeamForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def homepage():
    regions = Region.query.all()
    return render_template('main/home.html', regions=regions)

@main.route('/new_region', methods=['GET', 'POST'])
def new_region():
    form = RegionForm()

    if form.validate_on_submit():
        new_region = Region(
            name=form.name.data,
            photo_url=form.photo_url.data,
            description=form.description.data
        )
        db.session.add(new_region)
        db.session.commit()

        flash("New region was successfully added.")
        return redirect(url_for('main.region_details', region_name=new_region.name))

    return render_template('main/new_region.html', form=form)

@main.route('/region/<region_name>', methods=['GET', 'POST'])
def region_details(region_name):
    region = Region.query.filter_by(name=region_name).first()
    form = RegionForm(obj=region)

    if form.validate_on_submit():
        form.populate_obj(region)
        db.session.commit()

        flash("Region was successfully updated.")
        return redirect(url_for('main.region_details', region_name=region.name))

    return render_template('main/region_details.html', region=region, form=form)

@main.route('/new_pokemon', methods=['GET', 'POST'])
def new_pokemon():
    form = PokemonForm()

    if form.validate_on_submit():
        new_pokemon = Pokemon(
            name=form.name.data,
            photo_url=form.photo_url.data,
            description=form.description.data,
            region=form.region.data
        )

        flash("New pokemon successfully added.")
        return redirect(url_for('main.pokemon_details', pokemon_name=new_pokemon.name))

    return render_template('main/new_pokemon.html', form=form)

@main.route('/pokemon/<pokemon_name>', methods=['GET'])
def pokemon_details(pokemon_name):
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    form = PokemonForm(obj=pokemon)

    if form.validate_on_submit():
        form.populate_obj(pokemon)
        db.session.commit()

        flash("Pokemon was successfully updated.")
        return redirect(url_for('main.pokemon_details', pokemon_name=pokemon.name))

    return render_template('main/pokemon_details.html', pokemon=pokemon, form=form)

@main.route('/new_team', methods=['GET', 'POST'])
@login_required
def new_team():
    form = TeamForm()

    if form.validate_on_submit():
        new_team = Team(
            name=form.name.data,
            pokemon=form.pokemon.data,
            user=current_user
        )
        db.session.add(new_team)
        db.session.commit()

        flash("Team was successfully added.")
        return redirect(url_for('main.my_teams'))

    return render_template('main/new_team.html')

@main.route('/my_teams', methods=['GET'])
@login_required
def my_teams():
    teams = Team.query.filter_by(user_id=current_user.id).all()
    return render_template('main/my_teams.html', teams=teams)

@main.route('/my_teams/<team_id>', methods=['GET'])
@login_required
def team_details(team_id):
    team = Team.query.get(team_id)
    return render_template('main/team_details.html', team=team)
