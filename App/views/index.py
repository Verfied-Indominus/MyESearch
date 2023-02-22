from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from flask_login import current_user
from App.models.forms import ResearcherSignUpForm, BaseSignUpForm
from App.models.user import User, check_password_hash
from App.controllers.topic import get_all_topics
from App.controllers.pyre_base import uploadFile
from App.controllers.user import get_user, get_user_by_email, get_all_users_json
from App.controllers.publication import get_pub_byid, get_all_publications_for_user
from App.controllers.auth import login_user, logout_user
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
    topics = []
    publications = []
    return render_template('index.html',topics=topics,publications=publications)

@index_views.route('/publication/<id>',methods=["GET"])
def publication_page(id):
    
    pub = get_pub_byid(id)
    if not pub:
        return("404")
    return render_template("publication.html",pub=pub.toDict())
    
@index_views.route('/login', methods=['GET', 'POST'])
def login_page():
    remember = False
    if request.method == 'POST':
        form = request.form
        user = get_user_by_email(form['email'])
        if user and check_password_hash(user.password, form['password']):
            if 'remember' in form:
                remember = True
            login_user(user, remember)
            return redirect(url_for('.index_page'))

    return render_template('login.html')

@index_views.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('.index_page'))

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

        if isinstance(builder, StudentBuilder):
            user = builder.student
        else:
            user = builder.researcher

        if not user:
            flash('There already is an account associated with that email')
            return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

        if image:
            image_url = uploadFile(user.id, image[0])
            remove(f"App/uploads/{image[0]}")
            builder.image_url(image_url)
            builder.build()

        login_user(user, False)

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
    image.append(secure_filename(img.filename))
    img.save(f"App/uploads/{image[0]}")
    return image[0]

@index_views.route('/myprofile', methods=['GET'])
def my_profile():
    if not isinstance(current_user, User):
        flash('Not currently logged in')
        return redirect(url_for('.index_page'))
    return jsonify({'message': f"name: {current_user.first_name}, id : {current_user.id}"})

@index_views.route('profile/<id>', methods=['GET'])
def profile(id):
    re = False
    pubs = []
    user = get_user(id)
    if (isinstance(user, Researcher)):
        re = True
        pubs = get_all_publications_for_user(user)

    return 'Unfinished'
