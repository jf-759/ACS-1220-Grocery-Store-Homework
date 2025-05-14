from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.config import Config
from grocery_app.extensions import db, migrate

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

bcrypt = Bcrypt(app)

# Import blueprints after creating app
from grocery_app.routes import main, auth
app.register_blueprint(main)
app.register_blueprint(auth)

@login_manager.user_loader
def load_user(user_id):
    from grocery_app.models import User
    return User.query.get(int(user_id))