# Import the required libraries
import tkinter
from tkinter import *
from tkinter import ttk

# Create an instance of Tkinter Frame
win = Tk()

# Set the geometry of Tkinter Frame
win.geometry("700x350")

# Add a canvas widget
canvas = Canvas(win, width=350)


# Define a function for dog
def Dog():
    frame = tkinter.Toplevel()
    frame.title = "Dog"
    frame.geometry = "500 X 500"
    canvas = tkinter.Canvas(frame, width=500, height=500)
    img = tkinter.PhotoImage(file='Dog.png')
    canvas.create_image(500, 500, anchor=NW, image=img)
    canvas.pack()


# Add a Label widget in the Canvas
label = Label(canvas, text="Click the Button to display an image", font=('Helvetica 17 bold'))
label.pack(pady=30)

# Create a button in canvas widget
ttk.Button(canvas, text="Dog", command=Dog).pack()
canvas.pack()

win.mainloop()
