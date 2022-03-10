import multiprocessing
import os
import sys

import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.messagebox import showinfo
from tkinter.ttk import Style
from util import DataObject
from util import model_objects
import numpy as np
from tkinter import filedialog as fd

import csv

#import self

from util import pyfghutil, DataObject
import math

"""
The code in this file is for a gui (graphic user interface) application. This code is written with the tkinter library framework.
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""

"""
This is the main method. 
"""


def main_window():
    def close_window():
        global running
        running = False
        print("Window closed \nPython Terminated")
        window.destroy()
        os._exit(0)
    # Creating tkinter window
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", close_window)
    running = True
    style = Style()
    window.title('PyFGH')
    window.geometry('910x425')

    # Water molecule icon in the top left conner
    window.iconbitmap(default='icon.ico')

    # label text for title
    ttk.Label(window, text="A Python implementation of the Fourier Grid Hamiltonian method.",
              background='green', foreground="white",
              font=("Times New Roman", 15)).place(x=200, y=0)

    # This is where it finds how many cpu processors the computer has. It then displays this information in the GUI.
    cores = []
    for i in range(1, multiprocessing.cpu_count() + 1):
        cores.append(i)

        # label
    ttk.Label(window, text="Computer Cores:",
              font=("Times New Roman", 10)).place(x=10, y=50)

    # Combobox creation
    n = tk.StringVar()
    cores = ttk.Combobox(window, values=cores, width=10, textvariable=n)

    # definition for calculating core counts.
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
    def open_file():
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=filename
        )

        # kinter.Tk().withdraw()
        # DataObject.holdData.file_name = askopenfilename()

    # Open Button
    open = tk.Button(window, text='Open', bd='5', bg='black', fg='white',
                     command=open_file).place(x=795, y=150)

    # Label
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
    # This appends the models to the choice boxes for V
    for i in range(3):
        ttk.Label(window, text="V for Q" + str(i + 1) + ":", font=("Times New Roman", 15)).place(x=value, y=205)
        d = tk.StringVar()
        v.append(ttk.Combobox(window, width=32, textvariable=d))
        v[i]["values"] = model_objects.Oscillator_List
        value += 310

    # Button
    exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                     command=window.destroy).place(x=365, y=260)

    # Label for SSH
    SSH = ttk.Label(window, text="Run remotely:", font=("Times New Roman", 15))
    SSH.pack()
    SSH.place(x=5, y=270)

    b = tk.StringVar()
    SSH_box = ttk.Combobox(window, width=10, textvariable=b)

    # creates values inside of the choice box
    SSH_box["values"] = ('Yes', 'No')
    SSH_box.place(x=125, y=273)

    # This is just a method for testing the values
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

    # This method clears all of the data in the GUI
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

    # This method saves the output of the GUI to a text file
    def save_file_prompt():
        box: bool = tk.messagebox.askyesno("PyFGH", "Would you like to save the data to a CSV file?")
        if box:
            window5 = tk.Tk()
            style = Style()
            window5.title('File')
            window5.geometry('300x150')
            text = "Name for New File"

            Remote2 = ttk.Label(window5, text=text, font=("Times New Roman", 15), background='green',
                                foreground="white")
            Remote2.pack()
            Remote2.place(x=75, y=0)

            Host2 = ttk.Label(window5, text="Enter Name:", font=("Times New Roman", 15))
            Host2.pack()
            Host2.place(x=10, y=30)

            Host_entry3 = ttk.Entry(window5, font=("Times New Roman", 12))
            zebras = tk.StringVar()
            values = ttk.Combobox(window5, textvariable=zebras)
            Host_entry3.place(x=115, y=32)

            def enter6():
                DataObject.holdData.name_of_file = Host_entry3.get()
                window5.destroy()

            calculate = tk.Button(window5, text='Enter', bd='15', bg='green', fg='white',
                                  command=enter6).place(x=110, y=70)

            window.destroy()
            window5.mainloop()

        else:
            a = "holder"
            DataObject.holdData.name_of_file = a
            window.destroy()

    global model_prompt

    def model_prompt(potential_model):

        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH Parameters')
        box_length = 103
        for q in range(3):
            box_length = box_length + 33 * potential_model[q].nparam
        box_len_str = '300x' + str(box_length)
        window1.geometry(box_len_str)

        qvar = np.empty(3, dtype=list)
        for i in range(3):
            qvar[i] = []
        j = 0
        y = 5

        for q in range(3):
            qvar[q] = [0] * potential_model[q].nparam

            for qparam in range(potential_model[q].nparam):
                ttk.Label(window1, text=potential_model[q].label[qparam] + " for Q" + str(q + 1) + ":",
                          font=("Times New Roman", 15)).place(x=50, y=y)
                qvar[q][qparam] = ttk.Entry(window1, font=("Times New Roman", 10))
                qvar[q][qparam].place(x=140, y=y)
                j += 1
                y += 35

        def enter_button():
            for q in range(3):
                param_list = []
                for qparam in range(potential_model[q].nparam):
                    param_list.append(qvar[q][qparam].get())
                potential_model[q].set_param(param_list)

            for q in range(3):
                for qparam in range(potential_model[q].nparam):
                    print(potential_model[q].param[qparam])

            DataObject.holdData.model_data = potential_model
            # print(type(potential_model))
            # print(DataObject.holdData.model_data)
            window1.destroy()
            if SSH_box.get() == 'Yes':
                SSH_prompt()
            else:
                save_file_prompt()

        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=enter_button).place(x=110, y=y)

        window1.mainloop()

    # This is just for testing purposes.
    """
    def output2():
        sections = []
        for i in range(3):
            if DataObject.holdData.v[i] == "Model-Harmonic Oscillator":
                sections.append(Harmonic_Oscillator())
            elif DataObject.holdData.v[i] == "Model-Morse Oscillator":
                sections.append(Harmonic_Oscillator())
            elif DataObject.holdData.v[i] == "Model-Test Oscillator":
                sections.append(Harmonic_Oscillator())
    """

    """
    This method is for building the SSH window is the user selects yes for running remotely. This takes the data that
    is entered and saves it to the DataObject folder. This runs the GUI locally and then saves the input data to a new
    text folder called DataList.txt in the resources folder. Then it takes the DataList.txt and sends this file to the 
    remote server. It then calculates the values and saves it to a new file called Results.txt. This file gets saved in 
    resources folder.
    """


    def SSH_prompt():
        window3 = tk.Tk()
        style = Style()
        window3.title('Remote Access')
        window3.geometry('300x300')
        window.iconbitmap(default='key.ico')
        text = "Remote Access Login"

        Remote = ttk.Label(window3, text=text, font=("Times New Roman", 15), background='green',
                           foreground="white")
        Remote.pack()
        Remote.place(x=65, y=0)

        Host = ttk.Label(window3, text="Host:", font=("Times New Roman", 18))
        Host.pack()
        Host.place(x=30, y=30)

        Host_entry = ttk.Entry(window3, font=("Times New Roman", 12))
        zebra = tk.StringVar()
        Host_box = ttk.Combobox(window3, textvariable=zebra)
        Host_entry.place(x=115, y=32)

        User = ttk.Label(window3, text="Username:", font=("Times New Roman", 18))
        User.pack()
        User.place(x=10, y=65)

        Username_entry = ttk.Entry(window3, font=("Times New Roman", 12))
        lion = tk.StringVar()
        Echo = ttk.Combobox(window3, textvariable=lion)
        Username_entry.place(x=115, y=68)

        Password = ttk.Label(window3, text="Password:", font=("Times New Roman", 18))
        Password.pack()
        Password.place(x=10, y=100)

        Password_entry = ttk.Entry(window3, font=("Times New Roman", 12))
        Password_entry.config(show="*")
        tiger = tk.StringVar()
        Hunter = ttk.Combobox(window3, textvariable=tiger)
        Password_entry.place(x=115, y=103)

        # For running slum on a server
        def Srun():
            window1 = tk.Tk()
            style = Style()
            window1.title('Srun Configuration')
            window1.geometry('300x300')
            window.iconbitmap(default='key.ico')
            text = "Srun Configuration"
            Remote = ttk.Label(window1, text=text, font=("Times New Roman", 15), background='green',
                               foreground="white")
            Remote.pack()
            Remote.place(x=75, y=0)

            Partition = ttk.Label(window1, text="Partition:", font=("Times New Roman", 18))
            Partition.pack()
            Partition.place(x=20, y=30)

            Partition_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            zebra2 = tk.StringVar()
            Partition_box = ttk.Combobox(window1, textvariable=zebra2)
            Partition_entry.place(x=115, y=32)

            QOS = ttk.Label(window1, text="QOS:", font=("Times New Roman", 18))
            QOS.pack()
            QOS.place(x=50, y=65)

            QOS_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            lion2 = tk.StringVar()
            Echo2 = ttk.Combobox(window1, textvariable=lion2)
            QOS_entry.place(x=115, y=68)

            Cores = ttk.Label(window1, text="Cores:", font=("Times New Roman", 18))
            Cores.pack()
            Cores.place(x=45, y=100)

            Cores_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            tiger2 = tk.StringVar()
            Hunter2 = ttk.Combobox(window1, textvariable=tiger2)
            Cores_entry.place(x=115, y=103)

            Memory = ttk.Label(window1, text="Memory:", font=("Times New Roman", 18))
            Memory.pack()
            Memory.place(x=20, y=130)

            Memory_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            tiger3 = tk.StringVar()
            Hunter3 = ttk.Combobox(window1, textvariable=tiger3)
            Memory_entry.place(x=115, y=135)

            Memory = ttk.Label(window1, text="Time:", font=("Times New Roman", 18))
            Memory.pack()
            Memory.place(x=50, y=165)

            Memory_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            tiger3 = tk.StringVar()
            Hunter3 = ttk.Combobox(window1, textvariable=tiger3)
            Memory_entry.place(x=115, y=170)

            PTY = ttk.Label(window1, text="PTY:", font=("Times New Roman", 18))
            PTY.pack()
            PTY.place(x=55, y=200)

            PTY_entry = ttk.Entry(window1, font=("Times New Roman", 12))
            leopard = tk.StringVar()
            Omega = ttk.Combobox(window1, textvariable=leopard)
            PTY_entry.place(x=115, y=203)

            Enter2 = tk.Button(window1, text='Enter', bd='15', bg='green', fg='white',
                               command=window1.destroy).place(x=120, y=235)
            window3.destroy()
            window1.mainloop()

        var1 = tk.IntVar()
        c1 = tk.Checkbutton(window3, text='Configure with srun', font=("Times New Roman", 15), variable=var1, onvalue=1,
                            offvalue=0, command=Srun)
        c1.pack()
        c1.place(x=60, y=130)

        def Enter():
            DataObject.holdData.host = Host_entry.get()
            DataObject.holdData.user = Username_entry.get()
            DataObject.holdData.password = Password_entry.get()
            window3.destroy()
            print(DataObject.holdData.host, DataObject.holdData.user, DataObject.holdData.password)
            save_file_prompt()

        Enter = tk.Button(window3, text='Enter', bd='15', bg='green', fg='white',
                          command=Enter).place(x=110, y=170)

        window3.mainloop()

    """
    This method gets called when the GUI is terminated. This saves the values from the input to the DataObject file.
    This also checks for validation rules also for the values that were inputted.
    """

    def output():
        try:
            """
            Added validation rules to my interface. All N values must be positive, odd integers.
            All L values must be positive floating point-values. 
            Q1 and Q2 can not be the same.
            Fix N so that the user can not enter floating point values.
            """
            DataObject.holdData.molecule = molecule.get()
            DataObject.holdData.q_equation1 = q_equation1.get()
            DataObject.holdData.q_equation2 = q_equation2.get()
            DataObject.holdData.q_equation3 = q_equation3.get()
            DataObject.holdData.N1 = N1.get()
            DataObject.holdData.L1 = float(L1.get())
            DataObject.holdData.N2 = N2.get()
            DataObject.holdData.L2 = float(L2.get())
            DataObject.holdData.N3 = N3.get()
            DataObject.holdData.L3 = float(L3.get())
            DataObject.holdData.t = t.get()
            DataObject.holdData.g = g.get()
            DataObject.holdData.remote = SSH_box.get()

            for i in range(3):
                DataObject.holdData.v.append(v[i].get())

            # API_Class.outputAPI.items.file_name = filename
            # This is where error checking takes place.

            # These are validation rules for the input.
            if q_equation1.get() == 'OH\u2081 Bond Stretch' and q_equation2.get() == 'OH\u2081 Bond Stretch':
                messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")
                clear_data()

            elif q_equation1.get() == 'OH\u2082 Bond Stretch' and q_equation2.get() == 'OH\u2082 Bond Stretch':
                messagebox.showerror("PyFGH", "ERROR, Q\u2081 Bond and Q\u2082 Bond can not be the same!!!")
                clear_data()
            # this makes sure that the values are positive
            elif (int(DataObject.holdData.N1)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()
            elif (int(DataObject.holdData.N2)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()
            elif (int(DataObject.holdData.N3)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()

            elif int(DataObject.holdData.N1) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(DataObject.holdData.L1) < 0:
                messagebox.showerror("PyFGH", "L must be positive!!!")
                clear_data()
            elif int(DataObject.holdData.N2) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(DataObject.holdData.L2) < 0:
                messagebox.showerror("PyFGH", "L must be positive!!!")
                clear_data()
            elif int(DataObject.holdData.N3) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(DataObject.holdData.L3) < 0:
                messagebox.showerror("PyFGH", "L must be positive!!!")
                clear_data()
            # This runs the model window when the user hits calculate.
            else:
                """
                This will loop through the model_objects file. When you select a model in the GUI this will find the 
                models that you selected. It takes the selected models and it loops in the model_objects file to find the
                given class that you selected. When it finds the matching class it will pull all of the information from 
                that class and it will append it to the holder_model list. This list will be sent to the model_prompt 
                function that will build the GUI parameter box depending on the dimensions and parameters of each 
                unique model.
                """
                import inspect
                holder_model = []

                for key, className in inspect.getmembers(model_objects):
                    for i in range(3):
                        if DataObject.holdData.v[i] == key:
                            holder_model.append(className())

                print(holder_model)
                model_prompt(holder_model)

        except ValueError:
            messagebox.showerror("PyFGH", "Data is missing! FILL in ALL of the boxes before hitting calculate!!!")
        except IndexError:  # TODO this is not working properly. After the error restart the interface!
            messagebox.showerror("PyFGH", "Please select the appropriate models!!!")
            main_window()

    # This is the calculate button.
    calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                          command=output).place(x=420, y=250)

    # This is the clear button.
    clear = tk.Button(window, text='Clear', bd='10', bg='blue', fg='white',
                      command=clear_data).place(x=525, y=260)

    # This method displays the about window in the GUI interface.
    def about_window():
        window = tk.Toplevel()
        window.title("About")
        window.geometry("500x235")
        canvas = tkinter.Canvas(window, width=500, height=235)
        canvas.pack()

        text = "  A Python implementation of the Fourier Grid Hamiltonian \n \n Credits: Dr. Jeffrey Woodford, " \
               "Nelson Maxey, Tyler Law \n and Josiah Randleman. \n \n GitHub Repository: \n https://github.com/jeffwoodford27/PyFGH/tree/main "

        x = ttk.Label(window, text=text, font=("Times New Roman", 15))
        x.pack()
        x.place(x=0, y=0)

    # This is the about button.
    about = tk.Button(window, text='About', bd='10', bg='purple', fg='white',
                      command=about_window).place(x=590, y=260)

    # This method here displays the T equations.
    def t0():
        window = tk.Toplevel()
        window.title("T Equations")
        window.geometry("500x650")
        canvas = tkinter.Canvas(window, width=500, height=650)
        canvas.pack()

        x = ttk.Label(window, text="None: ", font=("Times New Roman", 15), background='green',
                      foreground="white")
        x.pack()
        x.place(x=215, y=0)

        img = tkinter.PhotoImage(file="t0.png")
        canvas.create_image(30, 30, anchor=NW, image=img)

        x2 = ttk.Label(window, text="Approximation 1: ", font=("Times New Roman", 15), background='green',
                       foreground="white")
        x2.pack()
        x2.place(x=175, y=135)

        img1 = tkinter.PhotoImage(file="t1.png")
        canvas.create_image(100, 165, anchor=NW, image=img1)

        x3 = ttk.Label(window, text="Approximation 2: ", font=("Times New Roman", 15), background='green',
                       foreground="white")
        x3.pack()
        x3.place(x=175, y=255)

        img2 = tkinter.PhotoImage(file="t2.png")
        canvas.create_image(250, 330, image=img2)

        x4 = ttk.Label(window, text="Approximation 3: ", font=("Times New Roman", 15), background='green',
                       foreground="white")
        x4.pack()
        x4.place(x=175, y=380)

        img3 = tkinter.PhotoImage(file="t3.png")
        canvas.create_image(250, 460, image=img3)

        x5 = ttk.Label(window, text="Approximation 4: ", font=("Times New Roman", 15), background='green',
                       foreground="white")
        x5.pack()
        x5.place(x=175, y=512)

        img4 = tkinter.PhotoImage(file="t4.png")
        canvas.create_image(250, 585, image=img4)

        window.mainloop()

    tbutton = tk.Button(window, text='Display T equation', bd='10', bg='orange', fg='white',
                        command=t0).place(x=232, y=260)
    """
    This is a validation checker for the Read Structures button. You can not read in values and also try to run the 
    GUI interface at the same time.
    """

    def Read_Structures_Button():
        def is_list_empty(list):
            # checking the length
            if len(list) == 0:
                # returning true as length is 0
                return True
            # returning false as length is greater than 0
            return False

        if is_list_empty(v):
            messagebox.showerror("PyFGH", "ERROR, Can not read data from file and have data from interface!!!")

        else:
            global molecules
            tkinter.Tk().withdraw()
            molecules = askopenfile()
            """
            if molecules is not None:
                content = molecules.read()
                print(content)
                """
            print(molecules)
            potential_energies_file = askopenfilename()
            print(potential_energies_file)

            Q1 = []
            Q2 = []
            Q3 = []
            Z = []
            s = []
            A = []
            m = []
            list2 = []
            list3 = []
            x_coordinates = []
            y_coordinates = []
            z_coordinates = []
            mass = []
            potx1 = []
            potx2 = []
            potx3 = []
            poty1 = []
            poty2 = []
            poty3 = []

            # TODO ask the user for two files. File 1 is the equilibrium file or the molecules.csv file
            # TODO File 2 is the potential energies file which is the waterpot-data.csv
            # TODO read in q and energies and verify in the water.csv that # of lines equals n1*n2*n3.
            # TODO q must be equally spaced also q3 then q2 then q1. Calcalte the Detla Q. L1=n1*delta Q1;  L2=n2*delta Q2
            # do distance test with potential energy file which is x1 and so forth
            # waterpot.csv: Q1, Q2, Q3, x1, y1, x2, y2, x3, y3, energies
            # TODO add to interface!!!!!!

            totalN = 0
            # totalN = DataObject.holdData.N1 * DataObject.holdData.N2 * DataObject.holdData.N3

            N1_1 = 11
            N2_1 = 11
            N3_1 = 11

            def getNs():
                file = open(potential_energies_file)
                reader = csv.reader(file)
                lines = len(list(reader))
                totalN = N1_1 * N2_1 * N3_1
                if lines == totalN:
                    print("The lines of waterpot-data equals the toal of all N vales")
                else:
                    print("The lines of waterpot-data do not equal the toal of all N vales ", lines)
                return totalN

            """
            def validateQ ():
                #TODO calculate delta q
                with open("waterpot-data.csv", ) as f:
                    for x in f:
                        Q1.append(x.split(',')[0])
                        Q2.append(x.split(',')[1])
                        Q3.append(x.split(',')[2])

                    i = 0
                    while i < len(Q3):
                        if Q3[i] == Q3[0] and (Q2[i] - 1.00):
                            print('true')
                            break

            """
            with open(molecules.read()) as a:
                for row in a:
                    list2.append(row.split(',')[0])  # Li
                    new_row = ['-'.join([row.split(',')[0], row.split(',')[1]])]
                    x = ' '.join(new_row)
                    list3.append(x)
                    x_coordinates.append(row.split(',')[2])
                    y_coordinates.append(row.split(',')[3])
                    z_coordinates.append((row.split(',')[4]).strip())
                    mass.append(row.split(',')[1])
                    masslist = ([float(x) for x in mass])
                    # print(list2)  # ['Li']
                    print(list3)  # ['Li-6']
                    print("\n")
                for x in list2:
                    print(x)

                for x in list2:  # x is the atomic symbol
                    if x in pyfghutil.AtomicSymbolLookup.values():
                        print(x + " is a valid element")
                        s.append(x)
                    else:
                        print(x + " is not a valid element")

                print("\n")
                for x in list2:  # x is the atomic symbol
                    for key, value in pyfghutil.AtomicSymbolLookup.items():
                        if x == value:
                            Z.append(key)
                            print("Atomic number of " + x + ":", key)

                print("\n")
                for x in list3:  # x is the atomic symbol
                    for key, value in pyfghutil.MassLookup.items():
                        if value in masslist:
                            print("valid atomic mass")

                        if x == key:
                            A.append(value)
                            print("Atomic mass of " + x + ":", value)

                print("\n")
                for x in list3:
                    for key, value in pyfghutil.MassLookup.items():
                        if x == key:
                            print(x + " is a valid element")
                            if value in masslist:
                                print("valid atomic mass")
                for x in A:
                    atomic = x * 1822.89
                    m.append(atomic)
                    print("amu to atomic ", m)

            """
            This does validation checking. Calculates the distance and the cos theta
            """

            def calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3):
                d = math.sqrt(math.pow(x2 - x1, 2) +
                              math.pow(y2 - y1, 2) +
                              math.pow(z2 - z1, 2))

                d2 = math.sqrt(math.pow(xx3 - x1, 2) +
                               math.pow(yy3 - y1, 2) +
                               math.pow(zz3 - z1, 2))

                d3 = math.sqrt(math.pow(xx3 - xx2, 2) +
                               math.pow(yy3 - yy2, 2) +
                               math.pow(zz3 - zz2, 2))
                # cos theta equation
                costheta = (((x2 - x1) * (xx3 - x1) + (y2 - y1) * (yy3 - y1) + (z2 - z1) * (zz3 - z1)) / (d * d2))
                print("Cos Theta is: ", costheta)

                if -1 < costheta < 1:
                    print('molecule is non-linear')
                    print("Cos Theta is: ", costheta)
                else:
                    print("Molecule is linear")

                if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
                    print("Distance is", d + d2 + d3, " Atom is unique")
                else:
                    print("Atom is not unique")

                    # First atom is assumed to be the central atom

            xlist = [float(x) for x in x_coordinates]
            ylist = [float(x) for x in y_coordinates]
            zlist = [float(x) for x in z_coordinates]

            # Driver Code
            x1 = xlist[0]
            y1 = ylist[0]
            z1 = zlist[0]
            x2 = xlist[1]
            y2 = ylist[1]
            z2 = zlist[1]

            xx2 = xlist[1]
            yy2 = ylist[1]
            zz2 = zlist[1]
            xx3 = xlist[2]
            yy3 = ylist[2]
            zz3 = zlist[2]

            """
            Splices the data in the waterpot-data.csv file
            """
            with open(potential_energies_file.read(),  encoding="utf-8") as a:
                for x in a:
                    potx1.append(x.split(',')[3])
                    potx2.append(x.split(',')[5])
                    potx3.append(x.split(',')[7])

                    poty1.append(x.split(',')[4])
                    poty2.append(x.split(',')[6])
                    poty3.append(x.split(',')[8])

            potxlist1 = [float(x) for x in potx1]
            potxlist2 = [float(x) for x in potx2]
            potxlist3 = [float(x) for x in potx3]

            potylist1 = [float(x) for x in poty1]
            potylist2 = [float(x) for x in poty2]
            potylist3 = [float(x) for x in poty3]

            """
            This does validation checking. Calculates the distance and the cos theta
            """

            def calculations2(x1, y1, x2, y2, x3, y3):
                d = math.sqrt(math.pow(x2 - x1, 2) +
                              math.pow(y2 - y1, 2))

                d2 = math.sqrt(math.pow(x3 - x1, 2) +
                               math.pow(y3 - y1, 2))

                d3 = math.sqrt(math.pow(x3 - x2, 2) +
                               math.pow(y3 - y2, 2))

                # cos theta equation
                costheta = (((x2 - x1) * (x3 - x1) + (y2 - y1) * (y3 - y1)) / (d * d2))
                print("Cos Theta is: ", costheta)

                if -1 < costheta < 1:
                    print('molecule is non-linear')
                    print("Cos Theta is: ", costheta)
                else:
                    print("Molecule is linear")
                    raise Exception("Molecule is linear")

                if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
                    print("Distance is", d + d2 + d3, " Atom is unique")
                else:
                    print("Atom is not unique")
                    raise Exception("Atom is not unique")

                    # First atom is assumed to be the central atom

            """
            This does validation checking for the waterpot-data.csv file
            """
            for x in range(
                    len(potxlist1) and len(potxlist2) and len(potxlist3) and len(potylist1) and len(potylist2) and len(
                        potylist3)):
                calculations2(potxlist1[x], potylist1[x], potxlist2[x], potylist2[x], potxlist3[x], potylist3[x])

            print("\n")
            print("WaterPot for x1: ", potxlist1)
            print("WaterPot for x2: ", potxlist2)
            print("WaterPot for x3: ", potxlist3)
            print("WaterPot for y1: ", potylist1)
            print("WaterPot for y2: ", potylist2)
            print("WaterPot for y3: ", potylist3)
            print("\n")
            print("X Coordinates of the elements: ", xlist)
            print("Y Coordinates of the elements: ", ylist)
            print("Z Coordinates of the elements: ", zlist)
            print("\n")
            print("Atomic Number: ", Z)  # Atomic Number
            print("Atomic Mass: ", A)  # Atomic Mass
            print("Symbol: ", s)  # Symbol
            calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3)
            test = pyfghutil.Atom(Z, A, m, xlist,
                                  ylist)  # save only one molecule to the atom class. Save a collection of the atoms to the structure class.
            print(getattr(test, 'Z'))
            getNs()
            # validateQ()

            """
            This is for validating the water potential energy file
            """

            N1_2 = 7
            L1_2 = 0.7
            N2_2 = 7
            L2_2 = 0.7
            N3_2 = 7
            L3_2 = 0.7

            deltaQ1 = L1_2 / float(N1_2)
            deltaQ2 = L2_2 / float(N2_2)
            deltaQ3 = L3_2 / float(N3_2)

            with open(potential_energies_file.read(),  encoding="utf-8") as a:
                for x in a:
                    Q1.append(float(x.split(',')[0]))
                    Q2.append(float(x.split(',')[1]))
                    Q3.append(float(x.split(',')[2]))

            n = 0
            for i in range(N1_2):
                for j in range(N2_2):
                    for k in range(N3_2):
                        q1 = deltaQ1 * float(i - int(N1_2 / 2))
                        q2 = deltaQ2 * float(j - int(N2_2 / 2))
                        q3 = deltaQ3 * float(k - int(N3_2 / 2))
                        if (round(q1, 3) == round(Q1[n], 3)) and (round(q2, 3) == round(Q2[n], 3)) and (
                                round(q3, 3) == round(Q3[n], 3)):
                            continue
                        else:
                            print('Values are not valid')
                            break
                        n += 1

            window.destroy()

    # This is a button called Read Structures
    readbutton = tk.Button(window, text='Read Structures and Energies from File', bd='10', bg='gray', fg='white',
                           command=Read_Structures_Button).place(x=360, y=320)
    # Disabled the compute button for now
    # compute = tk.Button(window, text='Compute on the fly', bd='10', bg='gray', fg='white',
    #                    command=open_file).place(x=410, y=370)

    # Adding combobox drop down list
    # cores['values'] = (multiprocessing.cpu_count())

    # This places a lot of things in the GUI
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
