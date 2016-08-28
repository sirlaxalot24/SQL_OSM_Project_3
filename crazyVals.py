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
