import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user
from App.controllers.pdf import get_information
from App.controllers.pubrecord import add_pub_record
from App.models.forms import ResearcherSignUpForm, BaseSignUpForm
from App.models.user import User, check_password_hash
from App.controllers.topic import *
from App.controllers.pyre_base import uploadFile
from App.controllers.user import get_all_users, get_user, get_user_by_email
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
import gmail

from App.models.builder import *
from sqlalchemy.sql import func

index_views = Blueprint('index_views', __name__, template_folder='../templates')

dates = list(reversed([i for i in range(1970, 2024)]))
institutions = ['The University of The West Indies']

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
        search_terms = form['search']
        authors, author_publications, topic_authors, publications, topic_publications, topics  = parse_search(search_terms)
        results = []
        results.append(authors)
        results.append([pub.toDict() for pub in author_publications])
        results.append(topic_authors)
        results.append([pub.toDict() for pub in publications])
        results.append([pub.toDict() for pub in topic_publications])
        results.append(topics)

        return render_template('results.html', results=results, search=True, search_terms=search_terms)

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

    # suggestions = []
    # if (isinstance(current_user, User)):
    #     suggestions = get_home_suggestions(current_user)

    return render_template('index.html',topics=topics)
    # return render_template('index.html',topics=topics, suggestions=suggestions)

@index_views.route('/publication/<id>',methods=["GET"])
def publication_page(id):
    pub = get_pub_byid(id)
    
    if not pub:
        flash('Publication does not exist or is inaccessible')
        return redirect(url_for('.index_page')) 
    return render_template("publication.html", pub=pub)

@index_views.route('/topic/<id>', methods=['GET'])
def topic_page(id):
    topic_ = get_topic_id(id) 
    print('got topic')
    pubs = get_all_publications()
    print('after pubs')

    if not topic_:
        flash('Topic does not exist or is inaccessible')
        return redirect(url_for('.index_page')) 
    
    topic_pubs = []
    topic_researchers = []
    print('before loopss')
    for tag in topic_.pub_tags.all():
        print('in first loop')
        topic_pubs.append(tag.publication.toDict())
        print('pub dictionary')
        for rec in tag.publication.pub_records:
            print('pub 2nd loop recs')
            re = rec.researcher.toDict()
            print('re dict\n\n')
            if re not in topic_researchers:
                topic_researchers.append(re)
        print('finished loop 2')

    return render_template('results.html', topic_=topic_, topic_page=True, topic_pubs=topic_pubs, topic_researchers=topic_researchers)

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
            flash(f'Welcome {user.first_name}')
            return redirect(url_for('.index_page'))
        else:
            flash('Incorrect credentials entered')

    return render_template('login.html')

@index_views.route('/logout', methods=['GET'])
def logout():
    if not isinstance(current_user, User):
        flash('Not currently logged in')
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

        builder.build()

        if re:
            user = builder.researcher
        else:
            user = builder.student

        if not user:
            flash('There already is an account associated with that email')
            return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

        create_library(user.id)
        create_recents(user.id)

        if re:
            add_interests_to_researcher(re_interests, user.id)

        if image:
            image_url = uploadFile(user.id, image[0])
            remove(f"App/uploads/{image[0]}")
            builder.image_url(image_url)
            builder.build()

        login_user(user, False)
        flash('You successfully created your account')

        if re:
            return redirect(url_for('.add_publication', id=user.id))
        else:
            return redirect(url_for('.index_page'))
    return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

@index_views.route('/addpublication/<id>', methods=['GET', 'POST'])
def add_publication(id):
    res = get_researcher(id)
    if not res:
        flash("The specified User ID does not exist or is not a Researcher's")
        flash('Researchers may also add publications in their profile')
        return redirect(url_for('.index_page'))

    if request.method == 'POST':
        form = request.form
        data = {
            'title': form['title'],
            'abstract': form['abstract'],
            'pub_type': form['pub_type'],
            'publication_date': datetime.date(datetime(form['publication_date'], 1, 1)),
            'url': form['url'],
            'eprint': form['eprint']
        }
        if '.pdf' in form['url'] or '.pdf' in form['eprint']:
            data['free_access'] = True
        else:
            data['free_access'] = False

        pub = create_pub(data)
        add_pub_record(res.id, pub.id)

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

        flash('A publication has been succesfully added')
        return redirect(url_for('.index_page'))
    return render_template('addpublication.html', id=id, types=types, dates=dates)

@index_views.route('/profile/addpublication', methods=['POST'])
def add_profile_pub():
    res = current_user
    form = request.form
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
    print(pub.toDict())
    print(res)
    add_pub_record(res.id, pub.id)

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

    flash('A publication has been succesfully added')
    return redirect(url_for('.profile', id=res.id))

@index_views.route('/myprofile', methods=['GET'])
def my_profile():
    if not isinstance(current_user, User):
        flash('Not currently logged in')
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
        flash('User does not exist or is inaccessible')
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

    if image:
        image_url = uploadFile(id, image[0])
        remove(f"App/uploads/{image[0]}")
        builder.image_url(image_url)

    if form['current_password']!='' and form['new_password']!='' and form['confirm_password']!='':
        if user.check_password(form['current_password']):
            if form['new_password']==form['confirm_password']:
                builder = builder.password(form['new_password'])
                flash('Password successfully changed')
            else:
                flash('Passwords not matching')
                return redirect(f'/profile/{id}')
        else:
            flash('Incorrect Password entered')
            return redirect(f'/profile/{id}')
    elif form['current_password']=='' and form['new_password']=='' and form['confirm_password']=='':
        pass
    else:
        flash('Password field(s) left blank')
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
    flash('Profile updated')
    return redirect(f'/profile/{id}')

# EMAIL : myesearch.noreply@gmail.com
# PASSWORD: admin@noreply
# APP_PASSWORD: sibvelfmfcupbche

@index_views.route("/mail", methods=['GET'])
def mails():
    mail = gmail.GMail("myesearch.noreply@gmail.com","sibvelfmfcupbche")
    msg = gmail.Message(
        subject="Hello World",
        cc=None,
        to="shivanmaharaj.sm@gmail.com",
        text="This is a test mail",
        html=None,
        attachments=None
        )
    mail.send(msg)
    mail.close()
    return "Email sent :)"

@index_views.route('/test', methods=['GET'])
def test():

    
    builder = (
        ResearcherBuilder()
        .title('Prof.')
        .first_name('Patrick')
        .last_name('Hosein')
        .email('patrick.hosein@sta.uwi.edu')
        .password('patrickpass')
        .institution('The University of The West Indies, St. Augustine')
        .faculty('Science & Technology')
        .department('Computing & Information Technology')
        .position('Professor')
        .start_year('2010')
        .qualifications('PhD (MIT)')
        .skills('Wireless Networks')
    )

    builder.build()

    topic = get_topic_by_name('Artificial Intelligence')
    if not topic:
        topic = create_topic('Artificial Intelligence')
    add_interests_to_researcher([topic], builder.researcher.id)

    create_library(builder.researcher.id)
    create_recents(builder.researcher.id)

    builder = (
        ResearcherBuilder()
        .title('Dr.')
        .first_name('Phaedra')
        .last_name('Mohammed')
        .email('Phaedra.Mohammed@sta.uwi.edu')
        .password('phaedrapass')
        .institution('The University of The West Indies, St. Augustine')
        .faculty('Science & Technology')
        .department('Computing & Information Technology')
        .position('Full-Time Lecturer')
        .start_year('2017')
        .qualifications('Ph.D. Computer Science (UWI)')
        .certifications('Raspberry Pi Certified Educator')
        .skills('Computational Models of Culture, Intelligent Tutoring Systems, Expert Systems, Knowledge Representation, Ontological Modelling')
        .build()
        .image_url(uploadFile(builder.researcher.id, 'phaedra.jpg'))
        .build()
    )

    interests = ['Artificial Intelligence in Education', 'Learning Engineering', 'Semantic Web Technologies', 'Natural Language Processing', 'Intelligent Learning Environments']
    topics = []
    for name in interests:
        topic = get_topic_by_name(name)
        if not topic:
            topic = create_topic(name)
            for top in get_all_topics():
                if top.name in topic.name:
                    topic.set_parent_id(top.id)
                elif topic.name in top.name:
                    top.set_parent_id(topic.id)
        topics.append(topic)
    add_interests_to_researcher(topics, builder.researcher.id)

    create_library(builder.researcher.id)
    create_recents(builder.researcher.id)

    builder = (
        ResearcherBuilder()
        .title('Mr.')
        .first_name('Amit')
        .middle_name('Neil')
        .last_name('Ramkissoon')
        .email('amit.ramkissoon@my.uwi.edu')
        .password('amitpass')
        .institution('The University of The West Indies, St. Augustine')
        .faculty('Science & Technology')
        .department('Computing & Information Technology')
        .position('Teaching Assistant')
        .start_year('2020')
        .qualifications('B.Sc. Computer Science (UWI)\nM.Sc. Computer Science (UWI)\nPh.D. Computer Science (UWI) - in progress')
        .skills('Fake News Detection\nSocial Computing\nInfrastructureless Social Networks')
        .introduction('Amit Neil Ramkissoon is a PhD Computer Science Candidate at the Department of Computing & Information Technology at The University of the West Indies at St Augustine. He did both his Bachelors Degree and Masters Degree at The University of the West Indies at St Augustine. His research interest entails Artificial Intelligence, Computational Social Systems, Data Mining, Distributed Computing, Fake News Detection and Mobile Ad Hoc Networks.')
        .website_url('https://sites.google.com/site/amitneilramkissoon')
        .build()
        .image_url(uploadFile(builder.researcher.id, 'amit.jpg'))
        .build()
    )

    interests = ['Data Mining', 'Distributed Computing', 'Artificial Intelligence', 'Computational Social Systems', 'Fake News Detection']
    topics = []
    for name in interests:
        topic = get_topic_by_name(name)
        if not topic:
            topic = create_topic(name)
            for top in get_all_topics():
                if top.name in topic.name:
                    topic.set_parent_id(top.id)
                elif topic.name in top.name:
                    top.set_parent_id(topic.id)
        topics.append(topic)
    add_interests_to_researcher(topics, builder.researcher.id)

    create_library(builder.researcher.id)
    create_recents(builder.researcher.id)

    builder = (
        ResearcherBuilder()
        .title('Dr.')
        .first_name('Vijayanandh')
        .last_name('Rajamanickam')
        .email('Vijayanandh.Rajamanickam@sta.uwi.edu')
        .password('vijayanandhpass')
        .institution('The University of The West Indies, St. Augustine')
        .faculty('Science & Technology')
        .department('Computing & Information Technology')
        .position('Full-Time Lecturer')
        .start_year('2021')
        .qualifications('B.Sc. Mathematics\nM.C.A Computer Applications\nM.Phil Computer Science\nPh.D Computer Science')
        .skills('Image Processing')
    )

    builder.build()

    interests = ['Image Processing', 'Image Segmenation', 'Image and Video Security']
    topics = []
    for name in interests:
        topic = get_topic_by_name(name)
        if not topic:
            topic = create_topic(name)
            for top in get_all_topics():
                if top.name in topic.name:
                    topic.set_parent_id(top.id)
                elif topic.name in top.name:
                    top.set_parent_id(topic.id)
        topics.append(topic)
    add_interests_to_researcher(topics, builder.researcher.id)

    create_library(builder.researcher.id)
    create_recents(builder.researcher.id)
    
    # data = {}
    # data['title'] = 'Veracity: A Fake News Detection Architecture for MANET Messaging'
    # data['abstract'] = 'Mobile Ad Hoc Network Messaging has become an integral part of today’s social communication landscape. They are used in a variety of applications. One major problem that these networks face is the spread of fake news. This problem can have serious deleterious effects on our social data driven society. Detecting fake news has proven to be challenging even for modern day algorithms. This research presents, Veracity, a unique computational social system to accomplish the task of Fake News Detection in MANET Messaging. The Veracity architecture attempts to model social behaviour and human reactions to news spread over a MANET. Veracity introduces five new algorithms namely, VerifyNews, CompareText, PredictCred, CredScore and EyeTruth for the capture, computation and analysis of the credibility and content data features. The Veracity architecture works in a fully distributed and infrastructureless environment. This study validates Veracity using a generated dataset with features relating to the credibility of news publishers and the content of the message to predict fake news. These features are analysed using a machine learning prediction model. The results of these experiments are analysed using four evaluation methodologies. The analysis reveals positive performance with the use of the fake news detection architecture.'
    # data['free_access'] = False
    # data['pub_type'] = 'conference paper'
    # data['publication_date'] = datetime.date(datetime.now())
    # data['url'] = 'https://google.com'
    # data['eprint'] = 'https://google.com'
    # pub = create_pub(data)
    # print(pub)
    # print(pub.toDict())



    # pubs = get_all_publications()
    # count = 1
    # for pub in pubs:
    #     print(count)
    #     count += 1
    #     if len(pub.tags.all()) == 0: 
    #         abstract = pub.abstract
    #         print(abstract)
    #         request = f"Extract the main topics pertaining to Computer Science from the following text as a python list: '{abstract}'"
    #         keywords  = prompt(request)["choices"][0]["text"]
    #         print(keywords)
    #         keywords = '[' + keywords.split('[')[1]
    #         keywords = ast.literal_eval(node_or_string=keywords.strip())
    #         for key in keywords:
    #             topic = get_topic_by_name(key.title())
    #             if not topic and len(key) < 60:
    #                 topic = create_topic(key.title())
    #                 for top in get_all_topics():
    #                     if top.name in topic.name:
    #                         set_topic_parent(topic.name, top.id)
    #                     if topic.name in top.name:
    #                         set_topic_parent(top.name, topic.id)
    #             if topic:
    #                 added = add_topic_to_pub(pub, topic)
    #                 if not added:
    #                     print('\nNOT ADDED\n') 
    #                     print(pub.title)
    #                     print(topic.name)
    #                     print('\n')
    #         print('\n\n', abstract)
    #         print(keywords)
    #         print([tag.topic.name for tag in pub.tags.all()])

    # for pub in get_all_publications(): 
    #     print('\n', pub.pub_type)
    #     print(pub.bibtex, '\n')  


    print('\n\nDONE\n\n')


    '''
    conference paper:
    booktitle, organization, pages

    patent:
    month, note, publisher

    article:
    journal, number, pages, publisher

    incollection:
    booktitle, pages, publisher

    techreport:
    institution

    phdthesis:
    author, pub_year, title
    '''

    # for pub in pubs:
        # if pub.bibtex and 'Patent' in pub.bibtex:
        #     set_pub_type(pub, 'patent')
        # if not pub.bibtex:
        #     print(pub.title, '\n')
        #     bibtex = search_pub_title(pub)
        #     if bibtex:
        #         items = []
        #         bibtex = bibtex.split(sep='{', maxsplit=1)[1].split(sep=',\n ', maxsplit=1)[1]
        #         bibtex = bibtex[:-3]
        #         items.extend([item.strip() for item in bibtex.split(',\n')])
        #         items.pop(0)
        #         bibtex = {}
        #         for item in items:
        #             bibtex[item.split('=')[0].strip()] = item.split('=')[1].strip().strip('}{')
        #         bibtex = json.dumps(bibtex)
        #         set_pub_bibtex(pub, bibtex)
        #         if 'Patent' in pub.bibtex:
        #             set_pub_type(pub, 'patent')
        #         print(pub.bibtex)
        #         print(pub.id)
        #         print('\n\n')
        #     else:
        #         print('\nNot Found\n')
            
    return 'bibtex'
