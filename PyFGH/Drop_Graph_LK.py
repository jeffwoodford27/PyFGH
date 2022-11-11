from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Create object
root = Tk()

# Adjust size
root.geometry("760x760")

def plot():
    # the figure that will contain the plot
    fig = Figure(figsize=(5, 5), dpi=100)

#wfn array
    wfn = [5.620948663068036e-09, 7.516713986034454e-09, 3.5815783726449676e-08, 1.429761598530566e-08,
              4.0423797837071565e-08, 5.018620962751152e-08, 2.9200717614568785e-08, 9.90464098883949e-09,
              2.5516302823135235e-09, -1.0053198802988102e-10, 6.892598644053881e-10]

    # list of squares
    y = wfn  # wfn
    x = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(x, y)


    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


# Change the label text
def show():
    label.config(text=clicked.get())


# Dropdown menu options
wfn = [1750, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Eigen Graphs")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *wfn)
drop.pack()

# Create button, it will change label text
button = Button(root, text="click Me", command=plot).pack()

# Create Label
label = Label(root, text=" ")
label.pack()

# Execute tkinter
root.mainloop()