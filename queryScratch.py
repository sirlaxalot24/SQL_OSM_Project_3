import sqlite3
from pprint import pprint as pp
import pandas as pd


dbFile = "OSM_JP_Project.db"

db = sqlite3.connect(dbFile)

c = db.cursor()

query = "SELECT * " \
        "FROM nodes " \
        "LIMIT 10;"

c.execute(query)

# ------ Grab header names for printing

headerVar = list(c.description)
headers = []

for i in range(len(headerVar)):
    headx = (headerVar[i][0])
    headers.append(headx)

# fetch data and print and make a dataframe for display purposes

data = pd.DataFrame(c.fetchall(), columns=headers)

pp(data)

db.close()