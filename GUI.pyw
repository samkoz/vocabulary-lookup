from Tkinter import *
import traceback;
import dictionary;


class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack();

        self.look_up_entry = Entry(self.frame)
        self.look_up_entry.pack();
        self.look_up_entry.delete(0, END)

        self.look_up_button = Button(self.frame, text="Look up word", command=self.look_up);
        self.look_up_button.pack(side=TOP)

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

    def look_up(self):
        try:
            word = self.look_up_entry.get()
            if self.med_dict_check():
                lookup_URL = dictionary.lookup(word, "m");
            else:
                lookup_URL = dictionary.lookup(word, "c");
            results = dictionary.entry_maker(lookup_URL)
            formatted_results = dictionary.entry_formatter(results)
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, formatted_results[1])
        except Exception as e:
            if type(e).__name__ == 'IndexError':
                pass;
            elif type(e).__name__ == "ParseError":
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, "-did you enter more than one word?\n-only enter one word at a time into the above query.")
            else:
                tb = traceback.format_exc();
                self.text_display.delete(1.0, END);
                self.text_display.insert(END, tb);


    def save_result(self):
        pass;

    def med_dict_check(self):
        toggle = self.dict_toggle.get()
        if toggle == 1:
            return True;
        else:
            return False;

root = Tk()
app = App(root);

root.mainloop()
root.destroy();
