#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xml.etree.cElementTree as ET
filename_1 = '../dataset/sample.osm'
filename_2 = '../dataset/shenzhen.osm'
def is_post_code(elem):
    return(elem.attrib['k'] == "addr:postcode")

def problematic_post_code(filename):
    p_post_code_set = []
    for event, elem in ET.iterparse(filename, events=("start",)): 
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"): 
                if is_post_code(tag):
                    post_code = tag.attrib['v'] 
                    
                    if len(str(post_code)) != 6: 
                        p_post_code_set.append(post_code)
    return p_post_code_set

print problematic_post_code(filename_1)
print problematic_post_code(filename_2)
