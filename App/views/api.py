import ast
from datetime import datetime
import io
import json
import os
from random import shuffle
from flask import Blueprint, send_file, send_from_directory
from App.controllers.library import add_publication_to_library, get_library_from_user, remove_publication_from_library
from App.controllers.notification import accept, delete_all_notif_recs, follow_back_researcher, reject, set_notif_rec_read, verified_notif, verify_author_notif
from App.controllers.open_ai import prompt
from App.controllers.edenai import ai_prompt
from App.controllers.pdf import decrypt_pdf_from_url
from App.controllers.publication import add_citation_to_pub, add_coauthors, add_download_to_pub, add_read_to_pub, add_search_to_pub, add_topic_to_pub, create_pub, get_all_publications, get_all_publications_json, get_pub_byid, get_pub_containing_title, set_pub_bibtex, set_pub_type
from App.controllers.pubrecord import add_pub_record
from App.controllers.recents import add_publication_to_recents, get_recents_from_user
from App.controllers.researcher import add_search, add_view, get_all_researchers, get_all_researchers_verified, get_researcher, reSubscribe, reUnsubscribe
from App.controllers.scholarly_py import fill_pub, get_pubs, search_pub_title
from App.controllers.suggestions import get_publication_suggestions
from App.controllers.topic import create_topic, get_all_topics, get_topic, get_topic_by_name, set_topic_parent, topSubscribe, topUnsubscribe
from App.controllers.user import get_user
from App.controllers.verify import verified

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/load/publications', methods=['GET'])
def load_publications():
    publications = get_all_publications_json() 
    publications.sort(key=lambda pub: pub['publication_date'], reverse=True)
    return publications

@api_views.route('/load/researchers', methods=['GET'])
def load_researchers():
    researchers = get_all_researchers_verified()
    shuffle(researchers)
    return [re.toDict() for re in researchers]

@api_views.route('/load/pubsuggestions/<id>', methods=['GET'])
def load_pub_suggestions(id):
    pub = get_pub_byid(id)
    
    publications = get_all_publications_json() 

    researchers, topics, pubs = get_publication_suggestions(pub)

    pubs = [p.toDict() for p in pubs]
    topics = [t.toDict() for t in topics] 
    researchers = [r.toDict() for r in researchers]

    return [researchers, topics, pubs]

@api_views.route('/addtolibrary/<user_id>/<pub_id>', methods=['GET'])
def add_to_library(user_id, pub_id):
    library = get_library_from_user(user_id)
    if add_publication_to_library(library, int(pub_id)):
        return {'text': 'In Library'}
    remove_publication_from_library(library, int(pub_id))
    return {'text': 'Add to Library'}

@api_views.route('/removefromlibrary/<user_id>/<pub_id>', methods=['GET'])
def remove_from_library(user_id, pub_id):
    library = get_library_from_user(user_id)
    remove_publication_from_library(library, int(pub_id))
    return 'Removed'

@api_views.route('/addtorecents/<user_id>/<pub_id>', methods=['GET'])
def add_to_recent(user_id, pub_id):
    recents = get_recents_from_user(user_id)
    add_publication_to_recents(recents, int(pub_id))
    return 'Added'

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

    if not pub.bibtex:
        return {'citation': "No Citation information was specified"}

    add_citation_to_pub(pub)

    citation = []
    request = f"Generate a Chicago-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

    request = f"Generate a APA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

    request = f"Generate a MLA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

    return {'citation': citation}

@api_views.route('/publication/getcitation/<id>', methods=['GET'])
def get_citation(id):
    pub = get_pub_byid(id)

    if not pub.bibtex:
        return {'citation': "No Citation information was specified"}

    citation = []
    request = f"Generate a Chicago-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

    request = f"Generate a APA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

    request = f"Generate a MLA-style bibliography citation from the following dict: '{json.loads(pub.bibtex)}'"
    # citation.append(prompt(request)["choices"][0]["text"])
    citation.append(ai_prompt(request))

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
    all_publications = get_all_publications()
    for publication in all_publications:
        if len(publication.tags.all()) == 0:
            abstract = publication.abstract
            request = f"Extract the main topics pertaining to Computer Science from the following text as a python list: '{abstract}'"
            # keywords  = prompt(request)["choices"][0]["text"]
            keywords  = ai_prompt(request)
            # print(keywords)
            keywords = '[' + keywords.split('[')[1]
            keywords = keywords.split(']')[0] + ']'
            print(keywords)
            keywords = ast.literal_eval(node_or_string=keywords.strip())
            for key in keywords:
                topic = get_topic_by_name(key.title())
                if not topic and len(key) < 60:
                    topic = create_topic(key.title())
                    for top in get_all_topics():
                        if top.name in topic.name:
                            set_topic_parent(topic.name, top.id)
                        if topic.name in top.name:
                            set_topic_parent(top.name, topic.id)
                if topic:
                    added = add_topic_to_pub(publication, topic)
                    if not added:
                        print('\nNOT ADDED\n') 
                        print(publication.title)
                        print(topic.name)
                        print('\n')
            print(keywords)
            print([tag.topic.name for tag in publication.tags.all()])

        if publication.bibtex and 'Patent' in publication.bibtex:
            set_pub_type(publication, 'patent')
        if not publication.bibtex:
            print(publication.title, '\n')
            bibtex = search_pub_title(publication)
            if bibtex:
                items = []
                bibtex = bibtex.split(sep='{', maxsplit=1)[1].split(sep=',\n ', maxsplit=1)[1]
                bibtex = bibtex[:-3]
                items.extend([item.strip() for item in bibtex.split(',\n')])
                items.pop(0)
                bibtex = {}
                for item in items:
                    bibtex[item.split('=')[0].strip()] = item.split('=')[1].strip().strip('}{')
                bibtex = json.dumps(bibtex)
                set_pub_bibtex(publication, bibtex)
                if 'Patent' in publication.bibtex:
                    set_pub_type(publication, 'patent')
                print(publication.bibtex)
                print(publication.id)
                print('\n\n')
            else:
                print('\nNot Found\n')


    researchers = get_all_researchers()
    for n in range(len(researchers), 0, -1): 
        user = researchers[n-1]
        pubs = get_pubs(user.first_name, user.last_name)
        print(user.first_name, user.last_name)
        for i in range(len(pubs)):
            p = get_pub_containing_title(pubs[i]['bib']['title'].strip().lower())
            if not p:
                print(pubs[i]['bib']['title'].strip().lower())
                pub = fill_pub(pubs[i], user.first_name, user.last_name)
                if pub:
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
                    print(p)
                    if p:
                        print('Adding authors')
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
                        for re in researchers:
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
                        print('pub id', p.id)
                        print(p.toDict())
                        abstract = p.abstract
                        request = f"Extract the main topics pertaining to Computer Science from the following text as a python list: '{abstract}'"
                        # keywords  = prompt(request)["choices"][0]["text"]
                        keywords  = ai_prompt(request)
                        print(keywords)
                        keywords = '[' + keywords.split('[')[1]
                        keywords = ast.literal_eval(node_or_string=keywords.strip())
                        for key in keywords:
                            topic = get_topic_by_name(key.title())
                            if not topic and len(key) < 60:
                                topic = create_topic(key.title())
                                for top in get_all_topics():
                                    if top.name in topic.name:
                                        set_topic_parent(topic.name, top.id)
                                    if topic.name in top.name:
                                        set_topic_parent(top.name, topic.id)
                            if topic:
                                added = add_topic_to_pub(p, topic)
                                if not added:
                                    print('\nNOT ADDED\n') 
                                    print(p.title)
                                    print(topic.name)
                                    print('\n')
                        print('\n\n', abstract)
                        print(keywords)
                        print([tag.topic.name for tag in p.tags.all()])

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
    res = verified(new_auth_id)
    print(res)
    if res:
        res = verified_notif(new_auth_id, auth_id)
        if res:
            return '200'
        else:
            return '300'
    return '300'

@api_views.route('/accept/<s_id>/<pub_id>', methods=['GET'])
def accept_request(s_id, pub_id):
    print(accept(s_id, pub_id))
    return 'Accepted'

@api_views.route('/reject/<s_id>/<pub_id>', methods=['GET'])
def reject_request(s_id, pub_id):
    reject(s_id, pub_id)
    return 'Rejected'

@api_views.route('/subscribe/researcher/<sub_id>/<re_id>', methods=['GET'])
def re_follow(sub_id, re_id):
    re = get_researcher(re_id)
    if not reSubscribe(sub_id, re_id):
        reUnsubscribe(sub_id, re_id)
        return {'text': f'<a onclick="reSubscribe(this, {sub_id}, {re_id}, `{re.title} {re.first_name} {re.last_name}`);" class="uk-icon-button uk-background-secondary" uk-icon="plus"></a><span class="uk-width-small uk-transition-fade"> Subscribe</span>'}
    return {'text': f' <a onclick="reSubscribe(this, {sub_id}, {re_id}, `{re.title} {re.first_name} {re.last_name}`);" class="uk-icon-button uk-background-secondary" uk-icon="check"></a><span class="uk-width-small uk-transition-fade"> Subscribed</span>'}

@api_views.route('/subscribe/topic/<sub_id>/<top_id>', methods=['GET'])
def top_follow(sub_id, top_id):
    topic = get_topic(top_id)
    if not topSubscribe(sub_id, top_id):
        topUnsubscribe(sub_id, top_id) 
        return {'text': f'<a onclick="topSubscribe(this, {sub_id}, {top_id}, `{topic.name}`);" class="uk-icon-button uk-background-secondary" uk-icon="plus"></a><span class="uk-width-auto uk-transition-fade"> Subscribe</span>'}
    return {'text': f'<a onclick="topSubscribe(this, {sub_id}, {top_id}, `{topic.name}`);" class="uk-icon-button uk-background-secondary" uk-icon="check"></a><span class="uk-width-auto uk-transition-fade"> Subscribed</span>'}

@api_views.route('/followback/<re_id>/<sub_id>', methods=['GET'])
def follow_back(re_id, sub_id):
    follow_back_researcher(re_id, sub_id)
    return "Followed"

@api_views.route('/getPDF/<pub_id>', methods=['GET'])
def get_encrypted_pdf(pub_id):
    pub = get_pub_byid(pub_id)
    filename = decrypt_pdf_from_url(pub.encryptedPDF)

    return_data = io.BytesIO()
    with open(f"App/{filename}", "rb") as file:
        return_data.write(file.read())

    return_data.seek(0)
    os.remove(f"App/{filename}")

    name = pub.title
    name = name.title()

    return send_file(return_data, "application/pdf", True, f"{name}.pdf")