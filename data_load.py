from pymongo import MongoClient

client = MongoClient('mongos', 27017)

db = client.test

with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/artists.dat') as fp:
    data = fp.read().split('\n')
    for val in data[1:]:
        if val.strip():
            id, name, url, picurl = val.split('\t')
            artist_info = {'_id' : int(id), 'name' : name, 'url' : url, 'picture' : picurl }
            db.artists.insert(artist_info)

user_info = { }

friends_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_friends.dat') as fp:
    for line in fp.readlines():
        if line:
            user, friend = line.strip().split('\t')
            user_info.setdefault(user,{'friends' : []})
            user_info[user]['friends'].append(friend)
            user_info[user]['friends'].append(user)

user_listen_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_artists.dat') as fp:
    for line in fp.readlines():
        if line:
            user,artist,count = line.strip().split('\t')
            user_listen_list.setdefault(user,[]).append({'artist' : artist, 'playcount' : count})
    # print user_listen_list

tags_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/tags.dat') as fp:
    for line in fp.readlines():
        tagid, tag = line.strip().split('\t')
        tags_list[tagid] = tag

user_tags_list = {}
with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/user_taggedartists.dat') as fp:
    for line in fp.readlines():
        user, artist, tag, day, month, year = line.strip().split('\t')
        # user_tags_list.setdefault(user,[]).append({'artist' : artist, 'tag' : tags_list[tag]})
        for user_artist in user_listen_list[user]:
            if (user_artist['artist'] == artist):
                user_artist.setdefault('tag', []).append(tags_list[tag])
    # print user_tags_list

for user,listen in user_listen_list.iteritems():
    user_info[user]['_id'] = user
    user_info[user]['artists'] = listen
    db.users.insert(user_info[user])
