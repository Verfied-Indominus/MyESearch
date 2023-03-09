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
            pub = scholarly.search_pubs(query='allintitle: "{}" author: "{} {}"'.format(pub['bib']['title'], fname, lname))
            break
        except Exception:
            set_new_proxy()
            print('search')
    return pub


def fill_pub(pub, fname, lname):
    pub1 = search_pub(pub, fname, lname)
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


# pubs = get_pubs('Shareeda', 'Mohammed')
# for pub in pubs:
#     print(pub)
#     print('\n\n')
#     fill = fill_pub(pub, 'Shareeda', 'Mohammed')
#     print(fill)
#     break
# print('\n\n')
# authors = fill['bib']['author'].split(' and ')
# temp = []
# for author in authors:
#     temp.append(author.split(', '))
# authors = temp
# temp = []
# for author in authors:
#     author.reverse()
#     temp.append(' '.join(author))
# authors = temp
# authors.remove('Shareeda Mohammed')
# authors = ', '.join(authors)
# print(authors)
# request = f"Extract the research Keywords from the following as a python list'{fill['bib']['abstract']}'"
# key_list  = prompt(request)["choices"][0]["text"]
# print(key_list)

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
