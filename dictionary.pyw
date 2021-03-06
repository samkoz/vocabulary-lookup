from Tkinter import *
import traceback;
import dict_helpers;
import save_helpers;

class App:
    """contains all code for the GUI display and functionality"""
    def __init__(self, master):
        self.query = ''
        self.definition = ''
        self.valid_entry = None;
        self.frame = Frame(master)
        self.frame.pack();

        self.look_up_entry = Entry(self.frame)
        self.look_up_entry.bind("<Return>", self.look_up)
        self.look_up_entry.bind("<Control-a>", self.select_text)
        self.look_up_entry.pack();
        self.look_up_entry.delete(0, END)

        self.look_up_button = Button(self.frame, text = "Look up word definition")
        self.look_up_button.bind("<Button-1>", self.look_up);
        self.look_up_button.bind("<Return>", self.look_up);
        self.look_up_button.pack(side=TOP);

        self.save_result_button = Button(self.frame, text="Save result", command=self.save_result);
        self.save_result_button.bind("<Return>", self.save_shortcut)
        self.save_result_button.pack(side=TOP);

        self.quit_button = Button(self.frame, text="Quit", command=self.frame.quit);
        self.quit_button.bind("<Return>", lambda e: self.frame.quit())
        self.quit_button.pack(side=TOP);

        self.dict_toggle = IntVar();
        #this will be 1 if the button is selected; otherwise 0
        self.check_button = Checkbutton(self.frame, text="Medical Dictionary", variable=self.dict_toggle);
        self.check_button.bind("<Return>", self.checkbox_shortcut)
        self.check_button.pack();

        self.text_display = Text(self.frame, wrap=WORD);
        self.text_display.pack(side=BOTTOM)
        self.text_display.insert(END, '-type a word above and press enter to get its definition.\n-it will search the normal, collegiate dictionary by default.\n-check the medical dictionary to use that instead.')

    def save_shortcut(self, event):
        """key binding to save a word-def pair when enter is pressed on the save button"""
        self.save_result()

    def select_text(self, event):
        """key binding to select all text in entry widget on ctrl+a"""
        self.look_up_entry.select_range(0, END);
        return "break"

    def checkbox_shortcut(self, event):
        """key binding to toggle checkbox w/ enter key"""
        if self.dict_toggle.get() == 1:
            self.check_button.deselect();
        else:
            self.check_button.select();

    def look_up(self, event):
        """function to lookup event when enter is pressed on entry widget"""
        word = self.look_up_entry.get()
        try:
            if self.med_dict_check():
                lookup_URL = dict_helpers.lookup(word, "m");
            else:
                lookup_URL = dict_helpers.lookup(word, "c");

            results = dict_helpers.entry_maker(lookup_URL)
            formatted_results = dict_helpers.entry_formatter(results)

            #update definition and query to save them if user decides to add them
            self.definition_update(formatted_results);
            self.query_update(formatted_results);

            #display results
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, formatted_results[1])
            self.valid_entry = True;

        except Exception as e:
            #this error occurs if no text is entered or there are no suggestions for a word
            if type(e).__name__ == 'IndexError':
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-you either misspelled a word so badly that there are no suggested corrections or you did not enter a word to search.\n-type a word you would like to look up the definition for and press enter.")

            #this is for multiple word entries
            elif type(e).__name__ == "ParseError":
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-did you enter more than one word?\n-only search one word at a time.")

            #no internet connection error
            elif type(e).__name__ == "URLError":
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-you are not connected to the internet...")

            #will display traceback for unaccounted errors for future debugging
            else:
                tb = traceback.format_exc();
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, tb);

            self.valid_entry = False;
            self.query = word;

    def save_result(self):
        """function to save results in a csv file\ndoes not save if no word is entered, the word is already in the csv file or the csv file is open (i.e. permissions denied)\nrelies on helper functions defined in save_helpers.py"""
        try:
            if self.query == "":
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-enter a word you would like to define");
            elif save_helpers.word_check(self.query):
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-the word '{0}' is already in your vocabulary dictionary.".format(self.query));
            else:
                if self.valid_entry == True:
                    save_helpers.add_word(self.query, self.definition)
                    self.text_display.delete(1.0, END);
                    self.text_display.insert(END, "-the word '{0}' was saved to your vocabulary dictionary".format(self.query));
                else:
                    self.text_display.delete(1.0, END);
                    self.text_display.insert(END, "-the word '{0}' is an invalid entry\n-look up the word to see why".format(self.query));
        except IOError as e:
            if str(e) == "[Errno 13] Permission denied: 'dictionary.csv'":
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "'{0}' WAS NOT saved to your vocabulary dictionary!!!\n-you need to close your dictionary.csv file to save words.".format(self.query));

    def med_dict_check(self):
        """helper function that returns True if the medical dictionary checkbox is selected and false if not"""
        toggle = self.dict_toggle.get()
        if toggle == 1:
            return True;
        else:
            return False;

    def definition_update(self, results):
        """updates app class' instance variable of the definition for the current query's definition"""
        self.definition = results[1];

    def query_update(self, results):
        """updates app class' instanace variable of the query to match the current query"""
        self.query = results[0];

root = Tk()
root.title("Dictionary")
app = App(root);

root.mainloop()
root.destroy();
