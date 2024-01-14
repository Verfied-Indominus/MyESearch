import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user
from App.controllers.notification import author_added_notif, request_access
from App.controllers.pdf import get_information
from App.controllers.pubrecord import add_pub_record
from App.controllers.verify import verify_process
from App.models.forms import ResearcherSignUpForm, BaseSignUpForm
from App.models.user import User, check_password_hash
from App.controllers.topic import *
from App.controllers.pyre_base import uploadFile, uploadPDF
from App.controllers.user import get_user, get_user_by_email
from App.controllers.publication import *
from App.controllers.researcher import *
from App.controllers.suggestions import *
from App.controllers.library import *
from App.controllers.recents import *
from App.controllers.auth import login_user, logout_user
from App.controllers.scholarly_py import *
from App.controllers.search import parse_search
from werkzeug.utils import secure_filename 
from os import remove
from datetime import datetime
import json

from App.models.builder import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

dates = list(reversed([i for i in range(1970, 2024)]))
institutions = ['The University of The West Indies']

global image 
image = []
re_interests = []

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

departments = {
    'Engineering': [
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research',
    ],
    'Food & Agriculture': [
        'Agricultural Economics and Extension',
        'Food Production',
        'Publications and Communications Unit',
        'University Farms',
        'Geography'
    ],
    'Humanities & Education': [
        'School of Education',
        'Centre for Language Learning',
        'Creative and Festival Arts',
        'History',
        'Literary, Cultural and Communication Studies',
        'Modern Languages and Linguistics',
        'The Archaeology Centre',
        'The Centre for Language Learning',
        "The Family Development and Children's Research Centre (FDCRC)",
        'The Film Programme'
    ],
    'Law': [
        'Faculty of Law'
    ],
    'Medical Sciences': [
        'Schools of Medicine',
        'Schools of Optometry',
        'Schools of Dentistry',
        'Schools of Nursing',
        'Schools of Pharmacy',
        'Schools of Veterinary Medicine', 
        'Caribbean Centre for Health Systems Research and Development',
        'Centre for Medical Sciences Education',
    ],
    'Science & Technology': [
        'Chemistry',
        'Physics',
        'Life Sciences',
        'Mathematics & Statistics',
        'Computing & Information Technology',
        'Cocoa Research Centre',
        'Seismic Research Unit',
        'The National Herbarium'
    ],
    'Social Sciences': [
        'Behavioural Sciences',
        'Economics',
        'Management Studies',
        'Political Science',
        'Arthur Lok Jack Graduate School for Business',
        'Caribbean Centre for Money and Finance',
        'Centre for Criminology and Criminal Justice',
        'Institute for Gender and Development Studies',
        'Institute of International Relations',
        'Entrepreneurship Unit',
        'Health Economics Unit',
        'Sir Arthur Lewis Institute of Social & Economic Studies',
        'Sustainable Economic Development Unit',
        'Business Development Unit',
    ],
    'Sport': [
        'St. Augustine Academy of Sport'
    ],
}

departments2 = [ 
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research'
    ]

types = [
        'article', 'book', 'chapter', 'code', 'conference paper', 'cover page', 'data', 'experiment finding', 'incollection', 'method', 'misc',
        'negative results', 'patent', 'phdthesis', 'poster', 'preprint', 'presentation', 'raw data', 'research proposal',
        'technical report', 'techreport', 'thesis'
    ]

@index_views.route('/all/publications',methods=['GET'])
def all_publications():
    pubs = get_all_publications()
    types = []
    for pub in pubs:
        if pub.pub_type not in types:
            types.append(pub.pub_type)
    return render_template("results.html", publications=True, now=datetime.utcnow(), types=types)
 
@index_views.route('/all/researchers',methods=['GET'])
def all_researchers():
    return render_template("results.html", researchers=True, faculties=faculties)

@index_views.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_terms = form['search'].strip()
        authors, author_publications, topic_authors, publications, topic_publications, topics  = parse_search(search_terms)
        results = []
        results.append(authors)
        results.append([pub.toDict() for pub in author_publications])
        results.append(topic_authors)
        results.append([pub.toDict() for pub in publications])
        results.append([pub.toDict() for pub in topic_publications])
        results.append(topics)

        return render_template('results.html', results=results, search=True, search_terms=search_terms)
    flash('No search query submitted.')
    return redirect('/')

@index_views.route('/', methods=['GET'])
def index_page():
    topics = [
        'Artificial Intelligence',
        'Biotechnology',
        'Climate Change',
        'Computer Science',
        'Energy',
        'Materials Science',
        'Medicine',
        'Neuroscience',
        'Quantum Computing', 
        'Robotics'
    ]

    return render_template('index.html',topics=topics)

@index_views.route('/publication/<id>',methods=["GET"])
def publication_page(id):
    pub = get_pub_byid(id)
    
    if not pub:
        flash('Publication does not exist or is inaccessible.')
        return redirect(url_for('.index_page')) 
    return render_template("publication.html", pub=pub)

@index_views.route('/topic/<id>', methods=['GET'])
def topic_page(id):
    topic_ = get_topic_id(id) 
    pubs = get_all_publications()

    if not topic_:
        flash('Topic does not exist or is inaccessible.')
        return redirect(url_for('.index_page'))
    
    topic_pubs = []
    topic_researchers = []
    for tag in topic_.pub_tags.all():
        topic_pubs.append(tag.publication.toDict())
        for rec in tag.publication.pub_records:
            re = rec.researcher.toDict()
            if re not in topic_researchers:
                topic_researchers.append(re)

    topic_pubs.sort(key=lambda pub: pub['publication_date'], reverse=True)
    return render_template('results.html', topic_=topic_, topic_page=True, topic_pubs=topic_pubs, topic_researchers=topic_researchers)

@index_views.route('/login', methods=['GET', 'POST'])
def login_page():
    remember = False
    if request.method == 'POST':
        form = request.form
        user = get_user_by_email(form['email'].lower())
        if user and check_password_hash(user.password, form['password']):
            if 'remember' in form:
                remember = True
            login_user(user, remember)
            flash(f'Welcome {user.first_name}!')
            return redirect(url_for('.index_page'))
        else:
            flash('Incorrect credentials entered.')

    return render_template('login.html')

@index_views.route('/logout', methods=['GET'])
def logout():
    if not isinstance(current_user, User):
        flash('Not currently logged in.')
    else:
        logout_user()
    return redirect(url_for('.index_page'))

@index_views.route('/interests/<selected>', methods=['GET'])
def parse_interests(selected):
    selected = json.loads(selected)
    re_interests.extend(selected['selected'])
    print(re_interests)
    return 'Interests Checked'

@index_views.route('/filename', methods=['POST'])
def filename():
    img = request.files['files[]']
    global image
    image.append(secure_filename(img.filename))
    img.save(f"App/uploads/{image[0]}")
    return image[0]

@index_views.route('/extract', methods=['GET'])
def extract():
    keywords, abstract, title = get_information(f"App/uploads/{image[0]}")
    print([keywords, abstract, title])
    return [keywords, abstract, title]

@index_views.route('/signup', methods=['GET', 'POST'])
def signup_page():
    interests = get_signup_topics()

    baseForm = BaseSignUpForm()
    reForm = ResearcherSignUpForm()
    baseForm.institution.choices = institutions
    baseForm.faculty.choices = faculties
    baseForm.department.choices = departments2
    
    reForm.start_date.choices = dates

    if request.method == 'POST':
        form = request.form 
        re = False

        if 'title' in form:
            builder = ResearcherBuilder()
            re = True
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
        
        if re:
            builder = (
                builder
                    .title(form['title'])
                    .position(form['position'])
                    .start_year(form['start_date'])
                    .qualifications(form['qualifications'])
                    .skills(form['skills'])
            )

            if form['certifications']:
                builder.certifications(form['certifications'])
            if form['website']:
                builder.website_url(form['website'])
            if form['introduction']:
                builder.introduction(form['introduction'])

        user = builder.build()

        if not user:
            flash('There already is an account associated with that email.')
            return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)
        elif re and user:
            user = builder.researcher
        else:
            user = builder.student

        create_library(user.id)
        create_recents(user.id)

        if re:
            add_interests_to_researcher(re_interests, user.id)

        global image
        if image:
            image_url = uploadFile(user.id, image[0])
            remove(f"App/uploads/{image[0]}")
            image = []
            builder.image_url(image_url)
            builder.build()

        login_user(user, False)
        flash('You successfully created your account!')

        if re:
            verify_process(user.id)
            return redirect(url_for('.add_publication', id=user.id))
        else:
            return redirect(url_for('.index_page'))
    return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

@index_views.route('/addpublication/<id>', methods=['GET', 'POST'])
def add_publication(id):
    res = get_researcher(id)
    if not res:
        flash("The specified User ID does not exist or is not a Researcher's.")
        flash('Researchers may also add publications in their profile.')
        return redirect(url_for('.index_page'))

    if request.method == 'POST':
        form = request.form
        global image
        filename = ''
        if image:
            filename = image[0]
            image = []

        data = {
            'title': form['title'].lower(),
            'abstract': form['abstract'],
            'pub_type': form['pub_type'].lower(),
            'publication_date': datetime.date(datetime(int(form['publication_date']), 1, 1)),
            'url': form['url'],
            'eprint': form['eprint']
        }
        if '.pdf' in form['url'] or '.pdf' in form['eprint']:
            data['free_access'] = True
        else:
            data['free_access'] = False

        pub = create_pub(data)
        add_pub_record(res.id, pub.id)

        if filename:
            set_encrypted_pdf_url(pub, uploadPDF(pub.id, filename))

        keywords = re.split('\s*,\s', form['coauthors'])
        for key in keywords:
            topic = get_topic_by_name(key.title())
            if not topic:
                topic = create_topic(key.title())
                for top in get_all_topics():
                    if top.name in topic.name:
                        topic.set_parent_id(top.id)
                    if topic.name in top.name:
                        top.set_parent_id(topic.id)
            add_topic_to_pub(pub=pub, topic=topic)

        coauthors = re.split('\s*,\s*', form['coauthors'])
        users = get_all_researchers()
        for res in users:
            target = []
            for co in coauthors:
                if res.first_name.lower() in co.lower() and res.last_name.lower() in co.lower():
                    target.append(coauthors.index(co))
            for t in target:
                add_pub_record(res.id, pub.id)
                coauthors.remove(coauthors[t])
        authors = ', '.join(coauthors)

        add_coauthors(pub, authors)
        author_added_notif(p_id=pub.id, r_id=res.id)

        bibtex = {}

        bibtex['author'] = f"{res.first_name} {res.last_name}, "
        bibtex['author'] += form['coauthors']

        if form['journal']:
            bibtex['journal'] = form['journal']

        if form['publisher']:
            bibtex['publisher'] = form['publisher']

        if form['organization']:
            bibtex['organization'] = form['organization']

        if form['institution']:
            bibtex['institution'] = form['institution']

        if form['booktitle']:
            bibtex['booktitle'] = form['booktitle']

        if form['month']:
            bibtex['month'] = form['month']

        if form['note']:
            bibtex['note'] = form['note']

        if form['pages']:
            bibtex['pages'] = form['pages']

        if form['volume']:
            bibtex['volume'] = form['volume']

        set_pub_bibtex(pub, bibtex)

        flash('A publication has been succesfully added!')
        return redirect(url_for('.index_page'))
    return render_template('addpublication.html', id=id, types=types, dates=dates)

@index_views.route('/profile/addpublication', methods=['POST'])
def add_profile_pub():
    res = current_user
    form = request.form
    global image
    filename = ""
    if image:
        filename = image[0]
        image = []

    data = {
        'title': form['title'].lower(),
        'abstract': form['abstract'],
        'pub_type': form['pub_type'].lower(),
        'publication_date': datetime.date(datetime(int(form['publication_date']), 1, 1)),
        'url': form['url'],
        'eprint': form['eprint']
    }
    if '.pdf' in form['url'] or '.pdf' in form['eprint']:
        data['free_access'] = True
    else:
        data['free_access'] = False

    pub = create_pub(data)
    add_pub_record(res.id, pub.id)
    
    if filename:
        set_encrypted_pdf_url(pub, uploadPDF(pub.id, filename))

    keywords = re.split('\s*,\s', form['coauthors'])
    for key in keywords:
        topic = get_topic_by_name(key.title())
        if not topic:
            topic = create_topic(key.title())
            for top in get_all_topics():
                if top.name in topic.name:
                    topic.set_parent_id(top.id)
                if topic.name in top.name:
                    top.set_parent_id(topic.id)
        add_topic_to_pub(pub=pub, topic=topic)

    coauthors = re.split('\s*,\s*', form['coauthors'])
    users = get_all_researchers()
    for res in users:
        target = []
        for co in coauthors:
            if res.first_name.lower() in co.lower() and res.last_name.lower() in co.lower():
                target.append(coauthors.index(co))
        for t in target:
            add_pub_record(res.id, pub.id)
            coauthors.remove(coauthors[t])
    authors = ', '.join(coauthors)

    add_coauthors(pub, authors)
    author_added_notif(p_id=pub.id, r_id=res.id)

    bibtex = {}

    bibtex['author'] = f"{res.first_name} {res.last_name}, "
    bibtex['author'] += form['coauthors']

    if form['journal']:
        bibtex['journal'] = form['journal']

    if form['publisher']:
        bibtex['publisher'] = form['publisher']

    if form['organization']:
        bibtex['organization'] = form['organization']

    if form['institution']:
        bibtex['institution'] = form['institution']

    if form['booktitle']:
        bibtex['booktitle'] = form['booktitle']

    if form['month']:
        bibtex['month'] = form['month']

    if form['note']:
        bibtex['note'] = form['note']

    if form['pages']:
        bibtex['pages'] = form['pages']

    if form['volume']:
        bibtex['volume'] = form['volume']

    set_pub_bibtex(pub, bibtex)

    flash('A publication has been succesfully added!')
    return redirect(url_for('.profile', id=res.id))

@index_views.route('/myprofile', methods=['GET'])
def my_profile():

    if not isinstance(current_user, User):
        flash('Not currently logged in.')
        return redirect(url_for('.index_page'))
    return redirect(url_for('.profile', id=current_user.id))

@index_views.route('/profile/<id>', methods=['GET'])
def profile(id):
    re = False
    pubs = []
    subs = []
    interests = []

    user = get_user(id)

    if not user or (not isinstance(user, Researcher) and current_user.id != user.id):
        flash('User does not exist or is inaccessible.')
        return redirect(url_for('.index_page'))
    
    topics = get_subscribed_topics(user)
    researchers = get_subscribed_researchers(user)
    library = get_publications_from_library(user.library)
    recents = get_publications_from_recents(user.recents)

    if (isinstance(user, Researcher)):
        re = True
        pubs = len(user.pub_records.all())
        subs = len(user.sub_records.all())
        interests = get_research_topics(user)
        skills = [user.skills]
        if ',' in user.skills:
            skills = user.skills.split(', ')
        if '\n' in user.skills:
            skills = user.skills.split('\n')
        if ',\n' in user.skills:
            skills = user.skills.split(',\n')

        all_topics = get_all_topics()
        all_topics.sort(key=lambda top: top.name)
        
        if isinstance(current_user, User) and (int(current_user.id)==int(id)):
            return render_template('profile.html', user=user, re=re, pubs=pubs, subs=subs, topics=topics, library=library, 
                                   recents=recents, researchers=researchers, interests=interests, skills=skills, types=types, 
                                   dates=dates, faculties=faculties, departments=departments[user.faculty], all_topics=all_topics)

    if isinstance(current_user, Student) and (int(current_user.id)==int(id)):
        return render_template('profile.html', user=user, re=re, library=library, recents=recents, topics=topics, 
                               researchers=researchers, faculties=faculties, departments=departments[user.faculty])

    return render_template('profile.html', user=user, re=re, pubs=pubs, subs=subs, topics=topics, library=library, 
                           recents=recents, researchers=researchers, interests=interests, skills=skills)

@index_views.route('/edit/profile/<id>', methods=['POST'])
def edit_profile(id):
    form = request.form

    re = None
    user = get_user(id)
    if isinstance(user, Researcher):
        re = user
        builder = (
            ResearcherBuilder()
            .existing_researcher(re)
        )
        positions = form.getlist('position')
        positions = ', '.join(positions)
    else:
        builder = (
            StudentBuilder()
            .existing_student(user)
        )

    if 'title' in form:
        builder = (
            builder
            .first_name(form['first_name'])
            .middle_name(form['middle_name'])
            .last_name(form['last_name'])
            .faculty(form['faculty'])
            .department(form['department'])
            .email(form['email'])
        )
        if re:
            builder = (
                builder
                .title(form['title'])
                .position(positions)
                .start_year(form['start_year'])
            )

    global image
    if image:
        image_url = uploadFile(id, image[0])
        remove(f"App/uploads/{image[0]}")
        image = []
        builder.image_url(image_url) 

    if form['current_password']!='' and form['new_password']!='' and form['confirm_password']!='':
        if user.check_password(form['current_password']):
            if form['new_password']==form['confirm_password']:
                builder = builder.password(form['new_password'])
                flash('Password successfully changed!')
            else:
                flash('Passwords not matching.')
                return redirect(f'/profile/{id}')
        else:
            flash('Incorrect Password entered.')
            return redirect(f'/profile/{id}')
    elif form['current_password']=='' and form['new_password']=='' and form['confirm_password']=='':
        pass
    else:
        flash('Password field(s) left blank.')
        return redirect(f'/profile/{id}')

    if 'introduction' in form: 
        topics = []
        delete_researcher_tags(re)
        interests = form['research_interests'].split('\r\n')
        for interest in interests:
            topic = get_topic_by_name(interest)
            topics.append(topic)
        add_interests_to_researcher(topics, id)
            
        builder = (
            builder
            .introduction(form['introduction'])
            .qualifications(form['qualifications'])
            .certifications(form['certifications'])
            .skills(form['skills'])
        )

    builder.build()
    flash('Profile updated!')
    return redirect(f'/profile/{id}')

@index_views.route('/request/<s_id>/<pub_id>', methods=['POST'])
def request_text(s_id, pub_id):
    form = request.form
    pub = get_pub_byid(pub_id)
    for rec in pub.pub_records:
        request_access(s_id, rec.researcher.id, pub_id, form['message'])
    flash('Your request has been sent.')
    return redirect(f'/publication/{pub_id}')
