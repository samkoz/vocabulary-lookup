#Dictionary.py

import urllib2;
import xml.etree.ElementTree as ET;
#ElementTree is the whole XML file
#Element is a node in that file

#collegiate dictionary example
col_dic_example = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/test?key=3f7480b2-e927-42bd-aebe-dfab617b5acb"

#medical dictionary example
#http://www.dictionaryapi.com/api/references/medical/v2/xml/test?key=20ab3427-bf97-49c6-b248-43ddce7bfdb8

response = urllib2.urlopen(col_dic_example)
result = response.read()

# print result
#print type(result)

result_XML = ET.fromstring(result)
print type(result_XML)
print type(result_XML[0])

print result_XML.tag
entries = list(result_XML)

#need to figure out what components of the definition we want...

for entry in result_XML:
    print "ENTRY: ", entry.tag, entry.attrib, entry.text
    for definition in entry.iter():
        try:
            print definition.tag, definition.attrib, definition.text
        except:
            print definition.tag, definition.attrib, definition.text.encode('utf-8');

#sketching this up:
# Num: word, noun/verb/adj
# etymology
# definition list

# ennumerate: entry.ew.text, entry.fl.text
# entry.et.text
# for x in entry.iter('dt'): x.text

#this function should get all the variables we are interested in
def entry_maker(XML):
    entries = []
    for entry in enumerate(XML):
        entry_order = entry[0]
        entry = entry[1]
        print entry
        word = entry.find('ew').text.encode('utf-8');

        def_list = []
        for el in entry.iter('et'):
            etymology = el.text.encode('utf-8');

        for el in entry.iter('fl'):
            grammer = el.text.encode('utf-8');

        for el in entry.iter('dt'):
            df = el.text.encode('utf-8');
            df = df.replace(':', '')
            df = df.rstrip();
            if len(df )> 0:
                df = '-' + df;
                def_list.append(df);

        entries.append({'word' : word, 'order' : entry_order, 'etymology' : etymology, 'grammer' : grammer, 'definitions' : def_list});
    return entries;

definitions = entry_maker(result_XML)
for x in definitions:
    print x['etymology'];
    print x['definitions']

# for child in result_XML.iter('dt'):
#     print child.tag, child.attrib, child.text
