from . import db
from datetime import datetime
from flask_login import UserMixin

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    venue_address = db.Column(db.String(200), nullable=False)
    venue_name = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    sport = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    comments = db.relationship('Comment', backref='event')
    standard_price = db.Column(db.Integer, nullable=False)
    premium_price = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Name: {self.name}"

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Booking', backref='user')
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    premium_count = db.Column(db.Integer)
    standard_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    booked_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(80), db.ForeignKey('events.name'))
    description = db.Column(db.String(200), db.ForeignKey('events.description'))
    total_price = db.Column(db.Integer)

    def __repr__(self):
        return f"Booking: {self.text}"
