#Dictionary.py

import urllib2;
import xml.etree.ElementTree as ET;
#ElementTree is the whole XML file
#Element is a node in that file

#collegiate dictionary example
col_dic_example = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/test?key=3f7480b2-e927-42bd-aebe-dfab617b5acb"

#medical dictionary example
med_dic_example = "http://www.dictionaryapi.com/api/references/medical/v2/xml/test?key=20ab3427-bf97-49c6-b248-43ddce7bfdb8"

def lookup(word, dict_type):
    if dict_type == "c":
        URL_lookup = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key=3f7480b2-e927-42bd-aebe-dfab617b5acb".format(word);
    elif dict_type == "m":
        URL_lookup = "http://www.dictionaryapi.com/api/references/medical/v2/xml/{}?key=20ab3427-bf97-49c6-b248-43ddce7bfdb8".format(word);
    #print URL_lookup
    try:
        response = urllib2.urlopen(URL_lookup)
        result = ET.fromstring(response.read());
    except:
        pass
        #raise an exception here if they are not connected to the internet.
        #this will need to be passed to an above function?
        #figure this out
    return result;

#this function should get all the variables we are interested in
def entry_maker(XML):
    entries = []

    #some print statements for feedback
    #will need to erase these when running w/o command line
    # print ET.tostring(XML, encoding='utf8', method='xml')
    # print ET.tostring(XML[0], encoding='utf-8', method='xml');

    #check if not a word; then format it according to suggestion parameters
    suggestion_list = [];
    if XML[0].find('ew') is None:
        print True
        sug_list = []
        for sug in XML.iter('suggestion'):
            suggestion = sug.text.encode('utf-8');
            sug_list.append(suggestion)
        entries = [{'word' : None, 'suggestions' : sug_list}];

    #this will run if a word ia found
    else:
        for entry in enumerate(XML):
            entry_order = entry[0]
            entry = entry[1]
            word = entry.find('ew').text.encode('utf-8');

            def_list = []
            etymology = None;
            for el in entry.iter('et'):
                try:
                    etymology = el.text.encode('utf-8');
                except AttributeError:
                    continue;

            for el in entry.iter('fl'):
                grammer = el.text.encode('utf-8');

            for el in entry.iter('dt'):
                try:
                    df = el.text.encode('utf-8');
                    df = df.replace(':', '')
                    df = df.rstrip();
                    if len(df )> 0:
                        df = '-' + df;
                        def_list.append(df);
                except:
                    continue;
            entries.append({'word' : word, 'order' : entry_order, 'etymology' : etymology, 'grammer' : grammer, 'definitions' : def_list});

    return entries;


def entry_formatter(entries):
    query = entries[0]['word'];
    count = 1;
    formatted_def = ""
    #this conditional statement was added to differentiate queires with definitions vs. suggestsions
    if query != None:
        for e in entries:
            def_string = ""
            word = e['word']
            ety = e['etymology']
            gram = e['grammer']
            defs = e['definitions'];

            def_string += "{0}: {1}\nGrammer: {2}, Etymology: {3}\n".format(count, word, gram, ety);
            for d in defs:
                def_string += "{}\n".format(d);
            def_string += '\n'
            formatted_def += def_string;
            count += 1;
    else:
        formatted_def = "Word not found - listed below are some suggestions.\n"
        for e in entries:
            sugs = e['suggestions'];
            for s in sugs:
                formatted_def += "{0}: {1}\n".format(count, s);
                count += 1;
    return (query, formatted_def);

# f_entries = entry_formatter(entries);
# print f_entries;

#there are a lot of different routes to go here


#
# def main():
#     results = lookup(sys.argv[1], "collegiate")
#     try:
#         entries = entry_maker(results);
#         entries = entry_formatter(entries);
#     except AttributeError:
#         print "word not in dictionary, here are some suggestions:";
#         for sug in results.iter('suggestion'):
#             print sug.text
#
# main();




# for child in result_XML.iter('dt'):
#     print child.tag, child.attrib, child.text
