from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    choices = [('Departure location', 'Departure location'),
               ('Arrival location', 'Arrival location')]
    select = SelectField('I want a precise:', choices=choices)
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search!')