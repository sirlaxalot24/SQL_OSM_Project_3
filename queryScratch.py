import sqlite3

dbFile = "OSM_JP_Project.db"

db = sqlite3.connect(dbFile)

c = db.cursor()

query1 = "SELECT count(*) " \
         "FROM nodes;" \

query2 = "SELECT count(*) " \
         "FROM nodes_tags;"

query3 = "SELECT count(*) " \
         "FROM ways;"

query4 = "SELECT count(*) " \
         "FROM ways_nodes;"

query5 = "SELECT count(*) " \
         "FROM ways_tags;"

c.execute(query1)
print "Nodes: ", c.fetchall()[0][0]

c.execute(query2)
print "Nodes Tags: ", c.fetchall()[0][0]

c.execute(query3)
print "Ways: ", c.fetchall()[0][0]

c.execute(query4)
print "Ways_Nodes: ", c.fetchall()[0][0]

c.execute(query5)
print "Ways Tags: ", c.fetchall()[0][0]


db.close()