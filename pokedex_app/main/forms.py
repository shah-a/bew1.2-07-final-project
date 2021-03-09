from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,  SubmitField
from wtforms.validators import DataRequired, Length, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from pokedex_app.models import Region

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
    region = QuerySelectField('Native Region', query_factory=lambda: Region.query)
    submit = SubmitField('Submit')

class TeamForm(FlaskForm):
    pass
