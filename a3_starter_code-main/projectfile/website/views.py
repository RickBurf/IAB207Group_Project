from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search', methods=['GET', 'POST'])
def search():
    # Your search logic here
    return render_template('index.html')