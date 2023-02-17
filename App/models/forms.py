from flask_wtf import FlaskForm  
from flask_wtf.file import FileField
from wtforms import validators, ValidationError  
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField
from wtforms.fields import DateField

class BaseSignUpForm(FlaskForm):
    first_name = StringField("First Name ", validators=[validators.DataRequired("Please enter your first name")])
    middle_name = StringField("Middle Name ")
    last_name = StringField("Last Name ", validators=[validators.DataRequired("Please enter your last name")])
    email = StringField("Email", validators=[validators.DataRequired("Please enter your email address")])
    password = PasswordField("Password", validators=[validators.DataRequired("Please enter a password"), validators.Length(min=8, message="Password is too short")])
    confirm = PasswordField(validators=[validators.EqualTo('password', 'Incorrect password entered')])
    image = FileField("Image(Headshot)")
    institution = SelectField("Institution", choices=['The University of The West Indies'], validators=[validators.DataRequired("Please select an institution")])
    faculty = SelectField("Faculty", validators=[validators.DataRequired("Please select a faculty")])
    department = SelectField("Department", validators=[validators.DataRequired("Please select a department")])

class ResearcherSignUpForm(FlaskForm):
    title = RadioField("Title", choices=['Mr.', 'Ms.', 'Mrs.', 'Prof.', 'Dr.'], validators=[validators.DataRequired("Please select a title")])
    position = SelectField("Position", choices=['Tutor', 'Part-Time Lecturer', 'Full-Time Lecturer', 'Instructor', 'Teaching Assistant', 
                                                'Research Assistant', 'Associate Professor', 'Professor', 'Head of Department'],
                            validators=[validators.DataRequired("Please select a position")])
    start_date = SelectField("Year of Commencement of Employment at UWI", validators=[validators.DataRequired("Please select a year")])
    qualifications = TextAreaField("Qualifications", validators=[validators.DataRequired("Please enter your qualifications")])
    certifications = TextAreaField("Certifications")
    interests = SelectField("Research Interests", validators=[validators.DataRequired("Please enter your interest(s)")])
    skills = TextAreaField("Skills", validators=[validators.DataRequired("Please enter your skills")])
    website = StringField("Website URL")
    introduction = TextAreaField("Introduction")