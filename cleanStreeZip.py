import re
from pprint import pprint as pp

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
findZip = re.compile(r'.*(\d{5}?)$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Terrace", "Way", "Highway", "Plaza", "Circle"]

MAPPING = {"St": "Street",
           "St.": "Street",
           "street": "Street",
           "Ave": "Avenue",
           "Aveneu": "Avenue",
           "Av.": "Avenue",
           "Ave.": "Avenue",
           "AVE": "Avenue",
           "AVE.": "Avenue",
           "Blvd": "Boulevard",
           "Blvd.": "Boulevard",
           "Boulelvard": "Boulevard",
           "Cir": "Circle",
           "Ct": "Court",
           "Ct.": "Court",
           "Ctr": "Center",
           "Dr": "Drive",
           "Dr.": "Drive",
           "Ln": "Lane",
           "PLACE": "Place",
           "Pkwy": "Parkway",
           "Pky": "Parkway",
           "Rd": "Road",
           "Rd.": "Road",
           "RD": "Road",
           "Trl": "Trail",
           "RdSt Louis": "Road",
           "PlaceArnold": "Place",
           "Ctr.": "Center",
           "StKimmswick": "Street"}


# Takes in the string associated with the key value in makeCSV.py if deemed to be a street name
# the string is split on the first comma and only index 0 in that list is manipulated and  returned

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


# the re expression returns any occurrence of 5 digits in a row

def clean_zip(zipCode):
    m = findZip.search(zipCode)
    if m:
        return findZip.findall(zipCode)[0]
    else:
        return '00000'
