#save result

#plan:
#read an existing csv file with pandas
#check to make sure the word of interest is not already in the csv file
#display a message that the entry already exists in the file
#write the entry to csv file if it is not in there

import csv;
import pandas as pd;

def add_word(word, definition):
    with open('dictionary.csv', 'ab+') as csvfile:
        dict_writer = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
        dict_writer.writerow([word, definition])
    #need GUI to display that it has been added

def word_check(word):
    dictionary = pd.read_csv('dictionary.csv', index_col=0);
    print dictionary.index;
    if word in dictionary.index:
        return True;
    else:
        return False;
        #need GUI to display word already exists
