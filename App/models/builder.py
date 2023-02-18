from .student import Student
from .researcher import Researcher
from App.controllers.user import build_user

class StudentBuilder():

    def __init__(self):
        self.student = Student()

    def email(self, email):
        self.student.email = email
        return self

    def password(self, password):
        self.student.set_password(password)
        return self

    def first_name(self, first_name):
        self.student.first_name = first_name
        return self

    def middle_name(self, middle_name):
        self.student.middle_name = middle_name
        return self

    def last_name(self, last_name):
        self.student.last_name = last_name
        return self

    def image_url(self, image_url):
        self.student.image_url = image_url
        return self

    def institution(self, institution):
        self.student.institution = institution
        return self

    def faculty(self, faculty):
        self.student.faculty = faculty
        return self

    def department(self, department):
        self.student.department = department
        return self

    def build(self):
        return build_user(self.student)


class ResearcherBuilder():

    def __init__(self):
        self.researcher = Researcher()

    def email(self, email):
        self.researcher.email = email
        return self

    def password(self, password):
        self.researcher.set_password(password)
        return self

    def first_name(self, first_name):
        self.researcher.first_name = first_name
        return self

    def middle_name(self, middle_name):
        self.researcher.middle_name = middle_name
        return self

    def last_name(self, last_name):
        self.researcher.last_name = last_name
        return self

    def image_url(self, image_url):
        self.researcher.image_url = image_url
        return self

    def institution(self, institution):
        self.researcher.institution = institution
        return self

    def faculty(self, faculty):
        self.researcher.faculty = faculty
        return self

    def department(self, department):
        self.researcher.department = department
        return self

    def title(self, title):
        self.researcher.title = title
        return self

    def position(self, position):
        self.researcher.position = position
        return self
    
    def start_year(self, start_year):
        self.researcher.start_year = start_year
        return self

    def qualifications(self, qualifications):
        self.researcher.qualifications = qualifications
        return self

    def certifications(self, certifications):
        self.researcher.certifications = certifications
        return self

    def skills(self, skills):
        self.researcher.skills = skills
        return self

    def website_url(self, website_url):
        self.researcher.website_url = website_url
        return self

    def introduction(self, introduction):
        self.researcher.introduction = introduction
        return self

    def build(self):
        return build_user(self.researcher)