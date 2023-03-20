from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user
from App.models.forms import ResearcherSignUpForm, BaseSignUpForm
from App.models.user import User, check_password_hash
from App.controllers.topic import *
from App.controllers.pyre_base import uploadFile
from App.controllers.user import get_user, get_user_by_email, get_user_by_name
from App.controllers.publication import *
from App.controllers.visitrecords import *
from App.controllers.researcher import *
from App.controllers.suggestions import *
from App.controllers.library import *
from App.controllers.recents import *
from App.controllers.auth import login_user, logout_user
from App.controllers.scholarly_py import *
from App.controllers.pubrecord import delete_pub_record
from App.controllers.search import parse_search
from App.controllers.open_ai import prompt, RAIL_KEY, CAESAR_KEY
from App.controllers.ciphers import doubleCipher, doubleDeCipher
from werkzeug.utils import secure_filename
from os import remove
from datetime import datetime
from random import shuffle
import json
import gmail
import ast

from App.models.builder import *


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

departments = [
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research'
    ]

@index_views.route('/all/publications',methods=['GET'])
def all_publications():
    types = [
        'article', 'book', 'chapter', 'code', 'conference paper', 'cover page', 'data', 'experiment finding', 'method', 'misc',
        'negative results', 'patent', 'phdthesis', 'poster', 'preprint', 'presentation', 'raw data', 'research proposal', 
        'technical report', 'techreport', 'thesis'
    ]
    return render_template("results.html", publications=True, now=datetime.utcnow(), types=types)

@index_views.route('/load/publications', methods=['GET'])
def load_publications():
    publications = get_all_publications()
    shuffle(publications) 
    publications = [pub.toDict() for pub in publications]
    return publications

@index_views.route('/load/pubauthors/<id>', methods=['GET'])
def load_pub_authors(id):
    pub = get_pub_byid(id)
    return [record.researcher.toDict() for record in pub.pub_records.all()]

@index_views.route('/all/researchers',methods=['GET'])
def all_researchers():
    return render_template("results.html", researchers=True, faculties=faculties)

@index_views.route('/load/researchers', methods=['GET'])
def load_researchers():
    researchers = get_all_researchers()
    shuffle(researchers)
    print('test')
    return [re.toDict() for re in researchers]

search_pubs = []

@index_views.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_terms = form['search']
        authors, publications, topics = parse_search(search_terms)
        results = []
        results.append(authors)
        results.append([pub.toDict() for pub in publications])
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
    suggestions = []
    if (isinstance(current_user, User)):
        suggestions = get_home_suggestions(current_user)
    return render_template('index.html',topics=topics, suggestions=suggestions)

@index_views.route('/publication/<id>',methods=["GET"])
def publication_page(id):
    pub = get_pub_byid(id)
    
    if not pub:
        flash('Publication does not exist or is inaccessible')
        return redirect(url_for('.index_page')) 
    
    researchers, topics, pubs = get_publication_suggestions(pub)

    return render_template("publication.html", pub=pub, researchers=researchers, topics=topics, pubs=pubs)
    # return render_template("publication.html", pub=pub)

@index_views.route('/topic/<id>', methods=['GET'])
def topic_page(id):
    topic_ = get_topic_id(id) 

    if not topic_:
        flash('Topic does not exist or is inaccessible')
        return redirect(url_for('.index_page')) 

    topic_pubs = [tag.publication.toDict() for tag in topic_.pub_tags]
    
    return render_template('results.html', topic_=topic_, topic_page=True, topic_pubs=topic_pubs)

@index_views.route('/load/profilepubs/<id>', methods=['GET'])
def load_profile_pubs(id):
    re = get_researcher(id)
    return [record.publication.toDict() for record in re.pub_records.all()]

@index_views.route('/load/pubsuggestions/<id>', methods=['GET'])
def load_pub_suggestions(id):
    pub = get_pub_byid(id)

    researchers, topics, pubs = get_publication_suggestions(pub)
    return [[r.toDict() for r in researchers], [t.toDict() for t in topics], [p.toDict() for p in pubs]]

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
    if not isinstance(current_user, User):
        flash('Not currently logged in')
    else:
        logout_user()
    return redirect(url_for('.index_page'))

@index_views.route('/signup', methods=['GET', 'POST'])
def signup_page():
    # interests = [
    #     'Artificial Intelligence',
    #     'Biotechnology',
    #     'Climate Change',
    #     'Computer Science',
    #     'Energy',
    #     'Materials Science',
    #     'Medicine',
    #     'Neuroscience',
    #     'Quantum Computing',
    #     'Robotics'
    # ]
    
    interests = get_signup_topics()

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

        if isinstance(builder, ResearcherBuilder):
            user = builder.researcher
        else:
            user = builder.student

        if not user:
            flash('There already is an account associated with that email')
            return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

        create_library(user.id)
        create_recents(user.id)

        print(re_interests)
        add_interests_to_researcher(re_interests, user.id)

        if image:
            image_url = uploadFile(user.id, image[0])
            remove(f"App/uploads/{image[0]}")
            builder.image_url(image_url)
            builder.build()

        if isinstance(current_user, User):
            logout_user()
        login_user(user, False)
        flash('You successfully created your account')

        return redirect(url_for('.index_page'))
    return render_template('signup.html', baseForm=baseForm, reForm=reForm, interests=interests)

@index_views.route('/addpublication', methods=['GET'])
def add_publication():
    return render_template('addpublication.html')

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

@index_views.route('/addtolibrary/<user_id>/<pub_id>', methods=['GET'])
def add_to_library(user_id, pub_id):
    library = get_library_from_user(user_id)
    if add_publication_to_library(library, pub_id):
        return True
    remove_publication_from_library(library, pub_id)
    return False

@index_views.route('/addtorecents/<user_id>/<pub_id>', methods=['GET'])
def add_to_recent(user_id, pub_id):
    recents = get_recents_from_user(user_id)
    if add_publication_to_recents(recents, pub_id):
        return True
    remove_publication_from_recents(recents, pub_id)
    return False

@index_views.route('/publication/addread/<id>', methods=['GET'])
def add_read(id):
    pub = get_pub_byid(id)
    add_read_to_pub(pub)
    return 'Added'

@index_views.route('/publication/adddownload/<id>', methods=['GET'])
def add_download(id):
    pub = get_pub_byid(id)
    add_download_to_pub(pub)
    return 'Added'

@index_views.route('/publication/addcitation/<id>', methods=['GET'])
def add_citation(id):
    pub = get_pub_byid(id)
    add_citation_to_pub(pub)
    request = f"Generate a Chicago style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation  = prompt(request)["choices"][0]["text"]
    return citation

@index_views.route('/publication/addsearch/<id>', methods=['GET'])
def add_search_pub(id):
    pub = get_pub_byid(id)
    add_search_to_pub(pub)
    return 'Added'

@index_views.route('/profile/addsearch/<id>', methods=['GET'])
def add_search_re(id):
    re = get_researcher(id)
    add_search(re)
    return 'Added'

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
        pubs = get_all_publications_for_user(user)
        subs = len(user.sub_records.all())
        interests = get_research_topics(user)
        skills = [user.skills]
        if ',' in user.skills:
            skills = user.skills.split(', ')
        if '\n' in user.skills:
            skills = user.skills.split('\n')
        if ',\n' in user.skills:
            skills = user.skills.split(',\n')

        if (isinstance(current_user, User)) and (current_user.id is not user.id):
            vrec = get_visit_record(current_user.id, user.id)

            if not vrec:
                vrec = create_visit_record(current_user.id, user.id)

            if update_visit_record(vrec):
                add_view(user)

    return render_template('profile.html', user=user, re=re, pubs=pubs, subs=subs, topics=topics, library=library, recents=recents, researchers=researchers, interests=interests, skills=skills)


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

@index_views.route('/update', methods=['GET'])
def scholarly_update():
    users = get_all_researchers()
    for n in range(len(users), 0, -1):
        user = users[n-1]
        pubs = get_pubs(user.first_name, user.last_name)
        print(user.first_name, user.last_name)
        for i in range(len(pubs)):
            p = get_pub_containing_title(pubs[i]['bib']['title'].strip().lower())
            if not p:
                print(pubs[i]['bib']['title'].strip().lower())
                print(p)
                pub = fill_pub(pubs[i], user.first_name, user.last_name)
                if pub:
                    print('Adding authors')
                    data = {}
                    data['title'] = pub['bib']['title'].lower()
                    data['abstract'] = pub['bib']['abstract']
                    data['eprint'] = ''
                    if 'pub_url' in pub:
                        data['url'] = pub['pub_url']
                    if 'eprint_url' in pub:
                        if 'pdf' in pub['eprint_url'][-18:]:
                            data['free_access'] = True
                        else:
                            data['free_access'] = False
                        data['eprint'] = pub['eprint_url']
                    else:
                        if 'pub_url' in pub and 'pdf' in pub['pub_url'][-18:]:
                            data['free_access'] = True
                        else:
                            data['free_access'] = False
                    if (pub['bib']['pub_type'] == 'inproceedings') or (pub['bib']['pub_type'] == 'proceedings') or (pub['bib']['pub_type'] == 'conference'):
                        data['pub_type'] = 'conference paper'
                    else:
                        data['pub_type'] = pub['bib']['pub_type'].lower()
                    
                    if pub['bib']['pub_year'] == 'NA':
                        data['publication_date'] = datetime.date(datetime.strptime('01/01/0001', '%d/%m/%Y'))
                    else:
                        data['publication_date'] = datetime.date(datetime.strptime(pub['bib']['pub_year'], '%Y'))
                    
                    p = create_pub(data)
                    if p:
                        authors = pub['bib']['author'].split(' and ')
                        temp = []
                        for author in authors:
                            temp.append(author.split(', '))
                        authors = temp
                        temp = []
                        for author in authors:
                            if not (user.first_name in author and user.last_name in author):
                                author.reverse()
                                temp.append(' '.join(author))
                        authors = temp
                        for re in users:
                            target = []
                            for co in authors:
                                if re.first_name in co and re.last_name in co:
                                    target.append(authors.index(co))
                            for t in target:
                                print(add_publication_to_researcher(re.id, p.id))
                                authors.remove(authors[t])
                        authors = ', '.join(authors)

                        add_coauthors(p, authors)
                        print(add_publication_to_researcher(user.id, p.id))
                        print(p.id)

    return 'Created'


@index_views.route('/test', methods=['GET'])
def test():
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

    for n in range(1, 3):
        pub = get_pub_byid(n)
        print('\n',pub.bibtex)
        request = f"Generate a Chicago style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
        citation  = prompt(request)["choices"][0]["text"]
        print(citation)

    print('\n\nDONE\n\n')

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
    