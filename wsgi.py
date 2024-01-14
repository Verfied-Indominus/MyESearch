from datetime import datetime, timedelta
import click, pytest, sys, json
from flask import Flask
from flask.cli import AppGroup

from App.database import create_db, get_migrate, drop_db
from App.main import create_app
from App.controllers import ( get_researcher_by_email, get_all_users_json, get_all_users,
                                create_topic, get_topic_by_name, create_topic_with_parent, get_all_topics,
                                delete_pub, delete_researcher
)

from App.models import User, Student, Researcher



app = create_app()
migrate = get_migrate(app)

# This commands file allow you to create convenient CLI commands for testing controllers

@app.template_filter('to_dict')
def to_dict(my_string):
    return json.loads(my_string)

@app.template_filter('tt_time')
def to_tt_time(dtobj):
    obj = dtobj-timedelta(hours=4)
    return obj.strftime("%B %d, %Y  %I:%M %p")


'''
Generic Commands
'''

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("drop", help="Drops all tables in the database")
def initialize():
    drop_db()
    print('database destroyed')

@app.cli.command("topic_init", help="Initializes the preliminary topics")
def init_topics():
    topics = {}
    with open('topics.txt') as f:
        for line in f.readlines():
            if line[0] != '\n':
                top = line.rstrip()
                temp = top.split(':', 1)
                topics[temp[0]] = temp[1].strip().split(', ')

    for key in topics:
        create_topic(key)
        for index, top in enumerate(topics[key]):
            if str(top).islower():
                topics[key][index] = top.title()

    for key in topics:
        parent = get_topic_by_name(key)
        for topic in topics[key]:
            top = create_topic_with_parent(topic, parent.id)

    f.close()

@app.cli.command("run", help="Run the Application")
def initialize():
    print('hello')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
researcher_cli = AppGroup('researcher', help='Researcher object commands') 

@researcher_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@researcher_cli.command("get", help="Gets a specific researcher")
@click.argument("email", default="test@mail.com")
def get_researcher_command(email):
    print(get_researcher_by_email(email).toDict())

@researcher_cli.command("delete", help="Deletes a specific researcher")
@click.argument("id")
def get_researcher_command(id):
    delete_researcher(id)
    print('deleted')

app.cli.add_command(researcher_cli) # add the group to the cli


user_cli = AppGroup("user", help="User object commands")

@user_cli.command("create")
def create_user_command():
    user = Researcher()
    user2 = Student()
    user.set_password('test')
    user.addSubscriber(user2)
    if user:
        print("User created")
        print(user.password)

app.cli.add_command(user_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("researcher", help="Run Researcher tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ResearcherUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ResearcherIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("library", help="Run Library tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "LibraryUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "LibraryIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

@test.command("notification", help="Run Notification tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "NotificationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "NotificationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("topic", help="Run Topic tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "TopicUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "TopicIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("publication", help="Run Publication tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PublicationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "PublicationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
