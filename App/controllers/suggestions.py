from App.controllers.researcher import get_researcher
from App.controllers.topic import get_topic
from App.models.researcher import Researcher
from App.models.publication import Publication
from random import shuffle


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

    if not pub:
        return researchers, topics, pubs

    for rec in pub.pub_records:
        researchers.extend(get_researcher_pubs(rec.researcher.id))
    for tag in pub.tags:
        topics.extend(get_topic_pubs(tag.topic.id))
    
    pubs = get_ranked_pubs()
    shuffle(pubs)
    shuffle(researchers)
    shuffle(topics)

    return researchers, topics, pubs

def get_researcher_pubs(id):
    re = get_researcher(id)
    # re_pubs = []
    # for rec in re.pub_records:
    #     re_pubs.append(rec.publication)   
    # return re_pubs     
    return [rec.publication for rec in re.pub_records.all()]

def get_topic_pubs(id):
    topic = get_topic(id)
    top_pubs = []
    for tag in topic.pub_tags:
        top_pubs.append(tag.publication)
    return top_pubs

def get_ranked_pubs():
    ranked_pubs = []
    reads = Publication.query.order_by(Publication.reads.desc()).limit(10)
    citations = Publication.query.order_by(Publication.citations.desc()).limit(10)
    searches = Publication.query.order_by(Publication.searches.desc()).limit(10)

    ranked_pubs.extend(reads)
    ranked_pubs.extend(citations)
    ranked_pubs.extend(searches)

    ranked_pubs = list(set(ranked_pubs))

    return ranked_pubs
    