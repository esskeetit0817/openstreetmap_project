# coding: utf-8
# In[2]:


import csv
import sqlite3

db = sqlite3.connect("shenzhen.db")
db.text_factory = str
c = db.cursor()


c.execute('drop table if exists nodes')

nodes = '''
create table nodes
(
id Integer NOT NULL PRIMARY KEY,
lat float,
lon float,
user Text,
uid Integer,
version Integer,
changeset Integer,
timestamp Text
);
'''

c.execute(nodes) 

with open('../dataset/nodes.csv','rb') as nodes_f: 
    dict_reader = csv.DictReader(nodes_f) 
    for row in dict_reader:

        id_value = int(row['id'])
        lat_value = float(row['lat'])
        lon_value = float(row['lon'])
        user_value = str(row['user'])
        uid_value = int(row['uid'])
        version_value = int(row['version'])
        changeset_value = int(row['changeset'])
        timestamp_value = str(row['timestamp'])

        c.execute('INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?)',(id_value,lat_value,lon_value,user_value,uid_value,version_value,changeset_value,timestamp_value))

db.commit()
db.close()

