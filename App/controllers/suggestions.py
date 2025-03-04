from App.controllers.publication import get_all_publications
from App.controllers.researcher import get_researcher
from App.controllers.topic import get_all_topics, get_topic
from App.models.researcher import Researcher
from App.models.publication import Publication
from random import shuffle

global all_publications, all_topics

# Need to figure out what pubs will be shown and where
# 1st. on home page:
        # if user logged in
        # pull random pubs from any researchers or topics subscribed to (1st priority)
            # if user not subscribed to anything:
            # pull random pubs from researchers that may be in same faculty or same department
            # department has priority over faculty

        # if not logged in:
        # pull pubs that have highest number of reads, then downloads, then citations, then searches

# 2nd. on publication page:
        # pull other pubs by the same author(s) first
        # then pubs of the same topic(s)
        # if user reaches near the end of list then pull same pubs as if user not logged in

def get_home_suggestions(user):
    pubs = []
    re_pubs = []
    top_pubs = []
    for rec in user.researcher_sub_records:
        re_pubs = get_researcher_pubs(rec.subject.id)

    for rec in user.topic_sub_records:
        top_pubs = get_topic_pubs(rec.subject.id)

    if not (re_pubs and top_pubs):
        researchers = []
        re_faculty = Researcher.query.filter_by(faculty=user.faculty).limit(10)
        if re_faculty:
            researchers.extend(re_faculty)
            re_department = Researcher.query.filter_by(department=user.department).limit(20)
            for re in re_department:
                if re not in researchers:
                    researchers.append(re)

        if researchers:
            for re in researchers:
                re_pubs.extend(get_researcher_pubs(re.id))
        
        pubs.extend(re_pubs)

    else:
        pubs.extend(re_pubs)
        pubs.extend(top_pubs)

    pubs.extend(get_ranked_pubs())
    pubs = list(set(pubs))
    shuffle(pubs)

    return pubs

def get_publication_suggestions(pub):
    pubs = []
    researchers = []
    topics = []

    global all_publications, all_topics
    all_publications = get_all_publications()
    all_topics = get_all_topics()

    if not pub:
        return researchers, topics, pubs
    
    for rec in pub.pub_records:
        researchers.extend(get_researcher_pubs(rec.researcher.id))
    for tag in pub.tags:
        top_id = tag.topic.id
        tops = get_topic_pubs(top_id)
        topics.extend(tops)
    topics = list(set(topics))
    pubs = get_ranked_pubs()

    researchers.sort(key=lambda pub: pub.publication_date, reverse=True)
    topics.sort(key=lambda pub: pub.publication_date, reverse=True)
    pubs.sort(key=lambda pub: pub.publication_date, reverse=True)

    return researchers, topics, pubs

def get_researcher_pubs(id):
    re = get_researcher(id)
    records = re.pub_records.all()
    shuffle(records)
    return [rec.publication for rec in records[:20]]

def get_topic_pubs(id):
    topic = get_topic(id)
    tags = topic.pub_tags.all()
    shuffle(tags)
    return [tag.publication for tag in tags[:20]]

def get_ranked_pubs():
    ranked_pubs = []

    global all_publications

    all_publications.sort(key=lambda pub: pub.reads, reverse=True)
    ranked_pubs.extend(all_publications[:10])

    all_publications.sort(key=lambda pub: pub.citations, reverse=True)
    ranked_pubs.extend(all_publications[:10])

    all_publications.sort(key=lambda pub: pub.searches, reverse=True)
    ranked_pubs.extend(all_publications[:10])

    ranked_pubs = list(set(ranked_pubs))
    return ranked_pubs
    