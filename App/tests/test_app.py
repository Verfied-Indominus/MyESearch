import os, tempfile, logging, unittest, pytest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import Researcher, Student, Topic, Library, Publication, Notification
from App.controllers.library import *
from App.controllers.researcher import *
# from App.controllers.publication import *
# from App.controllers.student import *
# from App.controllers.topic import *
from App.controllers.notification import *

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class ResearcherUnitTests(unittest.TestCase):

    def test01_new_researcher(self):
        email = 'test@mail.com'
        password = 'password'
        first_name = 'Bob'
        middle_name = ''
        last_name = 'Burger'
        institution = 'UWI'
        faculty = 'FST'
        department = 'DCIT'
        image_url = ''
        title = 'Dr.'
        position = 'Lecturer'
        start_year = '2015'
        qualifications = 'B.Sc. Computer Science (UWI)'
        certifications = ''
        skills = 'Data Mining'
        website_url = ''
        introduction = 'My name is Bob.'
        researcher = Researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, image_url, 
                                title, position, start_year, qualifications, certifications, skills, website_url, introduction)
        assert isinstance(researcher, Researcher) and researcher is not None

    # def test_new_user(self):
    #     user = User("bob", "bobpass")
    #     assert user.username == "bob"

    # # pure function no side effects or integrations called
    # def test_toJSON(self):
    #     user = User("bob", "bobpass")
    #     user_json = user.toJSON()
    #     self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    # def test_hashed_password(self):
    #     password = "mypass"
    #     hashed = generate_password_hash(password, method='sha256')
    #     user = User("bob", password)
    #     assert user.password != password

    # def test_check_password(self):
    #     password = "mypass"
    #     user = User("bob", password)
    #     assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
