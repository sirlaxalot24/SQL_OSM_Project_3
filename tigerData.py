import sqlite3
from pprint import pprint as pp
import pandas as pd


# Found a node tag with a key of 'FIXEME' so I would like to explore who is using that key

dbFile = "OSM_JP_Project.db"
db = sqlite3.connect(dbFile)
c = db.cursor()

query = "SELECT ways.user as User, count(*) as Count " \
        "FROM ways_tags " \
        "JOIN ways " \
        "ON ways_tags.id = ways.id " \
        "WHERE type = 'tiger'" \
        "GROUP BY User " \
        "ORDER BY Count DESC " \
        "LIMIT 25; "


c.execute(query)

# ------ Grab header names

headerVar = list(c.description)
headers = []

for i in range(len(headerVar)):
    headx = (headerVar[i][0])
    headers.append(headx)

# fetch data, print, and make a dataframe for display purposes

data = pd.DataFrame(c.fetchall(), columns=headers)
pd.set_option("expand_frame_repr", False)

pp(data)


query2 = "SELECT User, zips as 'Zip Codes', count(*) as Count " \
         "FROM(SELECT ways_tags.value as zips, ways.user as User " \
         "FROM ways_tags " \
         "JOIN ways " \
         "ON ways_tags.id = ways.id " \
         "WHERE ways.user = 'bot-mode' " \
         "and ways_tags.type = 'tiger' " \
         "and (ways_tags.key = 'zip_right' " \
         "or ways_tags.key = 'zip_left')) as zipsTb " \
         "GROUP BY zips " \
         "ORDER BY Count DESC " \
         "LIMIT 20;" \

c.execute(query2)
# ------ Grab header names

headerVar2 = list(c.description)
headers2 = []

for i in range(len(headerVar2)):
    headx2 = (headerVar2[i][0])
    headers2.append(headx2)

# fetch data, print, and make a dataframe for display purposes

data2 = pd.DataFrame(c.fetchall(), columns=headers2)
pd.set_option("expand_frame_repr", False)

pp(data2)

db.close()