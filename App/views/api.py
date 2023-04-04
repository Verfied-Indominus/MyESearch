from datetime import datetime
import json
from random import shuffle
from flask import Blueprint
from App.controllers.library import add_publication_to_library, get_library_from_user, remove_publication_from_library
from App.controllers.notification import accept, delete_all_notif_recs, follow_back_researcher, reject, set_notif_rec_read, verified_notif, verify_author_notif
from App.controllers.open_ai import prompt
from App.controllers.publication import add_citation_to_pub, add_coauthors, add_download_to_pub, add_read_to_pub, add_search_to_pub, create_pub, get_all_publications, get_pub_byid, get_pub_containing_title
from App.controllers.pubrecord import add_pub_record
from App.controllers.recents import add_publication_to_recents, get_recents_from_user, remove_publication_from_recents
from App.controllers.researcher import add_search, add_view, get_all_researchers, get_researcher
from App.controllers.scholarly_py import fill_pub, get_pubs
from App.controllers.suggestions import get_publication_suggestions
from App.controllers.user import get_user
from App.controllers.verify import verified

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/load/publications', methods=['GET'])
def load_publications():
    publications = get_all_publications()
    publications = [pub.toDict() for pub in publications]
    publications.sort(key=lambda pub: pub['publication_date'], reverse=True)
    return publications

@api_views.route('/load/researchers', methods=['GET'])
def load_researchers():
    researchers = get_all_researchers()
    shuffle(researchers)
    return [re.toDict() for re in researchers]

@api_views.route('/load/pubsuggestions/<id>', methods=['GET'])
def load_pub_suggestions(id):
    pub = get_pub_byid(id)
    researchers, topics, pubs = get_publication_suggestions(pub)
    return [[r.toDict() for r in researchers if r], [t.toDict() for t in topics if t], [p.toDict() for p in pubs if p]]

@api_views.route('/addtolibrary/<user_id>/<pub_id>', methods=['GET'])
def add_to_library(user_id, pub_id):
    library = get_library_from_user(user_id)
    if add_publication_to_library(library, pub_id):
        return True
    remove_publication_from_library(library, pub_id)
    return False

@api_views.route('/addtorecents/<user_id>/<pub_id>', methods=['GET'])
def add_to_recent(user_id, pub_id):
    recents = get_recents_from_user(user_id)
    if add_publication_to_recents(recents, pub_id):
        return True
    remove_publication_from_recents(recents, pub_id)
    return False

@api_views.route('/publication/addread/<id>', methods=['GET'])
def add_read(id):
    pub = get_pub_byid(id)
    add_read_to_pub(pub)
    return 'Added'

@api_views.route('/publication/adddownload/<id>', methods=['GET'])
def add_download(id):
    pub = get_pub_byid(id)
    add_download_to_pub(pub)
    return 'Added' 

@api_views.route('/publication/addcitation/<id>', methods=['GET'])
def add_citation(id):
    pub = get_pub_byid(id)
    add_citation_to_pub(pub)
    citation = []
    request = f"Generate a Chicago-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    request = f"Generate a APA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    request = f"Generate a MLA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    return {'citation': citation}

@api_views.route('/publication/getcitation/<id>', methods=['GET'])
def get_citation(id):
    pub = get_pub_byid(id)
    citation = []
    request = f"Generate a Chicago-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    request = f"Generate a APA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    request = f"Generate a MLA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    citation.append(prompt(request)["choices"][0]["text"])

    return {'citation': citation}

@api_views.route('/publication/addsearch/<id>', methods=['GET'])
def add_search_pub(id):
    pub = get_pub_byid(id)
    add_search_to_pub(pub)
    return 'Added'

@api_views.route('/profile/addview/<id>', methods=['GET'])
def add_view_re(id):
    re = get_researcher(id)
    add_view(re)
    return 'Added'

@api_views.route('/profile/addsearch/<id>', methods=['GET'])
def add_search_re(id):
    re = get_researcher(id)
    add_search(re)
    return 'Added'

@api_views.route('/load/profilepubs/<id>', methods=['GET'])
def load_profile_pubs(id):
    re = get_researcher(id)
    publications = get_all_publications()
    pubs = [rec.publication.toDict() for rec in re.pub_records]
    pubs.sort(key=lambda pub: pub['publication_date'], reverse=True)
    return pubs

@api_views.route('/update', methods=['GET'])
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
                                print(add_pub_record(re.id, p.id))
                                authors.remove(authors[t])
                        authors = ', '.join(authors)

                        add_coauthors(p, authors)
                        print(add_pub_record(user.id, p.id))
                        print(p.id)

    return 'Created'

@api_views.route('/clear/notifications/<user_id>', methods=['GET'])
def clear_notifs(user_id):
    user = get_user(user_id)
    delete_all_notif_recs(user)
    return 'Cleared'

@api_views.route('/setread/<notif_rec_id>', methods=['GET'])
def setread(notif_rec_id):
    set_notif_rec_read(notif_rec_id) 
    return 'Read'

@api_views.route("/verify/<auth_id>/<new_auth_id>", methods=['GET'])
def verify(auth_id, new_auth_id):
    res = verified(auth_id)
    if res:
        res = verified_notif(new_auth_id, auth_id)
        if res:
            return 200
        else:
            return 300
    return 300

@api_views.route("/verify/notification/<auth_id>/<new_auth_id>", methods=['GET'])
def verify_notif(auth_id, new_auth_id):
    auth = get_researcher(new_auth_id)
    verifier = get_researcher(auth_id)
    verify_author_notif(auth, verifier)
    res = verified(auth_id)
    if res:
        res = verified_notif(new_auth_id, auth_id)
        if res:
            return 200
        else:
            return 300
    return 300

@api_views.route('/accept/<s_id>/<pub_id>', methods=['GET'])
def accept_request(s_id, pub_id):
        accept(s_id, pub_id)
        return 'Accepted'

@api_views.route('/reject/<s_id>/<pub_id>', methods=['GET'])
def reject_request(s_id, pub_id):
        reject(s_id, pub_id)
        return 'Rejected'

@api_views.route('/followback/<re_id>/<sub_id>', methods=['GET'])
def follow_back(re_id, sub_id):
    follow_back_researcher(re_id, sub_id)
    return "Followed"