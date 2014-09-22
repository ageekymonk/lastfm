from py2neo import neo4j
from py2neo import cypher
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.music

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

# with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/artists.dat') as fp:
#     data = fp.read().split('\n')
#     for val in data[1:]:
#         if val.strip():
#             id, name, url, picurl = val.split('\t')
#             artist_info = {'id': int(id), 'name' : name, 'url' : url, 'picture' : picurl }
#             graph_db.create(artist_info)[0].add_labels('ARTIST')
#
# print "Created All Artists"
# rows = db.users.find({})
# rows = [row for row in rows]
# for row in rows:
#     id,name,picture = row['_id'],row['name'],row['picture']
#     user_info = {'id':int(id), 'name': name, 'picture' : picture}
#     graph_db.create(user_info)[0].add_labels('USER')
#
# print "Created All Users"
#
# rows = db.users.find({})
# for row in rows:
#     friend_list = row['friends']
#     for friend in friend_list:
#         query = "MATCH (n:USER {{id: {0} }}), (m: USER {{id: {1}}}) CREATE (n)-[:FRIEND]->m RETURN n".format(row['_id'],friend)
#         cypher.execute(graph_db,query)
#
# print "Created All Friends"
#
# print "Creating Relation User Listens to Artist"
# rows = db.users.find({})
# rows = [row for row in rows]
# for row in rows:
#     artist_list = row['artists']
#     for artist in artist_list:
#         query = "MATCH (n:USER {{id: {0} }}), (m: ARTIST {{id: {1}}}) " \
#                 "CREATE (n)-[:LISTENS {{count: {2} }}]->m RETURN n".format(int(row['_id']),int(artist['artist']),artist['playcount'])
#         cypher.execute(graph_db,query)
#
# print "Created all Listens to artists"

print "Creating Relation User Tags Artist"
rows = db.users.find({})
rows = [row for row in rows]
for row in rows:
    artist_list = row['artists']
    for artist in artist_list:
        if artist.has_key('tag'):
            # query = "MATCH (n:USER {{id: {0} }}), (m: ARTIST {{id: {1}}}) " \
            # "CREATE (n)-[:TAGS {{tags: {2} }}]->(m) RETURN n".format(int(row['_id']),int(artist['artist']),
            #                                                        [str(x) for x in artist['tag']])
            # print query
            # cypher.execute(graph_db,query)

            for tag in artist['tag']:
                query = "MATCH (n:USER {{id: {0} }}), (m: ARTIST {{id: {1}}}) " \
                        "CREATE (n)-[:`{2}`]->m RETURN n".format(row['_id'],artist['artist'],tag)
                print query
                cypher.execute(graph_db,query)