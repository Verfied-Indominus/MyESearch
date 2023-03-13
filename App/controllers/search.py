from App.database import db
from App.models import Topic, Researcher,Publication
from datetime import datetime
from sqlalchemy import extract


def parse_search(search_terms):
    authors = []
    publications = []
    topics = []
    terms = search_terms.split(" ")

    nums = [int(num.strip()) for num in terms if num.isdigit()]
    words = [word.strip() for word in terms if not word.isdigit()]

    result = Publication.query.get(19)
    print(result.title)
    print(search_terms)
    print(search_terms in result.title)
    result = Publication.query.filter(Publication.title.like(search_terms.lower())).all()
    if result:
        publications.extend(result)

    for num in nums:
        result = Publication.query.filter(extract('year', Publication.publication_date) == datetime.date(datetime.strptime(f"{num}-1-1", "%Y-%m-%d")).year).all()
        if result:
            publications.extend([pub for pub in result if pub not in publications])

    length = len(words)
    for n in range(0, length, 2):
        if n+2 <= length:
            result = Researcher.query.filter_by(first_name=f"{words[n]}".title(), last_name=f"{words[n+1]}".title()).first()
            if result:
                authors.append(result)
                publications.extend([rec.publication for rec in result.pub_records.all() if rec.publication not in publications])
            
            result = Topic.query.filter_by(name=f"{words[n]} {words[n+1]}".title()).first()
            if result:
                topics.append(result)
                authors.extend([rec.researcher for rec in result.researcher_tags.all() if rec.researcher not in authors])
                publications.extend([rec.publication for rec in result.pub_tags.all() if rec.publication not in publications])

            result = Publication.query.filter(Publication.title.like(f"{words[n]} {words[n+1]}".lower())).all()
            if result:
                publications.extend([pub for pub in result if pub not in publications])

    for word in words:
        result = Topic.query.filter(Topic.name.like(word.title())).all()
        if result:
            topics.extend([topic for topic in result if topic not in topics])

        result = Publication.query.filter(Publication.title.like(word.lower())).all()
        if result:
            publications.extend([pub for pub in result if pub not in publications])
        
    return authors, publications, topics 

    # for word in words:
    #     word = word.strip()
    #     if any(char.isdigit() for char in word):
    #         data['date'] = int(word)
        
        # if word.count(" ") == 1: # definietly a name
        #     content["name"] = True
        #     name = word.split(" ")
        #     for n in name:
        #         if Researcher.query.filter_by(first_name=n.capitalize()).first() is not None:
        #             name['first_name']= n.capitalize()
        #         if Researcher.query.filter_by( last_name=n.capitalize()).first() is not None:
        #             name['last_name']= n.capitalize()

        # if word.count(" ") > 1: # most likely a title
        #     content["title"] = True
        #     if Publication.query.filter_by(title=Publication.title.like(word + "%")).all() is not []:
        #         data["title"] = word
    
        # if Topic.query.filter_by(name=word.capitalize()).first() is not None:
        #     content["topic"] = True
        #     data["topic"] = word

        # if Researcher.query.filter_by(first_name=word.capitalize()).first() is not None:
        #     content["name"] = True
        #     name['first_name'] = word
        
        # if Researcher.query.filter_by(last_name=word.capitalize()).first() is not None:
        #     content["name"] = True
        #     name['last_name'] = word

        # if name != {}:
        #     data["name"] = name
        
        # return search_branch(data, content)

# def search_branch(search_params,content):
#     for c in content:
#         if c == "name":
#             return author_search(search_params)
#         if c == "title":
#             return title_search(search_params)
#         if c == "keyword":
#             return keyword_search(search_params)

# def researcher_search(search_params): #returns a list of researchers with the same name
#     try:
#         base = Researcher.query
#         if "first_name" in data["name"]:
#             base = base.filter_by(first_name =search_params["name"]["first_name"])
#         if "last_name" in data["name"]:
#             base =  base.filter_by(last_name = search_params["name"]["last_name"])

#         return base.all()
#     except e:
#         return [] 

# def title_search(search_params):
#     try:
#         results = Publication.query.filter_by(title = Publication.title.like(search_params['title'] + "%") )
#         if "date" in search_params:
#             results = results.filter_by(publication_date = search_params["date"])
#         return results.all()
#     except e:
#         return []

# def author_search(search_params):
#     results = []
#     try:
#         base_researcher = Researcher.query
#         if "first_name" in data["name"]:
#             base_researcher = base_researcher.filter_by(first_name =search_params["name"]["first_name"])
#         if "last_name" in data["name"]:
#             base_researcher =  base_researcher.filter_by(last_name = search_params["name"]["last_name"])
#         base_researcher = base_researcher.all()
#         for auth in base_researcher:
#             pubs = Publication.query.filter(Publication.pub_records.has(researcher_id=auth.id))
#             pubs = pubs.filter_by(publication_date=search_params["date"]).all()
#             if len(pubs) != 0:
#                 results.append(pubs)
#         return results
#     except e:
#         return []

# def keyword_search(search_params):
#     try:
#         topic = Topic.query.filter_by(name=search_params['topic']).first()
#         pubs = Publication.query.filter(Publication.tags.has(topic_id=topic.id))
#         if "date" in search_params:
#             pubs = pubs.filter_by(publication_date=search_params['date'])
#         return pubs.all()
#     except e:
#         return []



# def publication_search(data):
#  #for search bar use title, year/ author,year / keyword,year
    # limit search parms to 2 in csv form
    # search_form =  {
    #     "name": {
    #         "first_name" : first,
    #         "last_name": last
    #     },
    #     "title": title,
    #     "keyword": keyword,
    #     "year": year
    # }
    # try:
    #     # pubs  = Publicaton.query
    #     results = []
    #     for key,value in data.items():
    #         if key == "name" and value is not None:
    #             auth = Researcher.query.filter_by(first_name = value['first_name'])
    #             auth = auth.filter_by(value['last_name']).all()
    #             for a in auth:
    #                 results.append(Publication.query.filter_by(pubrecords.researcher_id==a.id))
    #         if key == "title":
    #             results = Publiation.query.filter_by(title=title)
    #         if key == "keyword":
                
    #         if key == "year":
    #             for key,value in results.items():
    #                 results[key] = value.filter_by(publication_date=data["year"]).all()

    #     return results
    # except e:
    #     return None

# from App.models.researcher import Researcher
# from App.models.publication import Publication

# def search(phrase):
#     pub_results = []
#     author_results = []

#     # check if numbers in phrase
#     nums = [int(num) for num in phrase if num.isdigit()]
    

#     # check first if title is searched
#     results = Publication.query.filter_by(title=phrase.lower()).first()
#     if results:
#         pub_results.append(results)

#     # check if portion of title is searched
#     results = Publication.query.filter(Publication.title.like(phrase.lower())).all()
#     if results:
#         pub_results.extend(results)