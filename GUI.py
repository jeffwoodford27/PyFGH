import multiprocessing
import os
import sys

import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.messagebox import showinfo
from tkinter.ttk import Style

import molecule_gui
from util import DataObject
from util import model_objects
import numpy as np
from tkinter import filedialog as fd

#TODO take the Atom class and add it to InputData so Nelson can grab it
#TODO 3 Atom class. Have a list of the three members of the atom class. [Atom1, Atom2, Atom3]
#TODO [List of all of the molecules] made into a equalibrium class.
#TODO

import csv

# import self

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
    holder = DataObject.InputData()

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
    window.geometry('910x275')

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
    ttk.Label(window, text="Equilibrium Coordinates:", font=("Times New Roman", 10)).place(x=645, y=50)

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
                     command=open_file).place(x=795, y=45)

    # Button
    exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                     command=window.destroy).place(x=365, y=160)

    # Label for SSH
    SSH = ttk.Label(window, text="Run remotely:", font=("Times New Roman", 15))
    SSH.pack()
    SSH.place(x=5, y=170)

    b = tk.StringVar()
    SSH_box = ttk.Combobox(window, width=10, textvariable=b)

    # creates values inside of the choice box
    SSH_box["values"] = ('Yes', 'No')
    SSH_box.place(x=125, y=173)

    # This is just a method for testing the values
    def apioutput():

        print(N1.get())
        print(L1.get())
        print(N2.get())
        print(L2.get())
        print(N3.get())
        print(L3.get())

    # This method clears all of the data in the GUI
    def clear_data():
        cores.set('')

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
                holder.set_name_of_file(Host_entry3.get())
                window5.destroy()

            calculate = tk.Button(window5, text='Enter', bd='15', bg='green', fg='white',
                                  command=enter6).place(x=110, y=70)

            window.destroy()
            window5.mainloop()

        else:
            a = "holder"
            holder.set_name_of_file(a)
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

            holder.model_data = potential_model
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
            holder.host = Host_entry.get()
            holder.user = Username_entry.get()
            holder.password = Password_entry.get()
            window3.destroy()
            print(holder.host, holder.user, holder.password)
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

            print(DataObject.test.equilibrium_file)
            holder.setN1(N1.get())
            holder.setN2(N2.get())
            holder.setN3(N3.get())
            holder.setL1(L1.get())
            holder.setL2(L2.get())
            holder.setL3(L3.get())
            holder.set_remote(SSH_box.get())
            print(holder.N1, holder.N2, " holder")

            print(holder.value_holder)

            if holder.value_holder:
                test = molecule_gui.molecule_testing(int(holder.N1), int(holder.L1),
                                          int(holder.N2),
                                          int(holder.L2), int(holder.N3),
                                          int(holder.L3))







            if (int(holder.N1)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()
            elif (int(holder.N2)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()
            elif (int(holder.N3)) % 2 == 0:
                messagebox.showerror("PyFGH", "N must be odd!!!")
                clear_data()

            elif int(holder.N1) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(holder.L1) < 0:
                messagebox.showerror("PyFGH", "L must be positive!!!")
                clear_data()
            elif int(holder.N2) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(holder.L2) < 0:
                messagebox.showerror("PyFGH", "L must be positive!!!")
                clear_data()
            elif int(holder.N3) < 0:
                messagebox.showerror("PyFGH", "N must be positive!!!")
                clear_data()
            elif int(holder.L3) < 0:
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

                save_file_prompt()

        except ValueError:
            messagebox.showerror("PyFGH", "Data is missing! FILL in ALL of the boxes before hitting calculate!!!")
        except IndexError:  # TODO this is not working properly. After the error restart the interface!
            messagebox.showerror("PyFGH", "Please select the appropriate models!!!")
            main_window()

    # This is the calculate button.
    calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                          command=output).place(x=420, y=150)

    # This is the clear button.
    clear = tk.Button(window, text='Clear', bd='10', bg='blue', fg='white',
                      command=clear_data).place(x=525, y=160)

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
                      command=about_window).place(x=590, y=160)

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

    """
    This is a validation checker for the Read Structures button. You can not read in values and also try to run the 
    GUI interface at the same time.
    """

    def Read_Structures_Button():
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        x = askopenfilename()
        y = askopenfilename()
        DataObject.test.equilibrium_file = x
        DataObject.test.potential_energy_file = y
        holder.setvalue_holder(True)

    # This is a button called Read Structures
    readbutton = tk.Button(window, text='Read Structures and Energies from File', bd='10', bg='gray', fg='white',
                           command=Read_Structures_Button).place(x=360, y=220)
    # Disabled the compute button for now
    # compute = tk.Button(window, text='Compute on the fly', bd='10', bg='gray', fg='white',
    #                    command=open_file).place(x=410, y=370)

    # Adding combobox drop down list
    # cores['values'] = (multiprocessing.cpu_count())

    # This places a lot of things in the GUI
    cores.place(x=105, y=50)
    cores.current()
    vales2 = 80
    N1.place(x=40, y=100, width=100)
    L1.place(x=185, y=100, width=100)
    N2.place(x=340, y=100, width=100)
    L2.place(x=495, y=100, width=100)
    N3.place(x=645, y=100, width=100)
    L3.place(x=800, y=100, width=100)

    window.mainloop()
    print("after mainloop")
    return holder
