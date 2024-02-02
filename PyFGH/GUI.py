import multiprocessing
import os
import gc
import tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import PyFGH.molecule_gui as molecule_gui
from PyFGH.util.pyfghutil import ValidationError as ValidationError
from PyFGH.util import DataObject as DataObject

"""
The code in this file is for a gui (graphic user interface) application. This code is written with the tkinter library framework.
Author: Josiah Randleman
"""

opened = False

'''
The main window is a function that calls the GUI window. The method gets called in main.  
'''

def main_window():
    holder = DataObject.InputData()
    holder.gui = True
    # this closes the gui and terminates the program
    def close_window():
        global running
        running = False
        print("Window closed \nPython Terminated")
        window.destroy()
        os._exit(0)

    # Creating main tkinter window
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", close_window)
    running = True
    style = Style()
    window.title('PyFGH')
    window.geometry('910x255')
    from pathlib import Path
    # Water molecule icon in the top left conner
    filepath = Path(__file__).parent / "icon.ico"
    window.iconbitmap(default=filepath)

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

    # Combobox creation for cores
    n = tk.StringVar()
    cores = ttk.Combobox(window, values=cores, width=10, textvariable=n)

    # definition for calculating core counts.

    # Label to get the dimensions
    ttk.Label(window, text="Dimensions:", font=("Times New Roman", 15)).place(x=25, y=47)
    d = tk.StringVar()
    N1text = ttk.Combobox(window, width=15, textvariable=d)

    dimensions = [1, 2, 3, 4, 5, 6]

    n10 = tk.StringVar()
    dimensions = ttk.Combobox(window, values=dimensions, width=10, textvariable=n10)

    # Label to get the number of eigenvalues
    ttk.Label(window, text="Number of Eigenvalues:", font=("Times New Roman", 12)).place(x=620, y=47)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=10, textvariable=d1)

    eigenvalues = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    n11 = tk.StringVar()
    eigenvalues = ttk.Combobox(window, values=eigenvalues, width=10, textvariable=n11)

    # Label to get the eigenvalue calculation method
    ttk.Label(window, text="Eigenvalue Calculation Method:", font=("Times New Roman", 10)).place(x=22, y=100)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=10, textvariable=d1)

    calculation = ['Sparse Matrix', 'Full Matrix']

    n12 = tk.StringVar()
    calculation = ttk.Combobox(window, values=calculation, width=10, textvariable=n12)

    # Label to get the potential energy calculation method
    ttk.Label(window, text="Potential Energy Calculation Method:", font=("Times New Roman", 8)).place(x=600, y=100)
    d1 = tk.StringVar()
    N1text = ttk.Combobox(window, width=12, textvariable=d1)

    calculation2 = ['Read from File', 'Compute With Psi4']

    n15 = tk.StringVar()
    calculation2 = ttk.Combobox(window, values=calculation2, width=16, textvariable=n15)

    def clearNdimensions():
        holder.setNlist(None)

    def clearLdimensions():
        holder.setLlist(None)

    # This method exits the program and then it clears unneeded memory
    def exit():
        window.destroy()
        gc.collect()

    # This method clears all of the data in the GUI+
    def clear_data():
        cores.set('')
        dimensions.set('')
        eigenvalues.set('')
        calculation.set('')
        calculation2.set('')
        holder.clearEverything()
        gc.collect()

    # This gets the N and L values and builds the GUI based on the Dimensions
    def actionN():
        try:
            if holder.getNlist() == None and holder.getLlist() == None:
                window2 = tk.Tk()
                x = int(dimensions.get())
                holder.setD(x)

                style = Style()
                window2.title('PyFGH')
                box_len_str = '300x' + str((x * 95 + 70))
                window2.geometry(box_len_str)
                # window.geometry('300x450')
                # Label

                x1 = [None] * x

                x2 = [None] * x

                fireflies = 0

                for number in range(x):
                    ttk.Label(window2, text="Values:", font=("Times New Roman", 15)).place(x=60, y=10)
                    d = tk.StringVar()
                    N1text = ttk.Combobox(window2, width=15, textvariable=d)

                    x1[number] = ttk.Entry(window2, font=("Times New Roman", 10))
                    c = tk.StringVar()
                    N1box = ttk.Combobox(window2, textvariable=c)

                    ttk.Label(window2, text=("N") + str(number + 1) + ":", font=("Times New Roman", 15)).place(x=60, y=(
                            40 + fireflies))
                    d = tk.StringVar()
                    N1text = ttk.Combobox(window2, width=15, textvariable=d)

                    x1[number].place(x=100, y=(40 + fireflies), width=100)
                    fireflies += 40

                for number in range(x):
                    ttk.Label(window2, text="", font=("Times New Roman", 15)).place(x=60, y=10)
                    d = tk.StringVar()
                    N1text = ttk.Combobox(window2, width=15, textvariable=d)

                    x2[number] = ttk.Entry(window2, font=("Times New Roman", 10))
                    c = tk.StringVar()
                    N1box = ttk.Combobox(window2, textvariable=c)

                    ttk.Label(window2, text=("L") + str(number + 1) + ":", font=("Times New Roman", 15)).place(x=60, y=(
                            40 + fireflies))
                    d = tk.StringVar()
                    N1text = ttk.Combobox(window2, width=15, textvariable=d)

                    x2[number].place(x=100, y=(40 + fireflies), width=100)
                    fireflies += 40

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
                        messagebox.showerror("PyFGH", "Must include only numeric values!!!")
                        holder.setNlist(None)
                        holder.setLlist(None)
                        gc.collect()
                        actionN()

                    window2.destroy()

                    holder.setNlist(valuesN)
                    holder.setLlist(valuesL)

                    print("Inputted values of N: " + str(holder.getNlist()))
                    print("Inputted values of L: " + str(holder.getLlist()))
                    print("Inputted value of D: " + str(holder.getD()))

                    # Enter validation checks
                    for x in holder.getNlist():
                        if x % 2 == 0 or x < 5:
                            messagebox.showerror("PyFGH", "N must be odd, positive integer greater to or equal to 5!!!")
                            clearNdimensions()

                    if holder.getLlist() is not None:
                        for x in holder.getLlist():
                            if x < 0:
                                messagebox.showerror("PyFGH", "L must be positive!!!")
                                clearLdimensions()

                yvalue = int(dimensions.get())


                enter = tk.Button(window2, text='Enter', bd='20', bg='green', fg='white',
                                  command=enter_button).place(x=110, y=(yvalue * 85 + 20))

            else:
                messagebox.showerror("PyFGH", "The Vales For N Have Already Been Assigned!!!")
        except ValueError:
            messagebox.showerror("PyFGH", "Error, Please Select The Dimensions First!!!")
            window2.destroy()
            window.destroy()
            gc.collect()
            main_window()

    # Label get values
    lbutton = tk.Button(window, text='Get Values', bd='10', bg='gray', fg='white',
                        command=actionN).place(x=425, y=90)

    # Label Exit window
    exit = tk.Button(window, text='Exit', bd='10', bg='red', fg='white',
                     command=close_window).place(x=365, y=150)

    # Sends holder to validation file
    def test():

        eq, pes = molecule_gui.molecule_testing(holder)
        gc.collect()
        holder.setEquilMolecule(eq)
        holder.setPES(pes)

    # opens file explorer to have the user to enter file
    def Read_Structures_Button():
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        y = askopenfilename(title='File Explorer for Potential Energy')
        holder.setpotential_energy(y)

    # opens file explorer to have the user to enter file
    def Read_Structures_Button2():
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        x = askopenfilename(title='File Explorer for Equilibrium Structure')
        holder.setequilibrium_file(x)

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
                window.destroy()
                test()
                gc.collect()
                #exit()
            else:
                if calculation2.get() == "Compute With Psi4":
                    windowpsi4 = tk.Tk()
                    style = Style()
                    windowpsi4.title('PyFGH')
                    windowpsi4.geometry('600x200')

                    ttk.Label(windowpsi4, text="Enter Valid Psi4 Method:",
                              font=("Times New Roman", 10)).place(x=25, y=70)

                    n10 = tk.StringVar()
                    psi4 = ttk.Entry(windowpsi4, width=70, textvariable=n10)

                    def psi4enter() :
                        holder.setPsi4Method(psi4.get())
                        print(psi4.get())
                        windowpsi4.destroy()
                        window.destroy()
                        gc.collect()
                        test()


                    readbutton = tk.Button(windowpsi4, text='Enter', bd='10', bg='green', fg='white',
                                           command=psi4enter).place(x=270, y=125)

                    psi4.place(x=160, y=70)
                    windowpsi4.mainloop()



        except ValueError:
            messagebox.showerror("PyFGH", "Data is missing! FILL in ALL of the boxes before hitting calculate!!!")
        except IndexError:  # TODO this is not working properly. After the error restart the interface!
            messagebox.showerror("PyFGH", "Error, Please restart program!!!")
            main_window()
        except ValidationError as e:
            print(e)
            raise
        # except:
        #     print("Unknown PyFGH error occurred!  Please contact the developers to let them know!")
        #     raise

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
        window.geometry("550x255")
        canvas = tkinter.Canvas(window, width=500, height=235)
        canvas.pack()

        text = "  A Python implementation of the Fourier Grid Hamiltonian \n \n Credits: Dr. Jeffrey Woodford, jwoodford@missouriwestern.edu \n" \
               "Nelson Maxey, Tyler Law \n and Josiah Randleman. \n " \
               "Department of Chemistry and Department of Computer Science \n" \
               "Missouri Western State University, St. Joseph, Missouri, USA \n" \
               "\n GitHub Repository: \n https://github.com/jeffwoodford27/PyFGH/tree/main \n" \
                " Licensed under LGPL-3.0"

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

        text = "Please visit https://github.com/jeffwoodford27/PyFGH \n for a helpful README file with detailed instructions \n" \
               "on how to run the program. \n \n" \
               "Send bug reports to jwoodford@missouriwestern.edu"

        x = ttk.Label(window, text=text, font=("Times New Roman", 15))
        x.pack()
        x.place(x=0, y=0)

        # This is the about button.

    help = tk.Button(window, text='Help', bd='10', bg='#F9BB46', fg='white',
                     command=help_window).place(x=303, y=150)


    # This is a button called Read Structures
    readbutton = tk.Button(window, text='Read Equilibrium Structure from File', bd='10', bg='gray', fg='white',
                           command=Read_Structures_Button2).place(x=360, y=200)

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
