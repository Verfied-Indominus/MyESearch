from scholarly import scholarly, ProxyGenerator

pg = ProxyGenerator()

def set_new_proxy():
    while True:
        success = pg.FreeProxies()
        if success:
            scholarly.use_proxy(pg)
            break

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
i = 0

if not first_author_result:
    while True:
        try:
            pub_query = scholarly.search_pubs('Permanand Mohan')
            break
        except Exception as e:
            i += 1
            print("Author", i)
            set_new_proxy()

filled_pubs = []
while True:
    try:
        for pub in pub_query:
            while True:
                try:
                    fill = scholarly.fill(pub)
                    filled_pubs.append(fill)
                    print(fill)
                    print('\n')
                    break
                except Exception as e:
                    i += 1
                    print("Pub", i)
                    set_new_proxy()
        break
    except Exception as e:
        i += 1
        print("Pub", i)
        set_new_proxy()

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
