#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import re
import xml.etree.cElementTree as ET

# cleanStreetZip imports the functions I built to clean street names and zip codes
# The file is 'cleanStreetZip.py'

import cleanStreeZip
# from pprint import pprint as pp

import cerberus

import schema

OSM_PATH = 'saint-louis_missouri.osm'

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# added function to shape shape the attribute values for both Node tags and Way tags
# this also calls the function to clean street name/zip code if necessary

def shape_tag(child):
    if LOWER_COLON.findall(child['k']):
        key = child['k'].split(':', 1)[1]
        if key == 'Street' or key == 'street':
            value = cleanStreeZip.clean_street_name(child['v'])
        elif key == 'postcode':
            value = cleanStreeZip.clean_zip(child['v'])
        else:
            value = child['v']

        type1 = child['k'].split(':', 1)[0]

    else:
        key = child['k']
        if key == 'Street' or key == 'street':
            value = cleanStreeZip.clean_street_name(child['v'])
        elif key == 'postcode':
            value = cleanStreeZip.clean_zip(child['v'])
        else:
            value = child['v']

        type1 = 'regular'

    return key, value, type1


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    counter = 0

    # MY CODE START------------------------------------------------------#
    # MY CODE START------------------------------------------------------#

    # NODE SETUP---------------------------------------------------------#

    if element.tag == 'node':
        for i in node_attr_fields:
            try:
                node_attribs[i] = element.attrib[i]
            except:
                node_attribs[i] = '00000'
                pass

        for child in element:
            if child.tag == 'tag':
                if PROBLEMCHARS.findall(child.attrib['k']):
                    pass
                else:
                    key, value, type1 = shape_tag(child.attrib)
                    tags.append({'id': element.attrib['id'], 'key': key, 'value': value, 'type': type1})
    else:
        pass

    # WAY SETUP---------------------------------------------------------#

    if element.tag == 'way':
        for i in way_attr_fields:
            way_attribs[i] = element.attrib[i]

        for child in element:
            if child.tag == 'nd':
                way_nodes.append({'id': element.attrib['id'], 'node_id': child.attrib['ref'],
                                  'position': counter})
                counter += 1

            elif child.tag == 'tag':
                if problem_chars.findall(child.attrib['k']):
                    pass
                else:
                    key, value, type1 = shape_tag(child.attrib)
                    tags.append({'id': element.attrib['id'], 'key': key, 'value': value, 'type': type1})
    else:
        pass

    # MY CODE END------------------------------------------------------#
    # MY CODE END------------------------------------------------------#

    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in
                                                row.iteritems()})

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #

# One change to the main function was in the first with statement. I changed open(filename, 'w') to 'wb'
# the 'w' param was causing an extra \n character to be printed causing a blank line in my CSV files

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'wb') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'wb') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:
        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
