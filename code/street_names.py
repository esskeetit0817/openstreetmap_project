#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
filename = '../dataset/shenzhen.osm'

def is_street_name(elem):                                                              
    return(elem.attrib['k'] == 'addr:street')   
    
def street_names(filename):
    for event, elem in ET.iterparse(filename,events=("start",)): 
        if elem.tag == "node" or elem.tag == "way":                       
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    print tag.attrib['v']
street_names(filename)
