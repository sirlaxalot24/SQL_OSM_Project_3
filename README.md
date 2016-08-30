# P3: Wrangle OpenStreetMaps Data 

##Map Info

St. Louis, Missouri

- [https://www.openstreetmap.org/relation/177415](https://mapzen.com/data/metro-extracts/metro/saint-louis_missouri/)


##Trouble with the Dataset 

The consistency of the street name suffixes was made apparent by the case study for the SQL project. I also noticed on the project forums that a number of people were noticing issues with postal codes.
However, I did decide to do some additional looking prior to writing code to clean any necessary tags. I set up a small python script in order to look through various levels the CSV files created. By changing the variable's I could quickly search the largest tag 'types' and 'keys' for strange values
That script is below.

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
I was unaware that this was a mojor import of data. I began to try and search through the various tags associated with tiger data and decided that cleaning that data was unnecessary. The second strange key I stumbled upon was 'FIXME'. 
Through further investigation, I found that users are setting way tags to FIXME. This seemed to be mostly for road construction or error marking.

I decide neither of these keys, 'tiger' or 'FIXME', would be appropriate to clean. However, they did help me practice some tougher SQL and were interesting pieces of data to explore after I imported into SQLite.  

###Street Name and Postal Code Improvement

The code I used for cleaning street names was basically what I used for the case study portion of the course. Below is a portion of the .py file I wrote for cleaning both street names and zip. I decided to put the two functions in a separate file, cleanStreeZip.py.
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


The two functions were a great addition to the file that created my CSV's (data.py in the case study problems, my file equivalent is makeCSV.py). 

##Overview of the Data

##Other Ideas About the Dataset

###File Links

###Helpful websites and documentation

hoping that this was mainly one user but it seems to be a few

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


````

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