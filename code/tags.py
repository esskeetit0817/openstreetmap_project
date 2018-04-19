import xml.etree.cElementTree as ET
import pprint
import re

filename_1 = '../dataset/sample.osm'
filename_2 = '../dataset/shenzhen.osm'

def count_tags(filename):
    tags={}
    tree = ET.iterparse(filename,events=('start',))
    for event,elem in tree:
        if elem.tag not in tags.keys():
            tags[elem.tag] =1
        else:
            tags[elem.tag] +=1
    return tags
#print count_tags(filename)

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


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

def find_problem_key(filename):
    for event, element in ET.iterparse(filename):
        if element.tag == "tag":
            k = element.attrib['k']
            
            if re.search(problemchars,k):
                problem_key = k
    return problem_key

def process_problematic_keys(filename):
    if find_problem_key(filename):
        problem_key = find_problem_key(filename)
        temp_key = problem_key.split(" ")
        new_key = "_".join(temp_key).split(':')[1]
    return new_key 


print "the key type in sample.osm dataset:" ,process_map(filename_1)
print "the key type in shenzhen.osm dataset:" ,process_map(filename_2)
print find_problem_key(filename_2)
print process_problematic_keys(filename_2)


