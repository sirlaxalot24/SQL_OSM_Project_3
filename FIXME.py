import sqlite3
from pprint import pprint as pp
import pandas as pd


# Found a node tag with a key of 'FIXEME' so I would like to explore who is using that key

dbFile = "OSM_JP_Project.db"
db = sqlite3.connect(dbFile)
c = db.cursor()

query = "SELECT nodes_tags.key as 'Tag Key', " \
        "nodes_tags.value as 'Tag Value', nodes_tags.type as 'Tag Type', " \
        "nodes_tags.id as 'Node Id', nodes.user as User, count(nodes.user) as Count " \
        "FROM nodes_tags " \
        "JOIN nodes " \
        "ON nodes_tags.id = nodes.id " \
        "WHERE key LIKE 'FIXME%' " \
        "GROUP BY nodes.user " \
        "ORDER BY Count DESC;"


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

db.close()