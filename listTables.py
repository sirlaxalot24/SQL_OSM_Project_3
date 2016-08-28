import sqlite3

dbFile = "OSM_JP_Project.db"

db = sqlite3.connect(dbFile)

c = db.cursor()

tableQuery = "SELECT name FROM sqlite_master WHERE type='table';"

c.execute(tableQuery)

rows = c.fetchall()

for i in rows:
    QUERY = "pragma table_info('%s')" % i
    c.execute(QUERY)
    table = c.fetchall()
    print i[0]
    for x in table:
        print x[1:3]
    print ""

db.close()