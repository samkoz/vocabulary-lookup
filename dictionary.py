#Dictionary.py

import urllib2;
import xml.etree.ElementTree as ET;
import sys;
#ElementTree is the whole XML file
#Element is a node in that file

#collegiate dictionary example
col_dic_example = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/test?key=3f7480b2-e927-42bd-aebe-dfab617b5acb"

#medical dictionary example
med_dic_example = "http://www.dictionaryapi.com/api/references/medical/v2/xml/test?key=20ab3427-bf97-49c6-b248-43ddce7bfdb8"

def lookup(word, dict_type):
    """Will keep a placeholder for dict type right now"""
    URL_lookup = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key=3f7480b2-e927-42bd-aebe-dfab617b5acb".format(word);
    print URL_lookup
    response = urllib2.urlopen(URL_lookup)
    result = ET.fromstring(response.read());
    return result;

#this function should get all the variables we are interested in
def entry_maker(XML):
    entries = []
    for entry in enumerate(XML):
        entry_order = entry[0]
        entry = entry[1]
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

#sketching this up:
# Num: word, noun/verb/adj
# etymology
# definition list

# ennumerate: entry.ew.text, entry.fl.text
# entry.et.text
# for x in entry.iter('dt'): x.text

# entries = entry_maker(result_XML);

def entry_formatter(entries):
    count = 1;
    formatted_def = ""
    for e in entries:
        def_string = ""
        word = e['word']
        ety = e['etymology']
        gram = e['grammer']
        defs = e['definitions'];

        def_string += "{0}: {1}\n Grammer: {2}, Etymology: {3}\n".format(count, word, gram, ety);
        for d in defs:
            def_string += "{}\n".format(d);
        def_string += '\n'
        formatted_def += def_string;
        count += 1;
    return (word, formatted_def);

# f_entries = entry_formatter(entries);
# print f_entries;

#there are a lot of different routes to go here



def main():
    results = lookup(sys.argv[1], "collegiate")
    try:
        entries = entry_maker(results);
        entries = entry_formatter(entries);
    except AttributeError:
        print "word not in dictionary, here are some suggestions:";
        for sug in results.iter('suggestion'):
            print sug.text

main();




# for child in result_XML.iter('dt'):
#     print child.tag, child.attrib, child.text
