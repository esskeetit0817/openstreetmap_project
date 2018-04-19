#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema
SCHEMA = schema.schema
OSM_PATH = "../dataset/shenzhen.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']

        if re.search(lower,k):
            keys['lower']+=1
        elif re.search(lower_colon,k):
            keys['lower_colon']+=1
        elif re.search(problemchars,k):
            keys['problemchars']+=1
            
        else:
            keys['other']+=1
        # YOUR CODE HERE
        pass
        
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for event, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def is_post_code(elem):
    return(elem.attrib['k'] == "addr:postcode")

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            if is_post_code(tag):
                post_code = tag.attrib['v']
                    
                if 'DD' in post_code:
                    new_post_code = post_code.replace(' ', '')[2:]
                    tag.attrib['v'] = new_post_code 
    
    if element.tag == 'node':
        for node_field in NODE_FIELDS:
            node_attribs[node_field] = element.attrib[node_field]
        
        for node_tag in element.iter('tag'):
            node_tags_dict = {}
            problem = re.search(PROBLEMCHARS,node_tag.attrib['k'])
            colon = re.search(LOWER_COLON,node_tag.attrib['k'])
            
            
            if problem:
                continue
            elif colon:
                node_tags_dict['id'] = element.attrib['id']
                node_tags_dict['key'] = node_tag.attrib['k'].split(":",1)[1]
                node_tags_dict['type'] = node_tag.attrib['k'].split(":",1)[0]
                node_tags_dict['value'] = node_tag.attrib['v']
                tags.append(node_tags_dict)
            else:
                node_tags_dict['key'] = node_tag.attrib['k']
                node_tags_dict['type'] = "regular"
                node_tags_dict['id'] = element.attrib['id']
                node_tags_dict['value'] = node_tag.attrib['v']
                tags.append(node_tags_dict)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for way_attr_fields in WAY_FIELDS:
            way_attribs[way_attr_fields] = element.attrib[way_attr_fields]
            
        counter = 0
        for way_node in element.iter("nd"):
            way_nodes_dict = {}
            way_nodes_dict['id'] = element.attrib['id']
            way_nodes_dict['node_id'] = way_node.attrib['ref']
            way_nodes_dict['position'] = counter
            counter +=1
            way_nodes.append(way_nodes_dict)
        
        
        
        
        for way_tag in element.iter('tag'):
            way_tags_dict = {}
            problem = re.search(PROBLEMCHARS,way_tag.attrib['k'])
            colon = re.search(LOWER_COLON,way_tag.attrib['k'])
            
            if problem:
                continue
            elif colon:
                way_tags_dict['value'] = way_tag.attrib['v']
                way_tags_dict['id'] = element.attrib['id']
                way_tags_dict['key'] = way_tag.attrib['k'].split(":",1)[1]
                way_tags_dict['type'] = way_tag.attrib['k'].split(":",1)[0]
                tags.append(way_tags_dict)
            else:
                way_tags_dict['value'] = way_tag.attrib['v']
                way_tags_dict['id'] = element.attrib['id']
                way_tags_dict['key'] = way_tag.attrib['k']
                way_tags_dict['type'] = "regular"
                tags.append(way_tags_dict)
        
        
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
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

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
    process_map(OSM_PATH, validate=True)

