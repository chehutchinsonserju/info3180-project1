from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class AddPropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    rooms = IntegerField('Number of Rooms', validators=[InputRequired(), NumberRange(min=1)])
    bathrooms = IntegerField('Number of Bathrooms', validators=[InputRequired(), NumberRange(min=1)])
    price = IntegerField('Price', validators=[InputRequired(), NumberRange(min=0)])
    property_type = SelectField('Property Type', choices=[('house', 'House'), ('apartment', 'Apartment'), ('mansion', 'Mansion'), ('dorm', 'Dorm')], validators=[InputRequired()])
    location = StringField('Location', validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired()])
