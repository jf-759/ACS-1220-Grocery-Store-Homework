from grocery_app.extensions import db
from grocery_app.utils import FormEnum
from flask_login import UserMixin



class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

shopping_list_table = db.Table(
    'shopping_list_items',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('grocery_item_id', db.Integer, db.ForeignKey('grocery_item.id'))
)

class User(db.Model, UserMixin):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    grocery_stores = db.relationship('GroceryStore', back_populates='created_by')
    grocery_items = db.relationship('GroceryItem', back_populates='created_by')

    shopping_list_items = db.relationship(
        'GroceryItem',
        secondary=shopping_list_table,
        backref='users'
    )


class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', back_populates='grocery_stores')


class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(db.String)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', back_populates='grocery_items')