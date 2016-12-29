from Tkinter import *
import traceback;
import dictionary;
import save_result;

class App:
    def __init__(self, master):
        self.query = ''
        self.definition = ''
        self.frame = Frame(master)
        self.frame.pack();

        self.look_up_entry = Entry(self.frame)
        self.look_up_entry.bind("<Return>", self.look_up)
        self.look_up_entry.bind("<Control-a>", self.select_text)
        self.look_up_entry.pack();
        self.look_up_entry.delete(0, END)

        self.save_result_button = Button(self.frame, text="Save result", command=self.save_result);
        self.save_result_button.pack(side=TOP);

        self.quit_button = Button(self.frame, text="Quit", command=self.frame.quit);
        self.quit_button.pack(side=TOP);

        self.dict_toggle = IntVar();
        #this will be 1 if th button is selected; otherwise 0
        self.check_button = Checkbutton(self.frame, text="Medical Dictionary", variable=self.dict_toggle);
        self.check_button.pack();

        self.text_display = Text(self.frame)
        self.text_display.pack(side=BOTTOM)
        self.text_display.insert(END, '-type a word above and press enter to get its definition.\n-it will search the normal, collegiate dictionary by default.\n-check the medical dictionary to use that instead.')

    def select_text(self, event):
        self.look_up_entry.select_range(0, END);
        return "break"

    def look_up(self, event):
        try:
            word = self.look_up_entry.get()
            if self.med_dict_check():
                lookup_URL = dictionary.lookup(word, "m");
            else:
                lookup_URL = dictionary.lookup(word, "c");

            results = dictionary.entry_maker(lookup_URL)
            formatted_results = dictionary.entry_formatter(results)

            #update definition and query to save them if user decides to add them
            self.definition_update(formatted_results);
            self.query_update(formatted_results);

            #display results
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, formatted_results[1])

        except Exception as e:
            #this error occurs if no text is entered OR if there are no suggesions...
            #NEED TO ACCOUNT FOR SUGGESTIONS COMPONENT
            if type(e).__name__ == 'IndexError':
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-you either misspelled a word so badly that there are no suggested corrections or you did not enter a word to search.\n-type a word you would like to look up the definition for and press enter.")
            elif type(e).__name__ == "ParseError":
                #this is for multiple word entries
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-did you enter more than one word?\n-only enter one word at a time into the above query.")
            else:
                #general print for all error statements at this point
                tb = traceback.format_exc();
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, tb);


    def save_result(self):
        if save_result.word_check(self.query):
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, "-the word {0} is already in your vocabulary dictionary.".format(self.query));
        else:
            save_result.add_word(self.query, self.definition)
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, "-the word {0} was saved to your vocabulary dictionary".format(self.query));

    def med_dict_check(self):
        toggle = self.dict_toggle.get()
        if toggle == 1:
            return True;
        else:
            return False;

    def definition_update(self, results):
        self.definition = results[1];

    def query_update(self, results):
        self.query = results[0];

root = Tk()
app = App(root);

root.mainloop()
root.destroy();
