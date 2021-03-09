from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,  SubmitField
from wtforms.validators import DataRequired, Length, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from pokedex_app.models import Region, Pokemon

class RegionForm(FlaskForm):
    """Form for adding a region."""
    name = StringField('Region Name', validators=[DataRequired(), Length(max=80)])
    photo_url = StringField('Photo URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PokemonForm(FlaskForm):
    """Form for adding a pokemon."""
    name = StringField('Pokemon Name', validators=[DataRequired(), Length(max=80)])
    photo_url = StringField('Photo URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[DataRequired()])
    region = QuerySelectField(
        'Native Region',
        validators=[DataRequired()],
        query_factory=lambda: Region.query
    )
    submit = SubmitField('Submit')

class TeamForm(FlaskForm):
    """Form for adding a team."""
    name = StringField('Team Name', validators=[DataRequired(), Length(max=80)])
    pokemon = QuerySelectMultipleField(
        'Pokemon',
        validators=[DataRequired()],
        query_factory=lambda: Pokemon.query
    )
    submit = SubmitField('Submit')
