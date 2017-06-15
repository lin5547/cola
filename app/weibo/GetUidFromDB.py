from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_name = 'sina1'
db = client[db_name]




dbuid = []


print('get id from follows and fans')

for u in db.weibo_user.find():
    for item in u['follows']:
        id = item['uid']
        if id not in dbuid:
            dbuid.append(id)
    for item in u['fans']:
        id = item['uid']
        if id not in dbuid:
            dbuid.append(id)

print('get io form comments')
commentuid =[]
for u in db.micro_blog.find():
    comments = u['comments']
    id = u['uid']
    temp_chat={}
    key=[]
    if len(comments)>0:
        comments.reverse()
        for comment in comments:
            if u'：回复@'not in comment['content']:
                continue
            c = comment['content']
            comment = comment['content'].split(u'：')

            if id not in commentuid:
                commentuid.append(id)


uid =commentuid
for id in dbuid:
    if id not in commentuid:
        uid.append(id)
count = 0

f = open('uid.yaml','w')
f.write('starts:\n')

for id in uid:
    f.write('  - uid: ' + id + '\n')
f.close()