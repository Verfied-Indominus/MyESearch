from App.models import User
from flask_login import UserMixin

class Student(UserMixin, User):
    
    def __init__(self):
        super(Student,self).__init__(email, password, first_name, middle_name, last_name, institution, faculty, department, image_url) #need to populate arguments  

    def toDict(self):
        return super.toDict()