from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)

    #we use this utility module to display forms quickly
    bootstrap = Bootstrap5(app)

    #A secret key for the session object
    app.secret_key = 'somerandomvalue'
    
    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)

    return app

@app.route('/')
def index():
    return render_template('index.html')