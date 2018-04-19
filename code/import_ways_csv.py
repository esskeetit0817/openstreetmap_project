
# coding: utf-8

# In[4]:

import csv
import sqlite3

db = sqlite3.connect("shenzhen.db")
db.text_factory = str
c = db.cursor()


c.execute('drop table if exists ways')

ways = '''
create table ways
(
id Integer primary key,
user Text,
uid Integer,
version Integer,
changeset Integer,
timestamp Text
);
'''

c.execute(ways)

with open('../dataset/ways.csv','rb') as ways_f: 
    dict_reader = csv.DictReader(ways_f) 
    for row in dict_reader:

        id_value = int(row['id'])
        user_value = str(row['user'])
        uid_value = int(row['uid'])
        version_value = int(row['version'])
        changeset_value = int(row['changeset'])
        timestamp_value = str(row['timestamp'])

        
        c.execute('INSERT INTO ways VALUES (?,?,?,?,?,?)',(id_value,user_value,uid_value,version_value,changeset_value,timestamp_value))

db.commit()
db.close()


