#save helper functions for dictionary.py
import csv;
import pandas as pd;

def add_word(word, definition):
    """will add word to csv file"""
    with open('dictionary.csv', 'ab+') as csvfile:
        dict_writer = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
        dict_writer.writerow([word, definition])

def word_check(word):
    """will check csv file to see if the current word-definition pair is present; it will add the word if not\na csv file (dictionary.csv) will be created if one does not already exist."""
    #this exception  was implemented to handle creation of the csv file
    try:
        dictionary = pd.read_csv('dictionary.csv', index_col=0);
        if word in dictionary.index:
            return True;
        else:
            return False;
    except IOError:
        return False;
