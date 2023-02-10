import os, tempfile, logging, unittest, pytest, datetime
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
    def setUp(self):
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
        self.researcher = Researcher(
            email, password, first_name, middle_name, last_name, institution, faculty, department, image_url, title, 
            position, start_year, qualifications, certifications, skills, website_url, introduction)
    
    def test01_new_researcher(self):
        assert isinstance(self.researcher, Researcher) and self.researcher is not None

    def test02_researcher_toDict(self):
        researcher_dict = self.researcher.toDict()
        self.assertDictEqual(researcher_dict, {
            'id': None,
            'email': 'test@mail.com',
            'first_name': 'Bob',
            'middle_name': '',
            'last_name': 'Burger',
            'institution': 'UWI',
            'faculty': 'FST',
            'department': 'DCIT',
            'image_url': '',
            'title': 'Dr.',
            'position': 'Lecturer',
            'start_year': '2015',
            'qualifications': 'B.Sc. Computer Science (UWI)',
            'certifications': '',
            'skills': 'Data Mining',
            'website_url': '',
            'introduction': 'My name is Bob.'
        })

    def test03_researcher_password(self):
        self.assertNotEqual(self.researcher.password, 'password')


class LibraryUnitTests(unittest.TestCase):

    def test01_new_library(self):
        library = Library(1)
        assert isinstance(library, Library) and library is not None

    def test02_library_toDict(self):
        library = Library(1)
        library_dict = library.toDict()
        self.assertDictEqual(library_dict, {
            'id': None,
            'user_id': 1,
            'records': []
        })

class NotificationUnitTests(unittest.TestCase):
    def test01_new_notification(self):
        notif = Notification('New notification', 'This is a test notification.')
        assert isinstance(notif, Notification) and notif is not None
    
    def test02_notification_toDict(self):
        notif = Notification('New notification', 'This is a test notification.')
        notif_dict = notif.toDict()
        self.assertDictEqual(notif_dict, {
            'id': None,
            'title': 'New notification',
            'message': 'This is a test notification.',
            'timestamp': None,
            'last_updated': None,
            'notification_records': []
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/instance/test.db')


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
