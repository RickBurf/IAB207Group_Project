from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import FilterForm
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event).order_by(Event.start_date)).all()    
    return render_template('index.html', events=events)

@mainbp.route('/filter')
def filter():
    form = FilterForm();
    if form.validate_on_submit():
        choice = form.data
        events = db.session.scalars(db.select(Event).where(Event.sport == choice)).all()    
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))



@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query) | Event.name.like(query) | Event.sport.like(query)).order_by(Event.start_date)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
