from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for
from App.models.forms import *
from App.controllers.topic import get_topics
import json

index_views = Blueprint('index_views', __name__, template_folder='../templates')

dates = [i for i in range(1970, 2024)]
institutions = ['The University of The West Indies']
faculties = [
        'Engineering',
        'Food & Agriculture',
        'Humanities & Education',
        'Law',
        'Medical Sciences',
        'Science & Technology',
        'Social Sciences',
        'Sport'
]
departments = [
    'Chemical Engineering',
    'Civil & Environmental Engineering',
    'Mechanical & Manufacturing Engineering',
    'Geomatics Engineering & Land Management',
    'Engineering Institute',
    'Electrical & Computer Engineering',
    'Agricultural Economics and Extension',
    'Food Production',
    'Geography',
    'Business Development Unit',
    'Publications and Communications Unit',
    'University Farms',
    'School of Education',
    'Centre for Language Learning',
    'Creative and Festival Arts',
    'History',
    'Literary, Cultural and Communication Studies',
    'Modern Languages and Linguistics',
    'Faculty of Law',
    'Schools of Medicine',
    'Schools of Optometry',
    'Schools of Dentistry',
    'Schools of Nursing',
    'Schools of Pharmacy',
    'Schools of Veterinary Medicine',
    'Chemistry',
    'Physics',
    'Life Sciences',
    'Mathematics & Statistics',
    'Computing & Information Technology',
    'Behavioural Sciences',
    'Economics',
    'Management Studies',
    'Political Science',
    'St. Augustine Academy of Sport',
    'Mechanical and Manufacturing Enterprise Research',
    'The Archaeology Centre',
    'The Centre for Language Learning',
    "The Family Development and Children's Research Centre (FDCRC)",
    'The Film Programme',
    'Caribbean Centre for Health Systems Research and Development',
    'Centre for Medical Sciences Education',
    'Cocoa Research Centre',
    'Seismic Research Unit',
    'The National Herbarium',
    'Arthur Lok Jack Graduate School for Business',
    'Caribbean Centre for Money and Finance',
    'Centre for Criminology and Criminal Justice',
    'Institute for Gender and Development Studies',
    'Institute of International Relations',
    'Entrepreneurship Unit',
    'Health Economics Unit',
    'Sir Arthur Lewis Institute of Social & Economic Studies',
    'Sustainable Economic Development Unit'
]


@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/signup', methods=['GET'])
def signup_page():
    interests = get_topics(15)
    
    baseForm = BaseSignUpForm()
    reForm = ResearcherSignUpForm()
    baseForm.institution.choices = institutions
    baseForm.faculty.choices = faculties
    baseForm.department.choices = departments
    reForm.start_date.choices = dates
    reForm.interests.choices = interests 
    return render_template('signup.html', baseForm=baseForm, reForm=reForm)

@index_views.route('/interests/<selected>', methods=['GET'])
def parse_interests(selected):
    selected = json.loads(selected)
    print(selected)
    return 'Interests Checked'