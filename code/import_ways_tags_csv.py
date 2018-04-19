
# coding: utf-8

# In[4]:

import csv
import sqlite3

db = sqlite3.connect("shenzhen.db")
db.text_factory = str
c = db.cursor()


c.execute('drop table if exists ways_tags')

ways_tags= '''
create table ways_tags
(
id Integer ,
key Text,
value Text,
type Text,
FOREIGN KEY (id) REFERENCES ways (id)
);
'''

c.execute(ways_tags)

with open('../dataset/ways_tags.csv','rb') as ways_tags_f: 
    dict_reader = csv.DictReader(ways_tags_f) 
    for row in dict_reader:

        id_value = int(row['id'])
        key_value = str(row['key'])
        v_value = str(row['value'])
        type_value = str(row['type'])

        
        c.execute('INSERT INTO ways_tags VALUES (?,?,?,?)',(id_value,key_value,v_value,type_value))

db.commit()
db.close()



