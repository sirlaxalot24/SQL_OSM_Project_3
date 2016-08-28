import csv
from pprint import pprint as pp
import cleanStreeZip


topVar = 'user'
bVar = 'value'
param = 'xybot'

crazyVals = {}

with open('nodes.csv', 'r') as f:
    tags = csv.DictReader(f)
    for row in tags:
        if row[topVar] == param:
            pp(row)
            # if row[bVar] not in crazyVals:
            #     crazyVals[row[bVar]] = 1
            # else:
            #     crazyVals[row[bVar]] += 1


        # if row[bVar] not in crazyVals:
        #     crazyVals[row[bVar]] = 1
        # else:
        #     crazyVals[row[bVar]] += 1

pp(crazyVals)