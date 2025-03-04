from App.models import User
from flask_login import UserMixin

class Student(UserMixin, User):

    __mapper_args__ = {
        'polymorphic_identity':'Student',
        'exclude_properties': []
    }

    def __init__(self):
        super(Student, self).__init__()
    
    # def __init__(self, email, password, first_name, middle_name, last_name, institution, faculty, department, image_url):
    #     super(Student, self).__init__(email, password, first_name, middle_name, last_name, institution, faculty, department, image_url)

    def toDict(self):
        return super().toDict()
