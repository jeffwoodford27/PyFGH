import multiprocessing
import sys
import tkinter
import tkinter as tk
from fileinput import filename
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import os

"""
The code in this file is for a gui (graphic user interface) application. This code is written with the tkinter library framework.
Also go back through and make better variable names instead of alphabetic letters.
Author: Josiah Randleman
"""

# Creating tkinter window
window = tk.Tk()
style = Style()
window.title('PyFGH')
window.geometry('910x425')

# Water molecule icon in the top left conner
window.iconbitmap(default='icon.ico')

# label text for title
ttk.Label(window, text="A Python implementation of the Fourier Grid Hamiltonian method.",
          background='green', foreground="white",
          font=("Times New Roman", 15)).place(x=200, y=0)

# label
ttk.Label(window, text="Computer Cores:",
          font=("Times New Roman", 10)).place(x=10, y=50)

# Combobox creation
n = tk.StringVar()
cores = ttk.Combobox(window, width=10, textvariable=n)


# definition for calculating core counts.
# TODO: make a better for loop. Include numbers that go up to the core count!!! For instance 12 cores, include 1-12 in choice box!!!
def cpu_count():
    for x in range(multiprocessing.cpu_count()):
        cores["values"] = (x + 1)


# Label
ttk.Label(window, text="Molecule Specification:", font=("Times New Roman", 10)).place(x=200, y=50)
m = tk.StringVar()
molecule = ttk.Combobox(window, width=10, textvariable=m)

# creates values inside of the choice box
molecule["values"] = u'H\u2082O'

# Label
ttk.Label(window, text="Q\u2081:", font=("Times New Roman", 15)).place(x=425, y=47)
n = tk.StringVar()
q_equation1 = ttk.Combobox(window, width=15, textvariable=n)

# creates values inside of the choice box
q_equation1["values"] = ('OH\u2081 Bond Stretch', 'OH\u2082 Bond Stretch', 'Symmetric Stretch', 'Asymmetric Stretch')

"""
btn = ttk.Button(window, text="Get Value", command=return_value)
btn.place(relx="0.5", rely="0.1")
"""

# Label
ttk.Label(window, text="Q\u2082:", font=("Times New Roman", 15)).place(x=590, y=47)
f = tk.StringVar()
q_equation2 = ttk.Combobox(window, width=15, textvariable=f)

# creates values inside of the choice box
q_equation2["values"] = ('OH\u2081 Bond Stretch', 'OH\u2082 Bond Stretch', 'Symmetric Stretch', 'Asymmetric Stretch')

# Label
ttk.Label(window, text="Q\u2083:", font=("Times New Roman", 15)).place(x=755, y=47)
f = tk.StringVar()
q_equation3 = ttk.Combobox(window, width=15, textvariable=f)

# creates values inside of the choice box
q_equation3["values"] = ('Angle', 'Cosine')

# Label
ttk.Label(window, text="N\u2081:", font=("Times New Roman", 15)).place(x=10, y=98)
d = tk.StringVar()
N1text = ttk.Combobox(window, width=15, textvariable=d)

# Entry
text1 = ttk.Entry(window, font=("Times New Roman", 10))
c = tk.StringVar()
N1box = ttk.Combobox(window, textvariable=c)

# Label
ttk.Label(window, text="L\u2081:", font=("Times New Roman", 15)).place(x=155, y=98)
h = tk.StringVar()
L1text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
text2 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
L1box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="N\u2082:", font=("Times New Roman", 15)).place(x=310, y=98)
h = tk.StringVar()
N2text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
text3 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
N2box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="L\u2082:", font=("Times New Roman", 15)).place(x=465, y=98)
h = tk.StringVar()
L2text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
text4 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
L2box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="N\u2083:", font=("Times New Roman", 15)).place(x=615, y=98)
h = tk.StringVar()
N3text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
text5 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
N3box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="L\u2083:", font=("Times New Roman", 15)).place(x=770, y=98)
h = tk.StringVar()
L3text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
text6 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
L3box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="Equilibrium Coordinates:", font=("Times New Roman", 10)).place(x=645, y=155)


# Allows the user to chose a file in their file explorer
def open_file():
    global filename
    tkinter.Tk().withdraw()
    filename = askopenfilename()
    print(filename)


# This Button works!!!
open = tk.Button(window, text='Open', bd='5', bg='black', fg='white',
                 command=open_file).place(x=795, y=150)

# Label
# TODO: look back at the slides in the chemistry google drive. When user selects an approximation, display an image of the selected equation!!!
ttk.Label(window, text="T:", font=("Times New Roman", 20)).place(x=50, y=150)
b = tk.StringVar()
t = ttk.Combobox(window, width=15, textvariable=b)

# creates values inside of the choice box
t["values"] = ('None', 'Approximation 1', 'Approximation 2', 'Approximation 3', 'Approximation 4', 'Approximation 5')

# Label
ttk.Label(window, text="G:", font=("Times New Roman", 20)).place(x=405, y=150)
c = tk.StringVar()
g = ttk.Combobox(window, width=15, textvariable=c)

# creates values inside of the choice box
g["values"] = 'q(x) = x', 'q(x) = x^2', 'q(x) = sinx', 'q(x) = cosx', 'Let us choose'

# TODO: if the user selects read from a file or compute on the fly disable the q, n, and l buttons!!!
# Label
ttk.Label(window, text="V for Q\u2081:", font=("Times New Roman", 15)).place(x=1, y=205)
d = tk.StringVar()
v1 = ttk.Combobox(window, width=32, textvariable=d)

v1[
    "values"] = 'Model-Harmonic Oscillator', 'Model-Morse Oscillator'

# Label
ttk.Label(window, text="V for Q\u2082:", font=("Times New Roman", 15)).place(x=305, y=205)
d = tk.StringVar()
v2 = ttk.Combobox(window, width=32, textvariable=d)

v2[
    "values"] = 'Model-Harmonic Oscillator', 'Model-Morse Oscillator'

ttk.Label(window, text="V for Q\u2083:", font=("Times New Roman", 15)).place(x=615, y=205)
d = tk.StringVar()
v3 = ttk.Combobox(window, width=32, textvariable=d)

v3[
    "values"] = 'Model-Harmonic Oscillator', 'Model-Morse Oscillator'

# Button
exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                 command=window.destroy).place(x=365, y=260)


def apioutput():
    print(molecule.get())
    print(q_equation1.get())
    print(q_equation2.get())
    print(q_equation3.get())
    print(text1.get())
    print(text2.get())
    print(text3.get())
    print(text4.get())
    print(text5.get())
    print(text6.get())
    print(t.get())
    print(g.get())
    print(v1.get())
    print(v2.get())
    print(v3.get())
    print(filename)


x1 = q_equation1.get()
y = 85


def output():
    if q_equation1.get() == 'OH\u2081 Bond Stretch' and q_equation2.get() == 'OH\u2081 Bond Stretch':
        messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")

    elif q_equation1.get() == 'OH\u2082 Bond Stretch' and q_equation2.get() == 'OH\u2082 Bond Stretch':
        messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")
    else:
        box: bool = tk.messagebox.askyesno("PyFGH", "Would you like to save the data to a text file?")
        if box:
            print('This yes button works')
        else:
            print('The no button works')
            apioutput()
            window.destroy()


calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                      command=output).place(x=420, y=250)


# This will clear the data in the choice boxes  !!! Clear N1 and L2 choice boxes !!!
# This definition works! This clears everything in the window!!!
def clear_data():
    cores.set('')
    molecule.set('')
    q_equation1.set('')
    q_equation2.set('')
    q_equation3.set('')
    t.set('')
    g.set('')
    v1.set('')
    v2.set('')
    v3.set('')
    text1.delete(0, END)
    text2.delete(0, END)
    text3.delete(0, END)
    text4.delete(0, END)
    text5.delete(0, END)
    text6.delete(0, END)


clear = tk.Button(window, text='Clear', bd='10', bg='blue', fg='white',
                  command=clear_data).place(x=525, y=260)


def t0():
    box = tkinter.Tk()
    box.title('PyFGH')
    box.geometry('500x500')
    canvas = tkinter.Canvas(box, width=300, height=300)
    canvas.pack()
    img = tkinter.PhotoImage(file="t0.png")
    canvas.create_image(50, 15, anchor=NW, image=img)
    box.mainloop()


tbutton = tk.Button(window, text='Display T equation', bd='10', bg='orange', fg='white',
                    command=t0).place(x=232, y=260)

readbutton = tk.Button(window, text='Read Structures and Energies from File', bd='10', bg='gray', fg='white',
                       command=open_file).place(x=360, y=320)

compute = tk.Button(window, text='Compute on the fly', bd='10', bg='gray', fg='white',
                    command=open_file).place(x=410, y=370)

# Adding combobox drop down list
# cores['values'] = (multiprocessing.cpu_count())
cpu_count()
cores.place(x=105, y=50)
cores.current()
molecule.place(x=330, y=50)
molecule.current()
q_equation1.place(x=455, y=50)
q_equation1.current()
q_equation2.place(x=620, y=50)
q_equation2.current()
q_equation3.place(x=785, y=50)
q_equation3.current()
t.place(x=80, y=157)
t.current()
g.place(x=440, y=157)
g.current()
v1.place(x=77, y=207)
v1.current()
v2.place(x=380, y=207)
v2.current()
v3.place(x=690, y=207)
v3.current()
text1.place(x=40, y=100, width=100)
text2.place(x=185, y=100, width=100)
text3.place(x=340, y=100, width=100)
text4.place(x=495, y=100, width=100)
text5.place(x=645, y=100, width=100)
text6.place(x=800, y=100, width=100)
window.mainloop()
