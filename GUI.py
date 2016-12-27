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

        self.text_display = Text(self.frame)
        self.text_display.pack(side=BOTTOM)
        self.text_display.insert(END, 'type a word above and press enter to get its definition.')

    def look_up(self):
        try:
            word = self.look_up_entry.get()
            lookup_URL = dictionary.lookup(word, "collegiate");
            results = dictionary.entry_maker(lookup_URL)
            formatted_results = dictionary.entry_formatter(results)
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, formatted_results[1])
        except Exception as e:
            tb = traceback.format_exc();
            self.text_display.delete(1.0, END);
            self.text_display.insert(END, tb);


    def save_result(self):
        pass;

root = Tk()
app = App(root);

root.mainloop()
root.destroy();
