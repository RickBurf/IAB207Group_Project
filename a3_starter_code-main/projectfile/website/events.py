from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User, Booking
from .forms import EventForm, CommentForm, BookingForm, UpdateForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user
from datetime import datetime

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    comment_form = CommentForm()    
    booking_form = BookingForm()
    events = [event]  # creating a list with the single 'event'
    return render_template('events/eventpage.html', events=events, comment_form=comment_form, booking_form=booking_form)

@eventbp.route('/<id>/update', methods=['GET', 'POST'])
def update(id):
    print('Method type: ', request.method)
    event = Event.query.get(id)
    form = UpdateForm()   
    if form.validate_on_submit():
        event.name=form.name.data
        event.description=form.description.data
        db_file_path = check_upload_file(form)
        event.image=db_file_path
        event.venue_address=form.Venue_Address.data
        event.venue_name=form.Venue_Name.data
        event.start_date=form.Start_Date.data
        event.end_date=form.End_Date.data
        event.start_time=form.Start_Time.data
        event.end_time=form.End_Time.data
        event.sport=form.Sport.data
        event.premium_price = form.Premium_price.data
        event.standard_price = form.Standard_price.data
        event.number_tickets += form.Number_Tickets.data
        event.user_id = current_user.id
        db.session.commit()
        flash('Successfully updated event', 'success')
        return redirect(url_for('event.show', id=id))
    return render_template('events/update.html', form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(
            name=form.name.data,
            description=form.description.data,
            image=db_file_path,
            venue_address=form.Venue_Address.data,
            venue_name=form.Venue_Name.data,
            start_date=form.Start_Date.data,
            end_date=form.End_Date.data,
            start_time=form.Start_Time.data,
            end_time=form.End_Time.data,
            sport=form.Sport.data,
            #status=form.Status.data,
            premium_price = form.Premium_price.data,
            standard_price = form.Standard_price.data,
            number_tickets = form.Number_Tickets.data,
            user_id = current_user.id
        )
        if form.Start_Date.data < datetime.now().date():
            event.status = "INACTIVE"
        elif form.Start_Date.data == datetime.now().date():
            if form.Start_Time.data < datetime.now().time():
                event.status = "INACTIVE"
        else: event.status = "OPEN"

        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Successfully created a new event', 'success')
        # Always end with redirect when the form is valid
        return redirect(url_for('event.create'))
    return render_template('events/create.html', form=form)


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_dir = os.path.join(BASE_PATH, 'static', 'image')
    os.makedirs(upload_dir, exist_ok=True)  # create the upload directory if it doesn't exist
    upload_path = os.path.join(upload_dir, secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

@eventbp.route('/<id>/booking', methods=['GET', 'POST'])  
@login_required
def booking(id):  
    form = BookingForm()  
    #get the destination object associated to the page and the comment
    event = Event.query.get(id)  # Retrieve the Event object using its ID
    user = User.query.get(current_user.id)  # Retrieve the User object using its ID

    if form.validate_on_submit():  
        # Read the comment from the form and create a new Comment object
        new_booking = Booking(
            premium_count=form.Premium_Count.data,
            standard_count=form.Standard_Count.data,
            event_id=event.id,
            user=user,
            #name = event.name,
            #description = event.description,
            created_at=datetime.now(),
            total_price=form.Premium_Count.data * event.premium_price + form.Standard_Count.data * event.standard_price
        )
        event.number_tickets -= (form.Premium_Count.data + form.Standard_Count.data)
        if event.number_tickets <= 0:
            event.status = "SOLD OUT"
        # Add the new comment to the database session and commit the changes
        db.session.add(new_booking) 
        db.session.commit() 
        # Flash a success message
        flash('Your Booking has been added', 'success')  
        # Redirect to the event page with the specified ID
        return redirect(url_for('event.show', id=id))

    # If the form doesn't validate or it's a GET request, render the template with the form
    return render_template('events/eventpage.html', form=form, events=[event])

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = Event.query.get(id)  # Retrieve the Event object using its ID
    user = User.query.get(current_user.id) # Retrieve the User object using its ID

    if form.validate_on_submit():  
        # Read the comment from the form and create a new Comment object
        new_comment = Comment(
            text=form.text.data,
            event_id=event.id,
            user=user,
            created_at=datetime.now()
        )
        # Add the new comment to the database session and commit the changes
        db.session.add(new_comment) 
        db.session.commit() 
        # Flash a success message
        flash('Your comment has been added', 'success')  
        # Redirect to the event page with the specified ID
        return redirect(url_for('event.show', id=id))

    # If the form doesn't validate or it's a GET request, render the template with the form
    return render_template('events/eventpage.html', form=form, events=[event])

@eventbp.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    print('Method type: ', request.method)
    # Retrieve bookings from the database
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    #bookings = db.session.query(Booking, Event).filter(Booking.user_id == current_user.id).filter(Event.id==Booking.event_id).all()
    # Pass the bookings to the template for rendering
    return render_template('events/history.html', bookings=bookings)

@eventbp.route('/myEvents', methods=['GET', 'POST'])
@login_required
def myEvents():
    print('Method type: ', request.method)
    # Retrieve bookings from the database
    events = db.session.scalars(db.select(Event).where(Event.user_id==current_user.id)).all()
    # Pass the bookings to the template for rendering
    return render_template('events/myEvents.html', events=events)

