# P3: Wrangle OpenStreetMaps Data 

##Map Info

St. Louis, Missouri

- [https://www.openstreetmap.org/relation/177415](https://mapzen.com/data/metro-extracts/metro/saint-louis_missouri/)


##Trouble with the Dataset 

The consistency of the street name suffixes was made apparent by the case study for the SQL project. I also noticed on the project forums that a number of people were noticing issues with postal codes.
However, I did decide to do some additional looking prior to writing code to clean any necessary tags. I set up a small python script in order to look through various levels the CSV files created. By changing the variable's I could quickly search the largest tag 'types' and 'keys' for strange values
That script is below ([crazyVals.py](crazyVals.py)).

```python

#files name is crazyVals.py

import csv
from pprint import pprint as pp
import cleanStreeZip


# this file is used to check the CVS's for systemic issues with the data


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Terrace", "Way", "Highway", "Plaza", "Circle"]

topVar = 'type'
bVar = 'key'
param = 'street'
fileName = 'ways_tags.csv'


crazyVals = {}

with open(fileName, 'r') as f:
    tags = csv.DictReader(f)
    for row in tags:

        # run this statement when looking for odd values

        if row[topVar] == param and bVar == 'value':
            # zipCode = cleanStreeZip.clean_street_name(row[bVar])
            streetName = row[bVar].split()[-1]
            # print streetName
            if streetName in expected:
                pass
            elif streetName not in crazyVals:
                crazyVals[streetName] = 1
            else:
                crazyVals[streetName] += 1

        elif bVar == 'value':
            pass

            # run this statement when exploring keys and types
        else:
            if row[bVar] not in crazyVals:
                crazyVals[row[bVar]] = 1
            else:
                crazyVals[row[bVar]] += 1

pp(crazyVals)
```

This block of code came in very handy when debugging my file that cleaned the data and created the CSV's. I mostly adapted the code from portions of the problem in from the case study. The most glaring issue was the key 'tiger'.
I was unaware that this was a major import of data. I began to try and search through the various tags associated with tiger data and decided that cleaning that data was unnecessary. The second strange key I stumbled upon was 'FIXME'. 
Through further investigation, I found that users are setting way tags to FIXME. This seemed to be mostly for road construction or error marking.

I decide neither of these keys, 'tiger' or 'FIXME', would be appropriate to clean. However, they did help me practice some tougher SQL and were interesting pieces of data to explore after I imported into SQLite.  

###Street Name and Postal Code Improvement

The code I used for cleaning street names was basically what I used for the case study portion of the course. Below is a portion of the .py file I wrote for cleaning both street names and zip. I decided to put the two functions in a separate file, [cleanStreeZip.py](cleanStreeZip.py).
I decided to split the element on the commas and only keep the first part of the returned list. The ordinal audit.py from the case study left the full string in the returned value. Removing the rest of the string, such as the errant city and state cleaned up my street names greatly.


```python

def clean_street_name(name, mapping=MAPPING):
    """

    :type name: str
    """
    m = name.split(',')
    m = street_type_re.search(m[0])
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type, mapping[street_type], name).split(',')[0]
        else:
            pass

    return name.split(',')[0]

```

For the postal code improvements I decided to just grab the first occorance of a 5 digit sequence using regular expressions. In the end the postal codes never had a sequence of 5 digits anywhere in the tag value other than the appropriate postal code value. that code is below along with the regular expression. 

```python

findZip = re.compile(r'.*(\d{5}?)$', re.IGNORECASE)

def clean_zip(zipCode):
    m = findZip.search(zipCode)
    if m:
        return findZip.findall(zipCode)[0]
    else:
        return '00000'
```


The two functions were a great addition to the file that created my CSV's (data.py in the case study problems, my file equivalent is [makeCSV.py](makeCSV.py). 

##Overview of the Data

For a quick overview of the size of my tables, I put together this fairly inefficient but effective file, [queryScratch.py](queryScratch.py). 

```python
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
```



```
Nodes:  1688506
Nodes Tags:  80298
Ways:  162837
Ways_Nodes:  1919496
Ways Tags:  957365

```

####Other Dataset Size Information

[Link to Larger Files](https://www.dropbox.com/sh/gdrgz6cpxdcnekr/AAAfe7o0KQ8X0la7eqU0einWa?dl=0)

- saint-louis_missouri.osm  360 MB
- nodes.csv                 136 MB
- nodes_tags.csv            3 MB
- ways.csv                  9 MB
- ways_nodes.csv            44 MB
- ways_tags.csv             33 MB

##Other Ideas About the Dataset

I spent most of my SQL writing time digging into the tiger and FIXME data I discovered in the audit portion of the project. I had two main assumptions or questions. The first was about the tiger data and if a large import like that could possibly import zip code data outside of the St. Louis zip codes.
The second assumption was that one person was using the FIXME tag and could I take a closer look at how they were using it.
 
#####Tiger Data

The code below is from [tigerData.py](tigerData.py). The first query was fairly straight forward. I wanted to see how many users had imported tiger. It turns out there are quite a few, but no one user imported more information than bot-mode.
After seeing the amount of data bot-mode imported, I decided to focus just on that users Zip Codes. Bot-mode did not actually import anything outside of the St. Louis zips but did however import a very large variety of zip codes. The bottom figure in this section is bot-mode's imported zip by count.
I realize that the top twenty zip codes imported isn't overwhelmingly exciting. I chose to include the sql and code here because it displayed the struggle I had writing a small sub query in query2. The results of the two queries are included below.

```
import sqlite3
from pprint import pprint as pp
import pandas as pd


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
```

######All Users Importing Tiger Data
```
               User   Count
0          bot-mode  244031
1   DaveHansenTiger   72014
2             Rub21   22733
3       maxerickson   17790
4        Millbrooky   16435
5            Ardric   14026
6          banjavjs   10140
7          RichRico    8650
8           g246020    8579
9               NE2    8263
10            Brett    7314
11        dannykath    7171
12        Luis36995    5342
13         CmdrThor    4129
14        andrewpmk    3931
15     railfan-eric    3852
16          ELadner    3494
17         Tom Layo    3387
18            MikeN    3122
19       AndrewSnow    3077
20       Mr Ballwin    3000
21        happy5214    2949
22           rhilde    2564
23        Mark Sims    2513
24           ediyes    2136

```
######bot-mode's Imports
```
        User Zip Codes  Count
0   bot-mode     63376   1594
1   bot-mode     62002   1465
2   bot-mode     62234   1243
3   bot-mode     63304   1182
4   bot-mode     62025   1126
5   bot-mode     63017   1012
6   bot-mode     63031   1004
7   bot-mode     63129    932
8   bot-mode     63123    878
9   bot-mode     63366    875
10  bot-mode     63301    838
11  bot-mode     63026    832
12  bot-mode     63010    815
13  bot-mode     62040    811
14  bot-mode     63122    784
15  bot-mode     63303    751
16  bot-mode     63021    725
17  bot-mode     62223    687
18  bot-mode     62269    680
19  bot-mode     62221    671

```


#####FIXME Data

I was really hoping the tags with the key 'FIXME' were from one user. It turns out the tags were actually from multiple users listed below, sorted by count. The "Tag Value" column in the output shows a couple examples of how users were marking certain tags to be checked on later.
The full file for this output is [FIXME.py](FIXME.py). Here is the SQL. 
 
```SQL
SELECT nodes_tags.key as 'Tag Key',
nodes_tags.value as 'Tag Value', nodes_tags.type as 'Tag Type',
nodes_tags.id as 'Node Id', nodes.user as User, count(nodes.user) as Count
FROM nodes_tags
JOIN nodes
ON nodes_tags.id = nodes.id
WHERE key LIKE 'FIXME%'
GROUP BY nodes.user
ORDER BY Count DESC;

```

###### FIXME Output
```
   Tag Key                                          Tag Value Tag Type     Node Id          User  Count
0    FIXME                                          continue?  regular  1788024764           NE2     45
1    fixme  tiger corrected / reviewed to this position, s...  regular  1466883332       WernerP     19
2    FIXME                                          continue?  regular  1780841454  railfan-eric     11
3    FIXME  Remove barrier when bridge construction is com...  regular  4005088578      banjavjs     10
4    fixme                                        extend line  regular  1874787257        zephyr     10
5    fixme                         unvollstaendig / not ready  regular  1468568549       ELadner      5
6    FIXME                         An aerodrome here, really?  regular   368934161   maxerickson      2
7    fixme                         unvollstaendig / not ready  regular  1466842255      Sundance      1
8    fixme  survey pleaese: is there really a street conne...  regular   191032712   aseerel4c26      1
9    fixme                                        extend line  regular  1821522368     bahnpirat      1
10   fixme  Please add turn restrictions as needed. Maybe ...  regular   191054803     dannykath      1
11   fixme                    This does not look like a park.  regular   354110002       g246020      1
12   fixme                   This junction looks to be wrong.  regular   193079849          spod      1
13   FIXME                                      check signage  regular   313034400       stucki1      1
14   FIXME            Position is in the middle of the street  regular  4327912487     user_5359      1
```



###Additional File Links

- [xmlSample.py](xmlSmaple.py)
- [smallStLou.osm](smallStLou.osm)  *This is the sample file
- [listTables.py](listTables.py) *I will always keep this code close by when working with SQLite. It was a great way to list out all the tables and columns
- [OSM_JP_tables.txt](OSM_JP_tables.txt) *Output of listTables.py
- [schema.py](schema.py)
- [create_tables.py](create_tables.py) *This is the code I used to create the tables in SQLite. This was much easier than using SQLite from the cmd line. 



###Helpful websites and documentation

- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [sqlite3 Docs](https://docs.python.org/2/library/sqlite3.html)
- [Python re docs](https://docs.python.org/2/library/re.html)
- [w3schools.com SQL tutorial](http://www.w3schools.com/sql/)
- [ElementTree Docs](https://docs.python.org/2/library/xml.etree.elementtree.html)
- [sebastianraschka - A thorough guide to SQLite database operations in Python](http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html)
- [Pandas Print Settings](http://pandas.pydata.org/pandas-docs/stable/options.html)