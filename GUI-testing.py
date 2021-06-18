import multiprocessing
import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, NW, END, DISABLED
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style

import self
from public import public

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
# TODO: Error somewhere in this. When you select to open a file, then run the code in API.py the variables do not transfer. Fix this!!!
def open_file():
    global filename
    tkinter.Tk().withdraw()
    filename = askopenfilename()
    print(filename)


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


def output():
    class outputAPI:
        molecule_api = molecule.get()
        q_equation1_api = q_equation1.get()
        q_equation2_api = q_equation2.get()
        q_equation3_api = q_equation3.get()
        text1_api = text1.get()
        text2_api = text2.get()
        text3_api = text3.get()
        text4_api = text4.get()
        text5_api = text5.get()
        text6_api = text6.get()
        t_api = t.get()
        g_api = g.get()
        v1_api = v1.get()
        v2_api = v2.get()
        v3_api = v3.get()

        def __init__(self, molecule_api):
            self.v3_api = v3_api
            self.v2_api = v2_api
            self.v1_api = v1_api
            self.g_api = g_api
            self.t_api = t_api
            self.text6_api = text6_api
            self.text5_api = text5_api
            self.text4_api = text4_api
            self.text3_api = text3_api
            self.text2_api = text2_api
            self.text1_api = text1_api
            self.q_equation3_api = q_equation3_api
            self.q_equation2_api = q_equation2_api
            self.q_equation1_api = q_equation1_api
            self._molecule_api = molecule_api

    # print(test.molecule1)

    # window.destroy()

    """
    global molecule_api
    global q_equation1_api
    global q_equation2_api
    global q_equation3_api
    global text1_api
    global text2_api
    global text3_api
    global text4_api
    global text5_api
    global text6_api
    global t_api
    global g_api
    global v1_api
    global v2_api
    global v3_api
    # global filename_api
        for x in text1:
            if x % 2 != 0:
                messagebox.showerror("PyFGH", "ERROR, Must be even!!!")
        """
    # This is where error checking takes place.
    if q_equation1.get() == 'OH\u2081 Bond Stretch' and q_equation2.get() == 'OH\u2081 Bond Stretch':
        messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")

    elif q_equation1.get() == 'OH\u2082 Bond Stretch' and q_equation2.get() == 'OH\u2082 Bond Stretch':
        messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")

    else:
        def test():
            molecule_api = molecule.get()
            return molecule_api

        box: bool = tk.messagebox.askyesno("PyFGH", "Would you like to save the data to a text file?")
        if box:
            print('This yes button works')
            #print(test())
            print(outputAPI.molecule_api, "works")
            # filename_api = filename
            # apioutput()
            window.destroy()
        else:
            print('The no button works')
            print(outputAPI.molecule_api, "works")
            # print(outputAPI.molecule_api)
            # filename_api = filename
            # apioutput()
            window.destroy()




calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                      command=output).place(x=420, y=250)


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


def open_file2():
    if v1.get() == 'Model-Harmonic Oscillator':
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")
    elif v1.get() == 'Model-Morse Oscillator':
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")
    elif v2.get() == 'Model-Harmonic Oscillator':
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")
    elif v2.get() == 'Model-Morse Oscillator':
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")
    elif v3.get() == 'Model-Harmonic Oscillator':
        messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")
    elif v3.get() == 'Model-Morse Oscillator':
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
