from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, TimeField, DateField, PasswordField, SelectField, FloatField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}
SPORTS = {'AFL', 'Rugby League', 'Tennis'}


class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    Venue_Address = TextAreaField('Venue Address', validators=[InputRequired()])
    Venue_Name = TextAreaField('Venue Name', validators=[InputRequired()])
    Start_Date = DateField('Start Date', validators=[InputRequired()], format='%Y-%m-%d')
    End_Date = DateField('End Date', validators=[InputRequired()], format='%Y-%m-%d')
    Start_Time = TimeField('Start Time', validators=[InputRequired()])
    End_Time = TimeField('End Time', validators=[InputRequired()])
    Sport = SelectField('Sport', choices=SPORTS, validators=[InputRequired()])
    Status = TextAreaField('Status', validators=[InputRequired()])
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
    user_name = StringField("User Name", validators=[InputRequired()])
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