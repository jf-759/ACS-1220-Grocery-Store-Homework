from grocery_app import app
from grocery_app.extensions import db
from grocery_app.models import User, GroceryStore, GroceryItem

@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'GroceryStore': GroceryStore,
        'GroceryItem': GroceryItem,
    }