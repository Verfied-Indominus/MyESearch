from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for
from App.models.forms import ResearcherSignUpForm, BaseSignUpForm
from App.models.user import check_password_hash
from App.controllers.topic import get_topics
from App.controllers.pyre_base import uploadFile
from App.controllers.user import get_user_by_email, get_all_users_json
from werkzeug.utils import secure_filename
from os import remove
import json

from App.models.builder import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

dates = list(reversed([i for i in range(1970, 2024)]))
institutions = ['The University of The West Indies']

image = []

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
        'Mechanical and Manufacturing Enterprise Research'
    ]


@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        form = request.form
        user = get_user_by_email(form['email'])
        if user and check_password_hash(user.password, form['password']):
            return redirect(url_for('.index_page'))

    return render_template('login.html')

@index_views.route('/signup', methods=['GET', 'POST'])
def signup_page():
    # interests = get_topics(15)
    interests = [
        'Engineering',
        'Social Sciences',
        'Food & Agriculture',
        'Humanities & Education',
        'Law',
        'Medical Sciences',
        'Science & Technology',
        'Sport'
    ]

    baseForm = BaseSignUpForm()
    reForm = ResearcherSignUpForm()
    baseForm.institution.choices = institutions
    baseForm.faculty.choices = faculties
    baseForm.department.choices = departments
    
    reForm.start_date.choices = dates

    if request.method == 'POST':
        form = request.form 

        if 'title' in form:
            builder = ResearcherBuilder()
        else:
            builder = StudentBuilder()

        builder = (
            builder
                .email(form['email'])
                .password(form['password'])
                .first_name(form['first_name'])
                .last_name(form['last_name'])
                .institution(form['institution'])
                .faculty(form['faculty'])
                .department(form['department'])
        )

        if form['middle_name']:
            builder.middle_name(form['middle_name'])

        if image:
            image_url = uploadFile(image[0])
            remove(f"App/uploads/{image[0]}")
            builder.image_url(image_url)
        
        if isinstance(builder, ResearcherBuilder):
            builder = (
                builder
                    .title(form['title'])
                    .position(form['position'])
                    .start_year(form['start_year'])
                    .qualifications(form['qualifications'])
                    .skills(form['skills'])
            )

            if form['certifications']:
                builder.certifications(form['certifications'])
            if form['website']:
                builder.website_url(form['website'])
            if form['introduction']:
                builder.introduction(form['introduction'])

        builder.build()

        return redirect(url_for('.index_page'))
    return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

@index_views.route('/interests/<selected>', methods=['GET'])
def parse_interests(selected):
    selected = json.loads(selected)
    print(selected)
    return 'Interests Checked'

@index_views.route('/filename', methods=['POST'])
def filename():
    img = request.files['files[]']
    img.save(f"App/uploads/{img.filename}")
    image.append(secure_filename(img.filename))
    return img.filename