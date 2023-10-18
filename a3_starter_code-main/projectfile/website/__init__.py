from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
    
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretgoeshere'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydbname.sqlite'
    db.init_app(app)

    
    #initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))
    #add Blueprints
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.authbp)

    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)

    #this creates a dictionary of variables that are available
    #to all html templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    return app