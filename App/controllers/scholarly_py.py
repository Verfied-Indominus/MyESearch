from scholarly import scholarly, ProxyGenerator

pg = ProxyGenerator()

def set_new_proxy():
    while True:
        success = pg.FreeProxies()
        if success:
            scholarly.use_proxy(pg)
            break

def get_pub_query(name):
    set_new_proxy()
    i = 0
    while True:
        try:
            pub_query = scholarly.search_pubs(name)
            break
        except Exception:
            i += 1
            print("Author", i)
            set_new_proxy()
    return pub_query

def get_pubs(pub_query, name):
    i = 0
    pubs = []
    name = get_shortened_name(name)
    while True:
        try:
            for pub in pub_query:
                if (name in pub['bib']['author']) or (name.upper() in pub['bib']['author']):
                    pubs.append(pub)
                else:
                    break
            break
        except Exception:
            i += 1
            print("Pub_List", i)
            set_new_proxy()
    return pubs

def fill_pubs(pubs):
    i = 0
    filled = []
    for pub in pubs:
        while True:
            try:
                fill = pub.fill()
                filled.append(fill)
                print(fill['bib']['abstract'])
                break
            except Exception:
                i += 1
                print("Filled_List", i)
                set_new_proxy()
    return filled

def get_shortened_name(name):
    name = name.split(' ')
    if len(name) == 2:
        name = "{} {}".format(name[0][0], name[1])
    elif len(name) == 3:
        name = "{}{} {}".format(name[0][0], name[1][0], name[2])
    return name

first_author_result = None

# search_query = scholarly.search_author('Permanand Mohan')
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
if not first_author_result:
    name = 'Permanand Mohan'
    pub_query = get_pub_query(name)
    print(next(pub_query)['bib']['abstract'])
    # pubs = get_pubs(pub_query, name)

    # filled = fill_pubs(pubs)
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
# print(first_publication_filled)

# # Print the titles of the author's publications
# publication_titles = [pub['bib']['title'] for pub in author['publications']]
# print(publication_titles)

# # Which papers cited that publication?
# citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
# print(citations)
