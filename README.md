# P3: Wrangle OpenStreetMaps Data 

###Map of St. Louis



```python
import csv
from pprint import pprint as pp
import cleanStreeZip

# this file is used to check the CVS's for systemic issues with the data
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Terrace", "Way", "Highway", "Plaza", "Circle"]

topVar = 'type'
bVar = 'key'
param = 'street'
fileName = 'nodes_tags.csv'


crazyVals = {}

with open(fileName, 'r') as f:
    tags = csv.DictReader(f)
    for row in tags:

        # run this statement when looking for odd values

        if row[topVar] == param and bVar == 'value':
            # zipCode = cleanStreeZip.clean_street_name(row[bVar])
            streetName = row[bVar]
            # print streetName
            if streetName in expected:
                pass
            elif streetName not in crazyVals:
                crazyVals[streetName] = 1
            else:
                crazyVals[streetName] += 1

            # run this statement when exploring keys and types
        else:
            if row[bVar] not in crazyVals:
                crazyVals[row[bVar]] = 1
            else:
                crazyVals[row[bVar]] += 1

pp(crazyVals)
```

#Crazy tables test

```
      key                                              value          id          user  Count
0   FIXME                                          continue?  1788024764           NE2     45
1   fixme  tiger corrected / reviewed to this position, s...  1466883332       WernerP     19
2   FIXME                                          continue?  1780841454  railfan-eric     11
3   FIXME  Remove barrier when bridge construction is com...  4005088578      banjavjs     10
4   fixme                                        extend line  1874787257        zephyr     10
5   fixme                         unvollstaendig / not ready  1468568549       ELadner      5
6   FIXME                         An aerodrome here, really?   368934161   maxerickson      2
7   fixme                         unvollstaendig / not ready  1466842255      Sundance      1
8   fixme  survey pleaese: is there really a street conne...   191032712   aseerel4c26      1
9   fixme                                        extend line  1821522368     bahnpirat      1
10  fixme  Please add turn restrictions as needed. Maybe ...   191054803     dannykath      1
11  fixme                    This does not look like a park.   354110002       g246020      1
12  fixme                   This junction looks to be wrong.   193079849          spod      1
13  FIXME                                      check signage   313034400       stucki1      1
14  FIXME            Position is in the middle of the street  4327912487     user_5359      1
```