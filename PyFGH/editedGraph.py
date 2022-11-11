from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class buttonclass:
    def __init__(self, window, title, x, y):
        self.window = window
        self.button = Button(master=window,
                     command=self.plot,  # show graph
                     height=2,
                     width=10,
                     text=title)
        self.x = x
        self.y = y
    # plot function is created for
    # plotting the graph in
    # tkinter window
    def plot(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5), dpi=100)

    #wfn array

        # list of squares
        y = self.y
        x = self.x
        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(x, y)


        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       self.window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

        return

# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("500x500")

x = [1,2,3,4,5,6,7,8,9,10,11]
y1 = [1,2,3,4,5,6,7,8,9,10,11]
y2 = [11,10,9,8,7,6,5,4,3,2,1]

button_list = []
button_list.append(buttonclass(window, "Plot 1", x, y1))
button_list.append(buttonclass(window, "Plot 2", x, y2))

for btn in button_list:
    btn.button.pack()
# place the button
# in main window

# run the gui
window.mainloop()
# PLOT AS THE WHY VARIABLE
# X VARIABLES WILL BE 1 - 11
# ACTIVITY LOG BOTH THIS WEEK AND NEXT
# PLUS SEND TO ACTIVITY LOG
#
# x = 1, 2, 3, 4, 5, 6, 7, 8, 9, 11
# # adding the subplot
# plot1 = fig.add_subplot(x)
#
# # plotting the graph
# plot1.plot(x, y)