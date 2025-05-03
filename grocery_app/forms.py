from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, NumberRange
from models import GroceryStore

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
