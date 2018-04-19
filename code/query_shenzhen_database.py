# coding=utf-8
import csv
import sqlite3
db = sqlite3.connect("../dataset/shenzhen.db")
c = db.cursor()

#��ȡ nodes ���ݱ��еĶ����û���
query1 = "select uid from nodes group by uid order by uid"
c.execute(query1)
nodes_uid = c.fetchall()
print 'Unique uid in table nodes is:'
print len(nodes_uid)

#��ȡ ways ���ݱ��еĶ����û���
query2 = "select uid from ways group by uid order by uid"
c.execute(query2)
ways_uid = c.fetchall()
print 'Unique uid in table ways is:'
print len(ways_uid)

#�����������ݿ��еĶ����û�������Ҫ��nodes���ݱ��ways���ݱ��еĶ����û�����Ӳ�ȥ��
for i in range(len(ways_uid)):
	if ways_uid[i] not in nodes_uid:
		nodes_uid.append(ways_uid[i])
unique_uid = len(nodes_uid)
print 'total unique users is:'
print unique_uid
