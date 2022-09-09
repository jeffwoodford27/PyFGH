
from tkinter import *
from PIL import ImageTk,Image

import tkinter
import tkinter as tk


def test():
    root = tkinter.Toplevel()
    canvas = Canvas(root, width=350, height=350)
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open("Dog.png"))
    canvas.create_image(20, 20, anchor=NW, image=img)
    root.mainloop()


root = Tk()
canvas = Canvas(root, width=350, height=450)
canvas.pack()
label = Label(canvas, text="Click the Button to display an image", font=('Helvetica 17 bold'))
label.pack(pady=30)

help = tk.Button(canvas, text='Help', bd='10', bg='#F9BB46', fg='white',
                     command=test).place(x=20, y=20)
root.mainloop()
