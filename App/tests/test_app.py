import os, tempfile, logging, unittest, pytest, datetime
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import Researcher, Student, Topic, Library, Publication, Notification
from App.controllers.library import *
from App.controllers.researcher import *
from App.controllers.publication import *
# from App.controllers.student import *
from App.controllers.topic import *
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


class PublicationUnitTests(unittest.TestCase):

    def setUp(self):
        self.data = {
            "id" : None,
            'title': "Test PUB",
            'abstract':"this apparently is an abstract.",
            'pub_type':"lol",
            'free_access':True
        }
        self.new_pub = Publication(self.data["title"],self.data["abstract"],self.data["free_access"],self.data["pub_type"])

    def test01_is_publication(self):
        self.assertTrue(isinstance(self.new_pub,Publication))

    def test02_correct_publication(self):
        self.assertDictEqual(self.data, self.new_pub.toDict())

class TopicUnitTests(unittest.TestCase):

    def setUp(self):
        self.data =  {
            'id': None,
            'name': "Test",
            'subtopics': [],
            'parent_topic_id': 1
        }
        self.new_topic = Topic(self.data["name"])
        self.new_topic.set_parent_id(1)

    def test01_is_topic(self):
        self.assertTrue(isinstance(self.new_topic,Topic))

    def test02_is_correct(self):
        self.assertDictEqual(self.new_topic.toDict(), self.data)

class StudentUnitTests(unittest.TestCase):
    def setUp(self):
        self.password = "bobpass"
        self.data={
            'id': None,
            'email': "bob@mail.com",
            'first_name': "bob",
            'middle_name': "bob",
            'last_name': "burger",
            'institution': "UWI",
            'faculty': "HFE",
            'department': "Gender Studies",
            'image_url': "None"
        }
        self.new_student = Student(self.data["email"], self.password, self.data["first_name"], self.data["middle_name"],self.data["last_name"], self.data["institution"], self.data["faculty"], self.data["department"], self.data["image_url"])
    
    def test01_is_student(self):
        self.assertTrue(isinstance(self.new_student, Student))

    def test02_password_check(self):
        self.assertFalse(self.new_student.password,self.password)

    def test03_correct_data(self):
        self.assertDictEqual(self.data, self.new_student.toDict())

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


class PublicationIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.data = {
            'id':0,
            'title': "Test PUB",
            'abstract':"this apparently is an abstract.",
            'pub_type':"article",
            'free_access':True
        }

    def test01_create_pub(self):
        self.assertTrue(create_pub(self.data))

    def test02_get_pub(self):
        self.assertEquals(get_pub(self.data["title"]).title, self.data["title"])

    def test03_update(self):
        pub = get_pub(self.data['title'])
        self.assertTrue(update_pub(self.data,pub.id))

    def test04_delete_pub(self):
        pub = get_pub(self.data["title"])
        self.assertTrue(delete_pub(pub.id))






# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None



