from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, TimeField, DateField, PasswordField, SelectField, FloatField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from .models import Event

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}
SPORTS = {'AFL','Basketball', 'Soccer', 'Rugby League', 'Tennis', 'Volleyball', 'Cricket', 'Badminton', 'Ice Hockey', 'Boxing', 'Baseball'}


class EventForm(FlaskForm):
    name = StringField('Event Name')
    description = TextAreaField('Description')
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    Venue_Address = TextAreaField('Venue Address', validators=[InputRequired('Enter venue address')])
    Venue_Name = TextAreaField('Venue Name', validators=[InputRequired('Enter venue name')])
    Start_Date = DateField('Start Date', format='%Y-%m-%d')
    Start_Time = TimeField('Start Time')
    Duration = FloatField('Duration (Hours)', validators=[InputRequired(), NumberRange(min=0, message="Duration must be a positive number")])
    Sport = SelectField('Sport', choices=SPORTS)
    #Status = TextAreaField('Status')
    Number_Tickets = FloatField('Tickets Available', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    Standard_price = FloatField('Standard Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    Premium_price = FloatField('Premium Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    submit = SubmitField("Create")

#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name")
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
  
class BookingForm(FlaskForm):
  Standard_Count = FloatField('Number of Standard Tickets', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive whole number")], default=0)
  Premium_Count = FloatField('Number of Premium Tickets', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive whole number")], default=0)
  submit = SubmitField('Order')

class FilterForm(FlaskForm):
   choice = SelectField('Filter', choices = SPORTS)

class UpdateForm(FlaskForm):
    name = StringField('Change Event Name')
    description = TextAreaField('Change Description')
    image = FileField('Change Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    Venue_Address = TextAreaField('Change Venue Address')
    Venue_Name = TextAreaField('Change Venue Name')
    Start_Date = DateField('Change Start Date', format='%Y-%m-%d')
    
    Start_Time = TimeField('Change Start Time')
    Duration = FloatField('Change Duration (Hours)', validators=[InputRequired(), NumberRange(min=0, message="Duration must be a positive number")])
    Sport = SelectField('Change Sport', choices=SPORTS)
    #Status = TextAreaField('Status')
    Number_Tickets = FloatField('Add Extra Tickets', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    Standard_price = FloatField('Change Standard Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    Premium_price = FloatField('Change Premium Price', validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    submit = SubmitField("Update Event Details")
