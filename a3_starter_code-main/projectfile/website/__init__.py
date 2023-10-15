from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretgoeshere'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydbname.sqlite'
    db.init_app(app)
    bootstrap = Bootstrap(app)

    #initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))

    # Import and register your views module here
    from . import views
    app.register_blueprint(views.bp)

    # Import and register the auth blueprint here
    from . import auth
    app.register_blueprint(auth.authbp)

    return app
