import os, tempfile, logging, unittest, pytest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from App.main import create_app
from App.database import create_db, drop_db
from App.models import Researcher, Student, Topic, Library, Publication, Notification, User
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
    @classmethod
    def setUpClass(cls):
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
        cls.researcher = create_researcher(
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
        notif = create_notification('New notification', 'This is a test notification.')
        assert isinstance(notif, Notification) and notif is not None
    
    def test02_notification_toDict(self):
        notif = create_notification('New notification', 'This is a test notification.')
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

class ResearcherIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        cls.researcher = create_researcher(
            email, password, first_name, middle_name, last_name, institution, faculty, department, image_url, title, 
            position, start_year, qualifications, certifications, skills, website_url, introduction)
    
    def test01_new_researcher_created(self):
        assert isinstance(self.researcher, Researcher) and self.researcher.id == 1

    def test02_int_researcher_toDict(self):
        researcher_dict = self.researcher.toDict()
        self.assertIsInstance(researcher_dict, dict)
        self.assertDictEqual(researcher_dict, {
            'id': 1,
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

    def test03_update_researcher_name(self):
        update_researcher_fname(self.researcher.id, 'Robbert')
        assert self.researcher.first_name == 'Robbert'

    def test04_add_researcher_website(self):
        update_researcher_website_url(self.researcher.id, 'google.com')
        assert self.researcher.website_url == 'google.com'

    def test05_update_researcher_middle_name(self):
        update_researcher_midname(self.researcher.id, 'Sam')
        assert self.researcher.middle_name == 'Sam'

    def test06_updated_researcher_toDict(self):
        researcher_dict = self.researcher.toDict()
        self.assertDictEqual(researcher_dict, {
            'id': 1,
            'email': 'test@mail.com',
            'first_name': 'Robbert',
            'middle_name': 'Sam',
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
            'website_url': 'google.com',
            'introduction': 'My name is Bob.'
        })


class NotificationIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notif = create_notification('New notification', 'This is a test notification.')

    def test01_new_int_notification(self):
        assert isinstance(self.notif, Notification) and self.notif is not None
    
    def test02_int_notification_toDict(self):
        notif_dict = self.notif.toDict()
        self.assertDictEqual(notif_dict, {
            'id': 1,
            'title': 'New notification',
            'message': 'This is a test notification.',
            'timestamp': datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'), 
            'last_updated': datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'),
            'notification_records': []
        })
    
    def test03_int_notification_update(self):
        before = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        update_notification_title(self.notif.id, 'New Test Notification')
        update_notification_message(self.notif.id, 'This is a new message')
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        notif_dict = self.notif.toDict()
        self.assertDictEqual(notif_dict, {
            'id': 1,
            'title': 'New Test Notification',
            'message': 'This is a new message',
            'timestamp': before, 
            'last_updated': now,
            'notification_records': []
        })

class LibraryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        cls.researcher = create_researcher(
            email, password, first_name, middle_name, last_name, institution, faculty, department, image_url, title, 
            position, start_year, qualifications, certifications, skills, website_url, introduction)
        cls.library = create_library(cls.researcher.id)
        
    def test01_new_library_creation(self):
        assert isinstance(self.library, Library) and self.library is not None

    def test02_library_has_user_id_stored(self):
        assert self.library.user_id == self.researcher.id

    def test03_library_linked_to_user(self):
        user = self.library.user
        assert isinstance(user, Researcher)

    def test04_library_toDict(self):
        library_dict = self.library.toDict()
        self.assertDictEqual(library_dict, {
            'id': 1,
            'user_id': 1,
            'records': []
        })