from flask_wtf import Form  
from wtforms import validators, ValidationError  
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField

class BaseSignUpForm(Form):
    first_name = TextField("First Name ",[validators.Required("Please enter your first name.")])
    middle_name = TextField("Middle Name ")
    last_name = TextField("Last Name ",[validators.Required("Please enter your last name.")])
    email = TextField("Email", [validators.Required("Please enter your email address.")])
    password = PasswordField("Password", [validators.Required("Please enter a password."), validators.Length(min=8, message="Password is too short")])
    confirm = PasswordField(validators=[validators.EqualTo('password', 'Incorrect password entered.')])
    
    
class ResearcherSignUpForm(Form):
