from Tkinter import *
import dictionary;

class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack();

        self.look_up_entry = Entry(self.frame)
        self.look_up_entry.pack();
        self.look_up_entry.delete(0, END)
        self.look_up_entry.insert(0, "enter a word to search")

        self.look_up_button = Button(self.frame, text="Look up word", command=self.look_up);
        self.look_up_button.pack(side=LEFT)

        self.save_result_button = Button(self.frame, text="Save result", command=self.save_result);
        self.save_result_button.pack(side=LEFT);

        self.quit_button = Button(self.frame, text="Quit", command=self.frame.quit);
        self.quit_button.pack(side=LEFT);

    def look_up(self):
        word = self.look_up_entry.get()
        lookup_URL = dictionary.lookup(word, "collegiate");
        results = dictionary.entry_maker(lookup_URL)
        formatted_results = dictionary.entry_formatter(results)
        print formatted_results;




    def save_result(self):
        pass;

root = Tk()
app = App(root);

root.mainloop()
root.destroy();
