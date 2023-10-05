from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretgoeshere'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydbname.sqlite'
    db.init_app(app)
    bootstrap = Bootstrap(app)
    
    # Import your views module here to avoid circular references
    from . import views
    app.register_blueprint(views.bp)

    return app