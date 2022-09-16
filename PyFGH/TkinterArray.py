# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
# this is the array and each element will be a button
num1 = [34, 42, 72, 99, 100]
# creates a Tk() object
master = Tk()
# sets the geometry of main
# root window
master.geometry("400x400")
# function to open a new window
# on a button click

class OpenNewWindow:
    def __init__(self, master, num):
        self.master = master
        self.num = num
        self.graphimage = None

    def generateGraph(self):
#        method that will generate a graph based on  self.num
#        y = x^num
#        store that image in self.graphimage

    def displayWindow(self):
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        title_str = "New Window"+str(self.num)
        newWindow.title(title_str)

        # sets the geometry of toplevel
        newWindow.geometry("200x200")

        # A Label widget to show in toplevel
        Label(newWindow,
              text="This is a new window").pack()

        if self.graphimage = None:
            self.generateGraph()

#        pseudocode: put that image that is now guarnateed to be in self.graphimage into the window


'''
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
'''

label = Label(master,
        text="This is the main window")


# a button widget which will open a
# new window on button click
btnMain = Button(master, text="This will deisplay a graph")
               #,command=Graph)

btn = []
windows = []
N = len(num1)
for i in range(N):
    windows.append(OpenNewWindow(master,num1[i]))
    btn.append(Button(master,text=num1[i],command=windows[i].displayWindow))
    btn[i].pack(pady=10)


'''
btn = Button(master, text=num1[0], command=openNewWindow)
btn.pack(pady=10)

btn1 = Button(master, text=num1[1], command=openNewWindow)
btn1.pack(pady=10)

btn2 = Button(master, text=num1[2], command=openNewWindow)
btn2.pack(pady=10)
'''

# mainloop, runs infinitely
mainloop()