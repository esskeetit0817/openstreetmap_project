
# coding: utf-8

# In[4]:

import csv
import sqlite3

db = sqlite3.connect("shenzhen.db")
db.text_factory = str
c = db.cursor()


c.execute('drop table if exists ways_nodes')

ways_nodes = '''
create table ways_nodes
(
id Integer ,
node_id Integer,
position Integer,
FOREIGN KEY (id) REFERENCES ways (id)
);
'''

c.execute(ways_nodes)

with open('../dataset/ways_nodes.csv','rb') as ways_nodes_f: 
    dict_reader = csv.DictReader(ways_nodes_f) 
    for row in dict_reader:

        id_value = int(row['id'])
        node_id_value = int(row['node_id'])
        position_value = int(row['position'])

        
        c.execute('INSERT INTO ways_nodes VALUES (?,?,?)',(id_value,node_id_value,position_value))

db.commit()
db.close()


