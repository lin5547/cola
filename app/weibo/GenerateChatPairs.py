# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pickle

def CombineSameName(data):
    tmpdata=[]
    for i in range(len(data)):
        if i==0:
            tmpdata.append(data[i])
            continue

        last=data[i-1]['n1']+u':'+data[i-1]['n2']
        cur = data[i]['n1']+u':'+data[i]['n2']
        if last==cur:
            tmpdata[-1]['content'] += data[i]['content']
        else:tmpdata.append(data[i])
    return tmpdata

client = MongoClient('localhost', 27017)
db_name = 'sina1'
db = client[db_name]

c = 0

chatpair={}

f = open('chatpair.txt','w')



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


            n1 = comment[0]
            try:
                n2 = comment[1].split(u':')[0].split(u'@')[1]
            except Exception as e:
                print(c)
                continue
            content = u':'.join(comment[1].split(u':')[1:])
            if n1==n2:
                continue

            cc={'n1':n1,'n2':n2,'content':content}

            if n1+u':'+n2 not in temp_chat and n2+u':'+n1 not in temp_chat:
                temp_chat[n1+u':'+n2] = []
                temp_chat[n1+u':'+n2].append(cc)
                key.append(n1+u':'+n2)
            else:
                try:
                    temp_chat[n1+u':'+n2].append(cc)
                except Exception as e:
                    temp_chat[n2+u':'+n1].append(cc)
                    continue
        if len(temp_chat)>0:
            a = 0
            for w in key:
                temp_chat[w]=CombineSameName(temp_chat[w])
                if len(temp_chat[w])<=1:
                    del temp_chat[w]
    if len(temp_chat)!=0:

        for item in temp_chat.items():
            for line in item[1]:
                f.write(line['content']+'\n')

            f.write('\n')
f.close()


