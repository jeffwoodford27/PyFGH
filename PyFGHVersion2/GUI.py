import multiprocessing
import os
import gc
import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, NW
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style

import PyFGHVersion2.molecule_gui as molecule_gui
from PyFGHVersion2.util import model_objects as model_objects
import numpy as np

# import jnwtest11 as test11
# TODO take the Atom class and add it to InputData so Nelson can grab it
# TODO 3 Atom class. Have a list of the three members of the atom class. [Atom1, Atom2, Atom3]
# TODO [List of all of the molecules] made into a equalibrium class.
# TODO

# import self
opened = False
from PyFGHVersion2.util import DataObject as DataObject

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
    window.geometry('910x255')

    # Water molecule icon in the top left conner

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
              font=("Times New Roman", 10)).place(x=350, y=50)

    # Combobox creation
    n = tk.StringVar()
    cores = ttk.Combobox(window, values=cores, width=10, textvariable=n)

    # definition for calculating core counts.
    # Label

    ttk.Label(window, text="Dimensions:", font=("Times New Roman", 15)).place(x=25, y=47)
    d = tk.StringVar()
    N1text = ttk.Combobox(window, width=15, textvariable=d)

    dimensions = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    n10 = tk.StringVar()
    dimensions = ttk.Combobox(window, values=dimensions, width=10, textvariable=n10)

    ttk.Label(window, text="Number of Eigenvalues:", font=("Times New Roman", 12)).place(x=620, y=47)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=10, textvariable=d1)

    eigenvalues = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    n11 = tk.StringVar()
    eigenvalues = ttk.Combobox(window, values=eigenvalues, width=10, textvariable=n11)

    ttk.Label(window, text="Eigenvalue Calculation Method:", font=("Times New Roman", 10)).place(x=22, y=100)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=10, textvariable=d1)

    calculation = ['Sparse Matrix', 'Full Matrix']

    n12 = tk.StringVar()
    calculation = ttk.Combobox(window, values=calculation, width=10, textvariable=n12)

    ttk.Label(window, text="Potential Energy Calculation Method:", font=("Times New Roman", 8)).place(x=600, y=100)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=12, textvariable=d1)

    calculation2 = ['Read from File', 'Compute With Psi4']

    n15 = tk.StringVar()
    calculation2 = ttk.Combobox(window, values=calculation2, width=16, textvariable=n15)

    # Entry
    N10 = ttk.Entry(window, font=("Times New Roman", 10))
    c10 = tk.StringVar()
    N10box = ttk.Combobox(window, textvariable=c10)

    # Entry
    N12 = ttk.Entry(window, font=("Times New Roman", 10))
    c12 = tk.StringVar()
    N120box = ttk.Combobox(window, textvariable=c12)
    global isopenedN
    global isopenedL
    global holderN
    global holderL
    holderN = 0
    holderL = 0
    isopenedN = holderN
    isopenedL = holderL

    def clearNdimensions():
        holder.setNlist(None)

    def clearLdimensions():
        holder.setLlist(None)

    def actionN():

        global isopenedN
        if holder.getNlist() == None and holder.getLlist() == None:
            window = tk.Tk()
            x = int(dimensions.get())
            holder.setD(x)

            style = Style()
            window.title('PyFGH')
            box_len_str = '300x' + str((x * 95 + 70))
            window.geometry(box_len_str)
            # window.geometry('300x450')
            # Label

            x1 = [None] * x

            x2 = [None] * x

            fireflies = 0

            for number in range(x):
                ttk.Label(window, text="Values:", font=("Times New Roman", 15)).place(x=60, y=10)
                d = tk.StringVar()
                N1text = ttk.Combobox(window, width=15, textvariable=d)

                x1[number] = ttk.Entry(window, font=("Times New Roman", 10))
                c = tk.StringVar()
                N1box = ttk.Combobox(window, textvariable=c)

                ttk.Label(window, text=("N") + str(number + 1) + ":", font=("Times New Roman", 15)).place(x=60, y=(
                        40 + fireflies))
                d = tk.StringVar()
                N1text = ttk.Combobox(window, width=15, textvariable=d)

                x1[number].place(x=100, y=(40 + fireflies), width=100)
                fireflies += 40

            for number in range(x):
                ttk.Label(window, text="", font=("Times New Roman", 15)).place(x=60, y=10)
                d = tk.StringVar()
                N1text = ttk.Combobox(window, width=15, textvariable=d)

                x2[number] = ttk.Entry(window, font=("Times New Roman", 10))
                c = tk.StringVar()
                N1box = ttk.Combobox(window, textvariable=c)

                ttk.Label(window, text=("L") + str(number + 1) + ":", font=("Times New Roman", 15)).place(x=60, y=(
                        40 + fireflies))
                d = tk.StringVar()
                N1text = ttk.Combobox(window, width=15, textvariable=d)

                x2[number].place(x=100, y=(40 + fireflies), width=100)
                fireflies += 40

            # Make a section for N and L.
            # If it is 3 dimension there must be 3 boxes for N and 3 boxs for L so a total of 6.

            def enter_button():
                x = int(dimensions.get())
                valuesN = []
                valuesL = []
                try:
                    for y in range(x):
                        valuesN.append(int(x1[y].get()))

                    for i in range(x):
                        valuesL.append(float(x2[i].get()))
                except ValueError:
                    messagebox.showerror("PyFGH", "Must include only number values!!!")
                    holder.setNlist(None)
                    holder.setLlist(None)
                    actionN()

                window.destroy()

                holder.setNlist(valuesN)
                holder.setLlist(valuesL)

                print(holder.getNlist())
                print(holder.getLlist())
                print(holder.getD())

                for x in holder.getNlist():
                    if x % 2 == 0 or x < 5:
                        messagebox.showerror("PyFGH", "N must be odd, positive integer greater to or equal to 5!!!")
                        holder.setNlist(None)
                        holder.setLlist(None)
                        actionN()

                if holder.getLlist() != None:
                    for x in holder.getLlist():
                        if x < 0:
                            messagebox.showerror("PyFGH", "L must be positive!!!")
                            holder.setNlist(None)
                            holder.setLlist(None)
                            actionN()
                # for x in holder.getLlist():
                #     if int(x) < 0:
                #         messagebox.showerror("PyFGH", "L must be positive!!!")
                #         clearLdimensions()

            yvalue = int(dimensions.get())
            enter = tk.Button(window, text='Enter', bd='20', bg='green', fg='white',
                              command=enter_button).place(x=110, y=(yvalue * 85 + 20))

        else:
            messagebox.showerror("PyFGH", "The Vales For N Have Already Been Assigned!!!")

    lbutton = tk.Button(window, text='Get Values', bd='10', bg='gray', fg='white',
                        command=actionN).place(x=425, y=90)

    # Button
    exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                     command=close_window).place(x=365, y=150)

    # This method clears all of the data in the GUI
    def clear_data():
        cores.set('')

        # N1.delete(0, END)
        # L1.delete(0, END)
        # N2.delete(0, END)
        # L2.delete(0, END)
        # N3.delete(0, END)
        # L3.delete(0, END)

    # This method saves the output of the GUI to a text file
    def save_file_prompt():
        window.destroy()
        gc.collect()


    global model_prompt

    def test():
        try:
            eq, pes = molecule_gui.molecule_testing(holder)
            holder.setEquilMolecule(eq)
            holder.setPES(pes)
        except:
            pass

    def Read_Structures_Button():
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """
        y = askopenfilename()
        #        DataObject.test.equilibrium_file = x
        #        DataObject.test.potential_energy_file = y
        holder.setpotential_energy(y)
        # holder.setvalue_holder(False)

    def Read_Structures_Button2():
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        x = askopenfilename()
        #        DataObject.test.equilibrium_file = x
        #        DataObject.test.potential_energy_file = y
        holder.setequilibrium_file(x)
        # holder.setvalue_holder(False)

    def output():

        try:
            """
            Added validation rules to my interface. All N values must be positive, odd integers.
            All L values must be positive floating point-values. 
            Q1 and Q2 can not be the same.
            Fix N so that the user can not enter floating point values.
            """
            holder.setcores_amount(max(1, int(cores.get())))
            holder.setNumberOfEigenvalues(int(eigenvalues.get()))
            holder.setVmethod(calculation2.get())

            if calculation.get() == "Sparse Matrix":
                holder.setEigenvalueMethod(True)

            if calculation.get() == "Full Matrix":
                holder.setEigenvalueMethod(False)

            if calculation2.get() == "Read from File":
                Read_Structures_Button()
                test()
                save_file_prompt()
            # try:
            #     if calculation.get() == "Matrix":
            #         holder.setEigenvalueMethod(True)
            # except:
            #     print("error")
            #     pass
            # if calculation.get() == "test":
            #     holder.setEigenvalueMethod(True)

            # if calculation2.get() == "Harmonic Oscillator":
            #     import inspect
            # holder_model = []
            # import re
            # testing = "Harmonic_Oscillator"
            #
            # for i in range(int(dimensions.get())):
            #     for key, className in inspect.getmembers(model_objects):
            #         if testing == key:
            #             holder_model.append(className())

            # print(holder_model)
            # model_prompt(holder_model)
            # test()
            #
            # if calculation2.get() == "Morse Oscillator":
            #     import inspect
            #     holder_model = []
            #     import re
            #     testing = "Morse_Oscillator"
            #
            #     for i in range(int(dimensions.get())):
            #         for key, className in inspect.getmembers(model_objects):
            #             if testing == key:
            #                 holder_model.append(className())
            #
            #     print(holder_model)
            #     model_prompt(holder_model)
            #     test()

        except ValueError:
            messagebox.showerror("PyFGH", "Data is missing! FILL in ALL of the boxes before hitting calculate!!!")
        except IndexError:  # TODO this is not working properly. After the error restart the interface!
            messagebox.showerror("PyFGH", "Error, Please restart program!!!")
            main_window()
        except:
            print("problem")

            # This is the calculate button.
    calculate = tk.Button(window, text='Calculate', bd='20', bg='green', fg='white',
                          command=output).place(x=420, y=140)

    # This is the clear button.
    clear = tk.Button(window, text='Clear', bd='10', bg='blue', fg='white',
                      command=clear_data).place(x=525, y=150)

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

    # This is the about button
    about = tk.Button(window, text='About', bd='10', bg='purple', fg='white',
                      command=about_window).place(x=590, y=150)

    def help_window():
        window = tk.Toplevel()
        window.title("About")
        window.geometry("500x235")
        canvas = tkinter.Canvas(window, width=500, height=235)
        canvas.pack()

        text = ""

        x = ttk.Label(window, text=text, font=("Times New Roman", 15))
        x.pack()
        x.place(x=0, y=0)

        # This is the about button.

    help = tk.Button(window, text='Help', bd='10', bg='#F9BB46', fg='white',
                     command=help_window).place(x=303, y=150)

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

    # This is a button called Read Structures
    readbutton = tk.Button(window, text='Read Equilibrium Structure from File', bd='10', bg='gray', fg='white',
                           command=Read_Structures_Button2).place(x=360, y=200)
    # Disabled the compute button for now
    # compute = tk.Button(window, text='Compute on the fly', bd='10', bg='gray', fg='white',
    #                    command=open_file).place(x=410, y=370)

    # Adding combobox drop down list
    # cores['values'] = (multiprocessing.cpu_count())

    # This places a lot of things in the GUI
    cores.place(x=450, y=50)
    cores.current()
    vales2 = 80
    dimensions.place(x=180, y=50)
    eigenvalues.place(x=780, y=50)
    calculation.place(x=200, y=100)
    calculation2.place(x=780, y=100)

    window.mainloop()
    return holder
