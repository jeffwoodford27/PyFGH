import multiprocessing
import tkinter as tk
from tkinter import ttk, messagebox

"""
The code in this file is for a gui (graphic user interface) application. This code is written with the tkinter library framework.
Also go back through and make better variable names instead of alphabetic letters.
Author: Josiah Randleman
"""

# Creating tkinter window
window = tk.Tk()
window.title('PyFGH')
window.geometry('1000x250')

# Water molecule icon in the top left conner
window.iconbitmap(default='icon.ico')

# label text for title
ttk.Label(window, text="A Python implementation of the Fourier Grid Hamiltonian method.",
          background='green', foreground="white",
          font=("Times New Roman", 15)).place(x=250, y=0)

# label
ttk.Label(window, text="Computer Cores:",
          font=("Times New Roman", 10)).place(x=10, y=50)

# Combobox creation
n = tk.StringVar()
cores = ttk.Combobox(window, width=10, textvariable=n)


# definition for calculating core counts. Needs to include numbers leading up to the core count. Need to implement a
# better for loop.
def cpu_count():
    for x in range(multiprocessing.cpu_count()):
        cores["values"] = (x + 1)


# Label
ttk.Label(window, text="Molecule Specification:", font=("Times New Roman", 10)).place(x=225, y=50)
m = tk.StringVar()
molecule = ttk.Combobox(window, width=10, textvariable=m)

# creates values inside of the choice box
molecule["values"] = u'H\u2082O'

# Label
ttk.Label(window, text="Q Choice Box:", font=("Times New Roman", 10)).place(x=475, y=50)
n = tk.StringVar()
q_equations = ttk.Combobox(window, width=22, textvariable=n)

# creates values inside of the choice box
q_equations["values"] = (u'q\u2081=r\u2081-r\u2081\u2070=>q\u2082=r\u2082-r\u2082\u2070', u'q=\u00BD(q\u2081+q\u2082)=>'
                                                                                          u'q=\u00BD(q\u2081-q\u2082)',
                         u'q=\u03B8-\u03B8\u2070=>q=cos(\u03B8-\u03B8\u2070)')

# Label
ttk.Label(window, text="Equilibrium Coordinates:", font=("Times New Roman", 10)).place(x=745, y=50)
a = tk.StringVar()
equilibrium = ttk.Combobox(window, width=5, textvariable=a)

# creates values inside of the choice box
equilibrium["values"] = ('N', 'L')

# Label
ttk.Label(window, text="T:", font=("Times New Roman", 20)).place(x=50, y=100)
b = tk.StringVar()
t = ttk.Combobox(window, width=15, textvariable=b)

# creates values inside of the choice box
t["values"] = ('None', 'Approximation 1', 'Approximation 2', 'Approximation 3', 'Approximation 4', 'Approximation 5')

# Label
ttk.Label(window, text="G:", font=("Times New Roman", 20)).place(x=425, y=100)
c = tk.StringVar()
g = ttk.Combobox(window, width=15, textvariable=c)

# creates values inside of the choice box
g["values"] = 'test'

# Label
ttk.Label(window, text="V:", font=("Times New Roman", 20)).place(x=675, y=100)
d = tk.StringVar()
v = ttk.Combobox(window, width=32, textvariable=d)

v[
    "values"] = 'Model-Harmonic Oscillator', 'Model-Morse Oscillator', 'Read Structures and Energies from File', 'Compute on The Fly'

# Button
exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                 command=window.destroy).place(x=385, y=180)


def output():
    messagebox.askyesno("PyFGH", "Would you like to save the data to a text file?")


calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                      command=output).place(x=450, y=170)


# This will clear the data in the choice boxes
def clear_data():
    cores.set('')
    molecule.set('')
    q_equations.set('')
    equilibrium.set('')
    t.set('')
    g.set('')
    v.set('')


clear = tk.Button(window, text='Clear', bd='10', bg='blue', fg='white',
                  command=clear_data).place(x=565, y=180)

# Adding combobox drop down list
# cores['values'] = (multiprocessing.cpu_count())
cpu_count()
cores.place(x=105, y=50)
cores.current()
molecule.place(x=355, y=50)
molecule.current()
q_equations.place(x=560, y=50)
q_equations.current()
equilibrium.place(x=895, y=50)
equilibrium.current()
t.place(x=100, y=105)
t.current()
g.place(x=455, y=105)
g.current()
v.place(x=725, y=105)
v.current()
window.mainloop()
