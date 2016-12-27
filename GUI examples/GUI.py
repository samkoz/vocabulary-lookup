from Tkinter import *

#initialize Tkinter
root = Tk();

#create a label widget as a child of the root widget
w = Label(root, text="Hello, world!");

#pack tells it to size itself to fit the given text
w.pack()

#initialize event loop
root.mainloop();
