from App.database import db
from App.models import Topic, Researcher,Publication


def parse_search(terms):
    data = {}
    name = {}
    content = ['name', 'title', 'keyword']
    words = terms.split(" ")

    for word in words:
        word = word.strip()
        if any(char.isdigit() for char in word):
            data['date'] = int(word)
        
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
        
        return search_branch(data, content)

def search_branch(search_params,content):
    for c in content:
        if c == "name":
            return author_search(search_params)
        if c == "title":
            return title_search(search_params)
        if c == "keyword":
            return keyword_search(search_params)

def researcher_search(search_params): #returns a list of researchers with the same name
    try:
        base = Researcher.query
        if "first_name" in data["name"]:
            base = base.filter_by(first_name =search_params["name"]["first_name"])
        if "last_name" in data["name"]:
            base =  base.filter_by(last_name = search_params["name"]["last_name"])

        return base.all()
    except e:
        return [] 

def title_search(search_params):
    try:
        results = Publication.query.filter_by(title = Publication.title.like(search_params['title'] + "%") )
        if "date" in search_params:
            results = results.filter_by(publication_date = search_params["date"])
        return results.all()
    except e:
        return []

def author_search(search_params):
    results = []
    try:
        base_researcher = Researcher.query
        if "first_name" in data["name"]:
            base_researcher = base_researcher.filter_by(first_name =search_params["name"]["first_name"])
        if "last_name" in data["name"]:
            base_researcher =  base_researcher.filter_by(last_name = search_params["name"]["last_name"])
        base_researcher = base_researcher.all()
        for auth in base_researcher:
            pubs = Publication.query.filter(Publication.pub_records.has(researcher_id=auth.id))
            pubs = pubs.filter_by(publication_date=search_params["date"]).all()
            if len(pubs) != 0:
                results.append(pubs)
        return results
    except e:
        return []

def keyword_search(search_params):
    try:
        topic = Topic.query.filter_by(name=search_params['topic']).first()
        pubs = Publication.query.filter(Publication.tags.has(topic_id=topic.id))
        if "date" in search_params:
            pubs = pubs.filter_by(publication_date=search_params['date'])
        return pubs.all()
    except e:
        return []



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