from flask_wtf import FlaskForm  
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField, RadioField, SelectField, PasswordField

class BaseSignUpForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(message="Please enter your first name")])
    middle_name = StringField("Middle Name(s)")
    last_name = StringField("Last Name", validators=[DataRequired(message="Please enter your last name")])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address")])
    password = PasswordField("Password", validators=[DataRequired("Please enter a password"), Length(min=8)])
    institution = SelectField("Institution", validators=[DataRequired("Please select an institution")])
    faculty = SelectField("Faculty", validators=[DataRequired("Please select a faculty")])
    department = SelectField("Department", validators=[DataRequired("Please select a department")])

class ResearcherSignUpForm(FlaskForm):
    title = RadioField("Title", choices=['Mr.', 'Ms.', 'Mrs.', 'Prof.', 'Dr.'], validators=[DataRequired("Please select a title")])
    position = SelectField("Position", choices=['Tutor', 'Part-Time Lecturer', 'Full-Time Lecturer', 'Instructor', 'Teaching Assistant', 
                                                'Research Assistant', 'Associate Professor', 'Professor', 'Head of Department'],
                            validators=[DataRequired("Please select a position")])
    start_date = SelectField("Year of Commencement of Employment at UWI", validators=[DataRequired("Please select a year")])
    qualifications = TextAreaField("Qualifications", validators=[DataRequired("Please enter your qualifications")])
    certifications = TextAreaField("Certifications")
    skills = TextAreaField("Skills", validators=[DataRequired("Please enter your skills")])
    website = StringField("Website URL")
    introduction = TextAreaField("Personal Introduction")
