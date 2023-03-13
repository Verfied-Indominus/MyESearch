from App.models.researcher import Researcher
from App.models.publication import Publication

def search(phrase):
    pub_results = []
    author_results = []

    # check if numbers in phrase
    nums = [int(num) for num in phrase if num.isdigit()]
    

    # check first if title is searched
    results = Publication.query.filter_by(title=phrase.lower()).first()
    if results:
        pub_results.append(results)

    # check if portion of title is searched
    results = Publication.query.filter(Publication.title.like(phrase.lower())).all()
    if results:
        pub_results.extend(results)