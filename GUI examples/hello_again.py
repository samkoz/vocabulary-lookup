from Tkinter import *

class App:
    def __init__(self, master):
        #parent widget (master) is instantiated in a frame widget (simple container)
        self.frame = Frame(master)
        #pack makes the frame visible
        self.frame.pack()

        #Create two button widgets as children to the frame
        #a lot of options are specified; by default child widgets are placed relative to their parent
        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.pack(side=LEFT);

        self.hi_there = Button(self.frame, text = "Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT);

    def say_hi(self):
        new_button = Button(self.frame, text="another Button")
        new_button.pack(side=LEFT);


root = Tk()

app = App(root);

root.mainloop()
root.destroy();
