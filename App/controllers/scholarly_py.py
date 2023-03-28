from scholarly import scholarly, ProxyGenerator
# from open_ai import prompt

pg = ProxyGenerator()

def set_new_proxy():
    while True:
        success = pg.FreeProxies()
        if success:
            scholarly.use_proxy(pg, pg)
            break

def get_pub_query(fname, lname):
    set_new_proxy()
    while True:
        try:
            pub_query = scholarly.search_pubs_custom_url(f'/scholar?as_vis=1&q=author:"{fname}+{lname}"')
            break
        except Exception:
            set_new_proxy()
    return pub_query

def get_author(fname, lname):
    while True:
        try:
            search_query = scholarly.search_author(f'{fname} {lname}')
            break
        except Exception:
            set_new_proxy()

    try:
        author = next(search_query)
        author = scholarly.fill(author)
        return author
    except Exception:
        return None

def get_pubs(fname, lname):
    pubs = []

    author = get_author(fname, lname)
    if author:
        return author['publications']
    
    pub_query = get_pub_query(fname, lname)
    while True:
        try:
            for pub in pub_query:
                pubs.append(pub)
            break
        except Exception:
            set_new_proxy()
    return pubs

def search_pub(pub, fname, lname):
    while True:
        try:
            pub = scholarly.search_pubs(query='allintitle: "{}" author: "{} {}"'.format(pub['bib']['title'], fname, lname), citations=False)
            break
        except Exception:
            set_new_proxy()
            print('search')
    return pub

def search_pub_again(pub, fname, lname):
    while True:
        try:
            pub = scholarly.search_pubs(query='allintitle: "{}"'.format(pub['bib']['title']), citations=False)
            break
        except Exception:
            set_new_proxy()
            print('search again')
    return pub


def fill_pub(pub, fname, lname):
    pub1 = search_pub(pub, fname, lname)
    try:
        pub1 = next(pub1)
    except Exception:
        pub1 = search_pub_again(pub, fname, lname)
        try:
            pub1 = next(pub1)
        except Exception:
            return None
    while True:
        try:
            fill = scholarly.fill(pub1)
            break
        except Exception:
            set_new_proxy()
            print('fill')
    return fill

def get_shortened_name(name):
    name = name.split(' ')
    if len(name) == 2:
        name = "{} {}".format(name[0][0], name[1])
    elif len(name) == 3:
        name = "{}{} {}".format(name[0][0], name[1][0], name[2])
    return name


# to get citations
def search_pub_title(pub):
    set_new_proxy()
    found = True
    while True:
        try:
            pub1 = scholarly.search_pubs(query='allintitle:"{}" author:"{} {}"'.format(pub.title, pub.pub_records.first().researcher.first_name, pub.pub_records.first().researcher.last_name), citations=False)
            break
        except Exception:
            set_new_proxy()
            print('search title and author')
    while True:
        try:
            pub1 = next(pub1)
            break
        except Exception as e:
            set_new_proxy()
            print('next pub')
            if isinstance(e, StopIteration):
                found = False
                break
    if not found:
        while True:
            try:
                pub1 = scholarly.search_pubs(query='allintitle:"{}" author: "{} {}"'.format(pub.title, pub.pub_records.first().researcher.first_name, pub.pub_records.first().researcher.last_name), citations=False)
                break
            except Exception:
                set_new_proxy() 
                print('search title and author again') 
        while True:
            try:
                pub1 = next(pub1)
                found = True
                break
            except Exception as e:
                set_new_proxy()
                print('next pub')
                if isinstance(e, StopIteration):
                    found = False
                    break
    if not found:
        while True:
            try:
                pub1 = scholarly.search_pubs(query='allintitle:"{}"'.format(pub.title), citations=False)
                break
            except Exception:
                set_new_proxy() 
                print('search title alone')
        while True:
            try:
                pub1 = next(pub1)
                for auth in pub1['bib']['author']:
                    print(f"{pub.pub_records.first().researcher.last_name}")
                    print(auth)
                    print(f"{pub.pub_records.first().researcher.last_name}" in auth)
                    print('\n')
                    if f"{pub.pub_records.first().researcher.last_name}" in auth:
                        found = True
                break
            except Exception as e:
                set_new_proxy()
                print('next pub')
                if isinstance(e, StopIteration):
                    found = False
                    break

    if found:
        while True:
            try:
                bibtex = scholarly.bibtex(pub1)
                break
            except Exception:
                set_new_proxy()
                print('bibtex')
        return bibtex
    return None

def verify_author(name):
    while True:
        try:
            author = scholarly.search_author(name)
            break
        except Exception:
            set_new_proxy()
    try:
        author = next(author)
        return author
    except StopIteration:
        return verify_author_from_search(name)

def verify_author_from_search(name):
    while True:
        try:
            author = scholarly.search_pubs(query='author: "{}"'.format(name), citations=False)
            break
        except Exception:
            set_new_proxy()
    try:
        author = next(author)
        return author
    except StopIteration:
        return None

# Retrieve the first result from the iterator
# try:
#     first_author_result = next(search_query)
# except Exception as e:
#     print(e.__repr__)
# scholarly.pprint(first_author_result)
#Returns personal info of author
#Scholar ID is important for verifications
# print(first_author_result)


# If author query yields no result

# pub_query = get_pub_query('Permanand', 'Mohan')
# print(next(pub_query))
# pubs = get_pubs(pub_query)
# filled = []
# for pub in pubs:
#     print(pub, '\n')
#     print(pub['gsrank'])
#     filled.append(fill_pub(pub))
# print(filled)

# Pull specifics for the author ["basics","indices","counts","coauthors","publications"]
# 'basics' = name, affiliation, and interests;
# 'indices' = h-index, i10-index, and 5-year analogues
# 'counts' = number of citations per year
# 'coauthors' = co-authors
# 'publications' = publications
# '[]' = all of the above (this is the default)
# e.g scholarly.fill(author,["basics","indices","counts","coauthors","publications"]) returns ALL info on the author
# author = scholarly.fill(first_author_result)
# scholarly.pprint(author)
# print(author)

# Take a closer look at the first publication
# first_publication = author['publications'][0]
# first_publication_filled = scholarly.fill(first_publication)
# scholarly.pprint(first_publication_filled)
# print(first_publication, '\n')

# # Print the titles of the author's publications
# publication_titles = [pub['bib']['title'] for pub in author['publications']]
# print(publication_titles)

# # Which papers cited that publication?
# citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
# print(citations)
