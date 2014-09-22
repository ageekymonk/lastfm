from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.music

with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/artists.dat') as fp:
    data = fp.read().split('\n')
    for val in data[1:]:
        if val.strip():
            id, name, url, picurl = val.split('\t')
            artist_info = {'_id' : int(id), 'name' : name, 'url' : url, 'picture' : picurl }
            db.artists.insert(artist_info)

user_info = { }
print "step 1 completed"
friends_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_friends.dat') as fp:
    fp.readline()
    for line in fp.readlines():
        if line:
            user, friend = line.strip().split('\t')
            user_info.setdefault(user,{'friends' : []})
            user_info[user]['friends'].append(int(friend))

print "step 2 completed"
user_listen_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_artists.dat') as fp:
    fp.readline()
    for line in fp.readlines():
        if line:
            user,artist,count = line.strip().split('\t')
            op = db.artists.find_one({'_id' : int(artist)})
            user_listen_list.setdefault(user,[]).append({'artist' : int(artist), 'playcount' : int(count), 'url' : op['url'],
                                                         'picture' : op['picture'], 'name' : op['name']})
    # print user_listen_list

print "step 3 completed"
tags_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/tags.dat') as fp:
    fp.readline()
    for line in fp.readlines():
        tagid, tag = line.strip().split('\t')
        tags_list[tagid] = tag

print "step 4 completed"
user_tags_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_taggedartists.dat') as fp:
    fp.readline()
    for line in fp.readlines():
        user, artist, tag, day, month, year = line.strip().split('\t')
        # user_tags_list.setdefault(user,[]).append({'artist' : artist, 'tag' : tags_list[tag]})
        for user_artist in user_listen_list[user]:
            if (user_artist['artist'] == int(artist)):
                user_artist.setdefault('tag', []).append(tags_list[tag])
    # print user_tags_list

for user,listen in user_listen_list.iteritems():
    user_info[user]['_id'] = int(user)
    user_info[user]['artists'] = listen
    db.users.insert(user_info[user])

print "All done"