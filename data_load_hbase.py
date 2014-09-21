import happybase

connection = happybase.Connection('ec2-54-167-85-158.compute-1.amazonaws.com', table_prefix='chaos', table_prefix_separator=':')

print connection.tables()

# connection.create_table('artists', {'info' : dict(max_versions=10)})
# table = connection.table('artists')
#
# with open('/Users/ramz/Projects/uni/datamod/databases/lastfm/artists.dat') as fp:
#     data = fp.read().split('\n')
#     for val in data[1:]:
#         if val.strip():
#             id, name, url, picurl = val.split('\t')
#             artist_info = {'_id' : id, 'name' : name, 'url' : url, 'picture' : picurl }
#             table.put(id, {'info:name': name, 'info:url': url, 'info:picture' : picurl})
#
