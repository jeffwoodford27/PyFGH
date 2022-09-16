# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
# this is the array and each element will be a button
num1 = [34, 6, 72]
# creates a Tk() object
master = Tk()
# sets the geometry of main
# root window
master.geometry("400x400")
# function to open a new window
# on a button click
def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")

    # sets the geometry of toplevel
    newWindow.geometry("200x200")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="This is a new window").pack()


label = Label(master,
        text="This is the main window")


# a button widget which will open a
# new window on button click
btnMain = Button(master, text="This will deisplay a graph")
               #,command=Graph)
btn = Button(master, text=num1[0], command=openNewWindow)
btn.pack(pady=10)

btn1 = Button(master, text=num1[1], command=openNewWindow)
btn1.pack(pady=10)

btn2 = Button(master, text=num1[2], command=openNewWindow)
btn2.pack(pady=10)

# mainloop, runs infinitely
mainloop()