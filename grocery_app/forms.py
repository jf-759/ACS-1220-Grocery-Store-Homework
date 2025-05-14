from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError, NumberRange
from grocery_app.models import GroceryStore, User
from grocery_app import bcrypt

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField(
        "Store Title",
        validators=[DataRequired(), Length(max=100)]
    )
    address = StringField(
        "Store Address",
        validators=[DataRequired(), Length(max=200)]
    )
    submit = SubmitField("Submit")


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField(
        "Item Name",
        validators=[DataRequired(), Length(max=100)]
    )
    price = FloatField(
        "Price",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    category = SelectField(
        "Category",
        choices=[
            ('produce', 'Produce'),
            ('dairy', 'Dairy'),
            ('bakery', 'Bakery'),
            ('meat', 'Meat'),
            ('pantry', 'Pantry'),
            ('frozen', 'Frozen'),
            ('beverage', 'Beverage'),
            ('other', 'Other')
        ],
        validators=[DataRequired()]
    )
    photo_url = StringField(
        'Photo URL',
        validators=[URL(), Length(max=300)]
    )
    store = QuerySelectField(
        'Store',
        query_factory=lambda: GroceryStore.query.all(),
        get_label="title",
        allow_blank=False,
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

# forms.py

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')