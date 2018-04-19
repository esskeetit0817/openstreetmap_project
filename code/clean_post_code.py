import xml.etree.cElementTree as ET
filename = '../dataset/shenzhen.osm'

def  is_post_code(elem):
    return(elem.attrib['k'] == "addr:postcode")

def get_clean_post_code(filename):
    new_post_code_set = []
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    post_code = tag.attrib['v']
                    
                    if 'DD' in post_code:
                        new_post_code = post_code.replace(' ', '')[2:]
                        
                        new_post_code_set.append(new_post_code) 
    return new_post_code_set

print get_clean_post_code(filename)
