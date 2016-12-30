#dict_helper functions for dictionary.py
import urllib2;
import xml.etree.ElementTree as ET;

def lookup(word, dict_type):
    """uses Miriam Webster Dictionary API keys and passed word queries to get the definition of the passed word"""
    if dict_type == "c":
        URL_lookup = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key=3f7480b2-e927-42bd-aebe-dfab617b5acb".format(word);
    elif dict_type == "m":
        URL_lookup = "http://www.dictionaryapi.com/api/references/medical/v2/xml/{}?key=20ab3427-bf97-49c6-b248-43ddce7bfdb8".format(word);

    response = urllib2.urlopen(URL_lookup)
    result = ET.fromstring(response.read());
    return result;

def entry_maker(XML):
    entries = []
    suggestion_list = [];
    if XML[0].find('ew') is None:
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
            formatted_def += def_string +"\n"
            count += 1;
    else:
        formatted_def = "Word not found - listed below are some suggestions.\n"
        for e in entries:
            sugs = e['suggestions'];
            for s in sugs:
                formatted_def += "{0}: {1}\n".format(count, s);
                count += 1;
    return (query, formatted_def.rstrip());
