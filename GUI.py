import multiprocessing

import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
from util import InputData
from util import model_objects
import numpy as np



"""
The code in this file is for a gui (graphic user interface) application. This code is written with the tkinter library framework.
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
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
molecule = ttk.Combobox(window, width=10, textvariable=m, state='readonly')

# creates values inside of the choice box
molecule["values"] = u'H\u2082O'

# Label
ttk.Label(window, text="Q\u2081:", font=("Times New Roman", 15)).place(x=425, y=47)
n = tk.StringVar()
q_equation1 = ttk.Combobox(window, width=15, textvariable=n)

# creates values inside of the choice box
q_equation1["values"] = (
    'OH\u2081 Bond Stretch', 'OH\u2082 Bond Stretch', 'Symmetric Stretch', 'Asymmetric Stretch')

"""
btn = ttk.Button(window, text="Get Value", command=return_value)
btn.place(relx="0.5", rely="0.1")
"""

# Label
ttk.Label(window, text="Q\u2082:", font=("Times New Roman", 15)).place(x=590, y=47)
f = tk.StringVar()
q_equation2 = ttk.Combobox(window, width=15, textvariable=f)

# creates values inside of the choice box
q_equation2["values"] = (
    'OH\u2081 Bond Stretch', 'OH\u2082 Bond Stretch', 'Symmetric Stretch', 'Asymmetric Stretch')

# Label
ttk.Label(window, text="Q\u2083:", font=("Times New Roman", 15)).place(x=755, y=47)
f2 = tk.StringVar()
q_equation3 = ttk.Combobox(window, width=15, textvariable=f2)

# creates values inside of the choice box
q_equation3["values"] = ('Angle', 'Cosine')

# Label
ttk.Label(window, text="N\u2081:", font=("Times New Roman", 15)).place(x=10, y=98)
d = tk.StringVar()
N1text = ttk.Combobox(window, width=15, textvariable=d)

# Entry
N1 = ttk.Entry(window, font=("Times New Roman", 10))
c = tk.StringVar()
N1box = ttk.Combobox(window, textvariable=c)

# Label
ttk.Label(window, text="L\u2081:", font=("Times New Roman", 15)).place(x=155, y=98)
h = tk.StringVar()
L1text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
L1 = ttk.Entry(window, font=("Times New Roman", 10))
zz = tk.StringVar()
L1box = ttk.Combobox(window, textvariable=zz)

# Label
ttk.Label(window, text="N\u2082:", font=("Times New Roman", 15)).place(x=310, y=98)
h = tk.StringVar()
N2text = ttk.Combobox(window, width=15, textvariable=h)

# Entry
N2 = ttk.Entry(window, font=("Times New Roman", 10))
i = tk.StringVar()
N2box = ttk.Combobox(window, textvariable=i)

# Label
ttk.Label(window, text="L\u2082:", font=("Times New Roman", 15)).place(x=465, y=98)
h2 = tk.StringVar()
L2text = ttk.Combobox(window, width=15, textvariable=h2)

# Entry
L2 = ttk.Entry(window, font=("Times New Roman", 10))
i2 = tk.StringVar()
L2box = ttk.Combobox(window, textvariable=i2)

# Label
ttk.Label(window, text="N\u2083:", font=("Times New Roman", 15)).place(x=615, y=98)
h3 = tk.StringVar()
N3text = ttk.Combobox(window, width=15, textvariable=h3)

# Entry
N3 = ttk.Entry(window, font=("Times New Roman", 10))
i4 = tk.StringVar()
N3box = ttk.Combobox(window, textvariable=i4)

# Label
ttk.Label(window, text="L\u2083:", font=("Times New Roman", 15)).place(x=770, y=98)
h6 = tk.StringVar()
L3text = ttk.Combobox(window, width=15, textvariable=h6)

# Entry
L3 = ttk.Entry(window, font=("Times New Roman", 10))
i5 = tk.StringVar()
L3box = ttk.Combobox(window, textvariable=i5)

# Label
ttk.Label(window, text="Equilibrium Coordinates:", font=("Times New Roman", 10)).place(x=645, y=155)


# Allows the user to chose a file in their file explorer
# TODO: Error somewhere in this. When you select to open a file, then run the code in API.py the variables do not transfer. Fix this!!!
def open_file():
    global filename
    tkinter.Tk().withdraw()
    filename = askopenfilename()


# This Button works!!!
open = tk.Button(window, text='Open', bd='5', bg='black', fg='white',
                 command=open_file).place(x=795, y=150)

# Label
# TODO: look back at the slides in the chemistry google drive. When user selects an approximation, display an image of the selected equation!!! Cosmetic!
ttk.Label(window, text="T:", font=("Times New Roman", 20)).place(x=50, y=150)
b = tk.StringVar()
t = ttk.Combobox(window, width=15, textvariable=b)

# creates values inside of the choice box
t["values"] = (
    'None', 'Approximation 1', 'Approximation 2', 'Approximation 3', 'Approximation 4', 'Approximation 5')

# Label
ttk.Label(window, text="G:", font=("Times New Roman", 20)).place(x=405, y=150)
c = tk.StringVar()
g = ttk.Combobox(window, width=15, textvariable=c)

# creates values inside of the choice box
g["values"] = 'q(x) = x', 'q(x) = x^2', 'q(x) = sinx', 'q(x) = cosx', 'Let us choose'

# TODO: if the user selects read from a file or compute on the fly disable the q, n, and l buttons!!!
# Label
v = []
value = 1
for i in range(3):
    ttk.Label(window, text="V for Q" + str(i + 1) + ":", font=("Times New Roman", 15)).place(x=value, y=205)
    d = tk.StringVar()
    v.append(ttk.Combobox(window, width=32, textvariable=d))
    v[i]["values"] = 'Model-Harmonic Oscillator', 'Model-Morse Oscillator'
    value += 310

# Button
exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                 command=window.destroy).place(x=365, y=260)


def apioutput():
    print(molecule.get())
    print(q_equation1.get())
    print(q_equation2.get())
    print(q_equation3.get())
    print(N1.get())
    print(L1.get())
    print(N2.get())
    print(L2.get())
    print(N3.get())
    print(L3.get())
    print(t.get())
    print(g.get())
    for i in range(3):
        print(v[i].get())
    print(filename)


# This definition works! This clears everything in the window!!!
def clear_data():
    cores.set('')
    molecule.set('')
    q_equation1.set('')
    q_equation2.set('')
    q_equation3.set('')
    t.set('')
    g.set('')
    for i in range(3):
        v[i].set('')
    N1.delete(0, END)
    L1.delete(0, END)
    N2.delete(0, END)
    L2.delete(0, END)
    N3.delete(0, END)
    L3.delete(0, END)


def save_file_prompt():
    box: bool = tk.messagebox.askyesno("PyFGH", "Would you like to save the data to a text file?")
    if box:
        print('This yes button works')
        # filename_api = filename
        # apioutput()
        window.destroy()
    else:
        print('The no button works')
        # filename_api = filename
        # apioutput()
        window.destroy()


# This is not working properly. q1var list is not working.



def output():
    try:
        """
        Added validation rules to my interface. All N values must be positive, odd integers.
        All L values must be positive floating point-values. 
        Q1 and Q2 can not be the same.
        Fix N so that the user can not enter floating point values.
        """
        InputData.output.items.molecule = molecule.get()
        InputData.output.items.q_equation1 = q_equation1.get()
        InputData.output.items.q_equation2 = q_equation2.get()
        InputData.output.items.q_equation3 = q_equation3.get()
        InputData.output.items.N1 = N1.get()
        InputData.output.items.L1 = float(L1.get())
        InputData.output.items.N2 = N2.get()
        InputData.output.items.L2 = float(L2.get())
        InputData.output.items.N3 = N3.get()
        InputData.output.items.L3 = float(L3.get())
        InputData.output.items.t = t.get()
        InputData.output.items.g = g.get()
        for i in range(3):
            InputData.output.items.v.append(v[i].get())
        # API_Class.outputAPI.items.file_name = filename
        # This is where error checking takes place.
        for i in range(3):
            if InputData.output.items.v[0] == 'Model-Harmonic Oscillator' and InputData.output.items.v[1] == 'Model-Harmonic Oscillator' and InputData.output.items.v[2] == 'Model-Harmonic Oscillator':
                holder = [model_objects.Harmonic_Oscillator(), model_objects.Harmonic_Oscillator(), model_objects.Harmonic_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Harmonic Oscillator' and InputData.output.items.v[1] == 'Model-Harmonic Oscillator' and InputData.output.items.v[2] == 'Model-Morse Oscillator':
                holder = [model_objects.Harmonic_Oscillator(), model_objects.Harmonic_Oscillator(),
                          model_objects.Morse_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Harmonic Oscillator' and InputData.output.items.v[1] == 'Model-Morse Oscillator' and InputData.output.items.v[2] == 'Model-Harmonic Oscillator':
                holder = [model_objects.Harmonic_Oscillator(), model_objects.Morse_Oscillator(),
                          model_objects.Harmonic_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Harmonic Oscillator' and InputData.output.items.v[1] == 'Model-Morse Oscillator' and InputData.output.items.v[2] == 'Model-Morse Oscillator':
                holder = [model_objects.Harmonic_Oscillator(), model_objects.Morse_Oscillator(),
                          model_objects.Morse_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Morse Oscillator' and InputData.output.items.v[1] == 'Model-Harmonic Oscillator' and InputData.output.items.v[2] == 'Model-Harmonic Oscillator':
                holder = [model_objects.Morse_Oscillator(), model_objects.Harmonic_Oscillator(),
                          model_objects.Harmonic_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Morse Oscillator' and InputData.output.items.v[1] == 'Model-Harmonic Oscillator' and InputData.output.items.v[2] == 'Model-Morse Oscillator':
                holder = [model_objects.Morse_Oscillator(), model_objects.Harmonic_Oscillator(),
                          model_objects.Morse_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Morse Oscillator' and InputData.output.items.v[1] == 'Model-Morse Oscillator' and InputData.output.items.v[2] == 'Model-Harmonic Oscillator':
                holder = [model_objects.Morse_Oscillator(), model_objects.Morse_Oscillator(),
                          model_objects.Harmonic_Oscillator()]
                model_objects.model_prompt(holder)
            elif InputData.output.items.v[0] == 'Model-Morse Oscillator' and InputData.output.items.v[1] == 'Model-Morse Oscillator' and InputData.output.items.v[2] == 'Model-Morse Oscillator':
                holder = [model_objects.Morse_Oscillator(), model_objects.Morse_Oscillator(),
                          model_objects.Morse_Oscillator()]
                model_objects.model_prompt(holder)


        if q_equation1.get() == 'OH\u2081 Bond Stretch' and q_equation2.get() == 'OH\u2081 Bond Stretch':
            messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")
            clear_data()

        elif q_equation1.get() == 'OH\u2082 Bond Stretch' and q_equation2.get() == 'OH\u2082 Bond Stretch':
            messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")
            clear_data()
        # this makes sure that the values are positive
        elif (int(InputData.output.items.N1)) % 2 == 0:
            messagebox.showerror("PyFGH", "N must be odd!!!")
            clear_data()
        elif (int(InputData.output.items.N2)) % 2 == 0:
            messagebox.showerror("PyFGH", "N must be odd!!!")
            clear_data()
        elif (int(InputData.output.items.N3)) % 2 == 0:
            messagebox.showerror("PyFGH", "N must be odd!!!")
            clear_data()

        elif int(InputData.output.items.N1) < 0:
            messagebox.showerror("PyFGH", "N must be positive!!!")
            clear_data()
        elif int(InputData.output.items.L1) < 0:
            messagebox.showerror("PyFGH", "L must be positive!!!")
            clear_data()
        elif int(InputData.output.items.N2) < 0:
            messagebox.showerror("PyFGH", "N must be positive!!!")
            clear_data()
        elif int(InputData.output.items.L2) < 0:
            messagebox.showerror("PyFGH", "L must be positive!!!")
            clear_data()
        elif int(InputData.output.items.N3) < 0:
            messagebox.showerror("PyFGH", "N must be positive!!!")
            clear_data()
        elif int(InputData.output.items.L3) < 0:
            messagebox.showerror("PyFGH", "L must be positive!!!")
            clear_data()

        else:
            save_file_prompt()
    except ValueError:
        messagebox.showerror("PyFGH", "Data is missing! FILL in ALL of the boxes before hitting calculate!!!")


calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                      command=output).place(x=420, y=250)

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


def open_file2():
    def is_list_empty(list):
        # checking the length
        if len(list) == 0:
            # returning true as length is 0
            return True
        # returning false as length is greater than 0
        return False

    if not is_list_empty(v):
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")

    else:
        global filename2
        tkinter.Tk().withdraw()
        filename2 = askopenfilename()
        print(filename2)
        window.destroy()


readbutton = tk.Button(window, text='Read Structures and Energies from File', bd='10', bg='gray', fg='white',
                       command=open_file2).place(x=360, y=320)
# Disabled the compute button for now
# compute = tk.Button(window, text='Compute on the fly', bd='10', bg='gray', fg='white',
#                    command=open_file).place(x=410, y=370)

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
vales2 = 80

for i in range(3):
    v[i].place(x=vales2, y=207, width=175)
    v[i].current()
    vales2 += 310

N1.place(x=40, y=100, width=100)
L1.place(x=185, y=100, width=100)
N2.place(x=340, y=100, width=100)
L2.place(x=495, y=100, width=100)
N3.place(x=645, y=100, width=100)
L3.place(x=800, y=100, width=100)
window.mainloop()
