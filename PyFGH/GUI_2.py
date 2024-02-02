import gc
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import multiprocessing
import sys
import numpy as np

from PyFGH import molecule_gui
from PyFGH.util import DataObject as DataObject

# class InputObj:
    # def __init__(self):
    #     self.D = 0
    #     self.N = None
    #     self.L = None
    #     self.cores_amount = 0
    #     self.NoEigen = 0
    #     self.PEMethod = None
    #     self.EigenMethod = None
    #     #New
    #     self.equilibrium_file = None
    #     self.potential_energy_file = None
    #     self.EquilMolecule = 0
    #     self.PES = 0
    #     self.Vmethod = 0
    #     self.psi4method = None
    #     self.gui = None



class TextBoxFrame(ttk.LabelFrame):
    def __init__(self, container, txt):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.txtboxstrvar = tk.StringVar()
        self.txtbox = ttk.Entry(self, width=10, textvariable=self.txtboxstrvar)
        self.txtbox.grid(column=0, row=0)

    def get(self):
        return self.txtbox.get()

    def clear(self):
        self.txtboxstrvar.set('')
        return

class LabelFrame(ttk.Frame):
    def __init__(self, container, txt):
        super().__init__(container)

        self.lbl = ttk.Label(self, text=txt)
        self.lbl.grid(column=0, row=0)

class ButtonFrame(ttk.Frame):
    def __init__(self, container, txt, f):
        super().__init__(container)

        self.txtboxbutton = ttk.Button(self, text=txt, command=f)
        self.txtboxbutton.grid(column=0, row=0)

class ComboboxFrame(ttk.LabelFrame):
    def __init__(self, container, txt, dropdownlist):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.cboxstrvar = tk.StringVar()
        self.cbox = ttk.Combobox(self, values=dropdownlist, width=30, textvariable=self.cboxstrvar)
        self.cbox.state(['readonly'])
        self.cbox.grid(column=0, row=0, sticky=tk.NSEW)

    def get(self):
        return self.cbox.get()

    def clear(self):
        self.cboxstrvar.set('')
        return

class ListboxFrame(ttk.LabelFrame):
    def __init__(self, container, txt, dropdownlist):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.list_items = tk.Variable(value=dropdownlist)

        self.listbox = tk.Listbox(self, height=1, listvariable=self.list_items)
        self.listbox.grid(column=0, row=0, sticky=tk.N)

class GUI(tk.Tk):
    def __init__(self, obj):
        super().__init__()

        self.obj = obj

        self.title('PyFGH')
        self.geometry('910x255')
        self.resizable(False, False)

        for i in range(3):
            self.columnconfigure(i,weight=1)
        for i in range(5):
            self.rowconfigure(i,weight=3)

        self.TitleFrame = LabelFrame(self, "A Python Implementation of the Fourier Grid Hamiltonian Method")
        self.TitleFrame.config(borderwidth=5)
        self.TitleFrame.config(padding=(5,5,5,5))
        self.TitleFrame.config(relief='solid')
        self.TitleFrame.grid(columnspan=3, row=0)

        DimensionRange = [i for i in range(1,7)]
        self.DimensionInput = ComboboxFrame(self, "Dimensions: ", DimensionRange)
        self.DimensionInput.grid(column=0, row=1)

        CoresRange = [i for i in range(1,multiprocessing.cpu_count()+1)]
        self.CoresInput = ComboboxFrame(self, "Computer Cores: ", CoresRange)
        self.CoresInput.grid(column=0, row=3)

        NumEigen = [i for i in range(1,11)]
        self.NumEigenInput = ComboboxFrame(self, "Number of Eigenvalues: ", NumEigen)
        self.NumEigenInput.grid(column=1, row=1)

        PEMethod = ["Calculate With Psi4", "Read From File"]
        self.PEMethodInput = ComboboxFrame(self, "PE Input Method: ", PEMethod)
        self.PEMethodInput.grid(column=1, row=3)

        EigenMethod = ["Full Matrix", "Sparse Matrix"]
        self.EigenMethodInput = ComboboxFrame(self, "Eigenvalue Calculation Method: ", EigenMethod)
        self.EigenMethodInput.grid(column=1, row=2)

        self.GetValuesButton = ButtonFrame(self, "Get N, L Values", self.getNLvalues)
        self.GetValuesButton.grid(column=0, row=2)

        self.AboutButton = ButtonFrame(self, "About", self.AboutButtonCommand)
        self.AboutButton.grid(column=2, row=1)

        self.HelpButton = ButtonFrame(self, "Help", self.HelpButtonCommand)
        self.HelpButton.grid(column=2, row=2)

        self.ClearButton = ButtonFrame(self, "Clear", self.ClearButtonCommand)
        self.ClearButton.grid(column=2, row=3)

        self.ExitButton = ButtonFrame(self, "Exit", self.ExitButtonCommand)
        self.ExitButton.grid(column=2, row=4)

        self.GetEquilCoordButton = ButtonFrame(self, "Get Equilibrium Coordinates", self.GetEquilCoordCommand)
        self.GetEquilCoordButton.grid(column=0, row=4)

        self.CalculateButton = ButtonFrame(self, "CALCULATE!", self.CalculateButtonCommand)
        self.CalculateButton.grid(column=1, row=4)

    def getNLvalues(self):
        D = self.DimensionInput.get()
        if (D == ''):
            tk.messagebox.showerror(title="Error", message="Error: First Select D Value")
            return

        D = int(D)
        self.obj.D = D

        w = 200
        h = 20 + 50 * D

        NLwindow = tk.Toplevel(self)
        NLwindow.title("Get N and L Values")
        NLwindow.geometry(str(w) + "x" + str(h))
        NLwindow.attributes("-topmost",1)

        NFrame = []
        LFrame = []
        for i in range(D):
            Nobj = TextBoxFrame(NLwindow, "N"+str(i+1))
            Nobj.grid(column=0, row=i)
            NFrame.append(Nobj)

            Lobj = TextBoxFrame(NLwindow, "L"+str(i+1))
            Lobj.grid(column=1, row=i)
            LFrame.append(Lobj)

        def get_values():
            self.obj.N = None
            self.obj.L = None
            Nval = np.zeros(D, dtype=int)
            Lval = np.zeros(D, dtype=float)

            error_state = False
            msg = ""
            for i in range(D):
                try:
                    Nval[i] = int(NFrame[i].get())
                except ValueError:
                    msg = msg + "Error: N" + str(i+1) + " must be an integer\n"
                    NFrame[i].clear()
                    error_state = True
                else:
                    if (Nval[i] < 5):
                        msg = msg + "Error: N" + str(i+1) + " must be greater than or equal to 5\n"
                        NFrame[i].clear()
                        error_state = True
                    if (Nval[i] % 2 == 0):
                        msg = msg + "Error: N" + str(i+1) + " must be an odd integer\n"
                        NFrame[i].clear()
                        error_state = True

            for i in range(D):
                try:
                    Lval[i] = float(LFrame[i].get())
                except ValueError:
                    msg = msg + "Error: L" + str(i + 1) + " must be a floating point number\n"
                    LFrame[i].clear()
                    error_state = True
                else:
                    if (Lval[i] <= 0):
                        msg = msg + "Error: L" + str(i + 1) + " must be greater than zero\n"
                        LFrame[i].clear()
                        error_state = True

            if (error_state):
                tk.messagebox.showerror(title="Error", message=msg)
            else:
                self.obj.N = np.zeros(D,dtype=int)
                self.obj.L = np.zeros(D,dtype=float)
                for i in range(D):
                    self.obj.N[i] = Nval[i]
                    self.obj.L[i] = Lval[i]
                NLwindow.destroy()

            return

        getValuesButton = ButtonFrame(NLwindow, "Get Values", get_values)
        getValuesButton.grid(columnspan=2, row=D)
        return

    def AboutButtonCommand(self):
        window = tk.Toplevel(self)
        window.title("About")
        window.geometry("550x255")
        canvas = tk.Canvas(window, width=500, height=235)
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
        return

    def HelpButtonCommand(self):
        window = tk.Toplevel(self)
        window.title("Help")
        window.geometry("500x235")
        canvas = tk.Canvas(window, width=500, height=235)
        canvas.pack()

        text = "Please visit https://github.com/jeffwoodford27/PyFGH \n for a helpful README file with detailed instructions \n" \
               "on how to run the program. \n \n" \
               "Send bug reports to jwoodford@missouriwestern.edu"

        x = ttk.Label(window, text=text, font=("Times New Roman", 15))
        x.pack()
        x.place(x=0, y=0)
        return

    def ClearButtonCommand(self):
        print("Clear Button Clicked")
        self.DimensionInput.clear()
        return

    def ExitButtonCommand(self):
        print("Exit Button Clicked")
        self.destroy()
        sys.exit()
        return

    def GetEquilCoordCommand(self):
        print ('Get Equilibrium Coordinate Button Clicked')
        self.Read_Structures_Button2()
        return

    def CalculateButtonCommand(self):
        self.obj.cores_amount = self.CoresInput.get()
        self.obj.NoEigen = self.NumEigenInput.get()
        self.obj.PEMethod = self.PEMethodInput.get()
        self.obj.gui = True
        if self.EigenMethodInput.get() == "Sparse Matrix":
            self.obj.setEigenvalueMethod(True)
        else:
            self.obj.setEigenvalueMethod(False)
        self.obj.psi4method = None
        if self.obj.PEMethod == "Read From File":
            self.obj.setVmethod(self.obj.PEMethod)
            self.Read_Structures_Button()
            self.test(self.obj)


        #destroy window
        self.destroy()
        return

    #collect data function and return self.obj
    def DataReturner(self):
        return self.obj


    def Read_Structures_Button(self):
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        y = askopenfilename(title='File Explorer for Potential Energy')
        self.obj.setpotential_energy(y)

    # opens file explorer to have the user to enter file
    def Read_Structures_Button2(self):
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        x = askopenfilename(title='File Explorer for Equilibrium Structure')
        self.obj.setequilibrium_file(x)

    # def setequilibrium_file(self, equilibrium_file):
    #     self.obj.equilibrium_file = equilibrium_file
    #     return
    #
    # def setpotential_energy(self, potential_energy):
    #     self.obj.potential_energy_file = potential_energy
    #     return
    #
    # def getD(self):
    #     return self.obj.D
    #
    # def getNlist(self):
    #     return self.obj.N
    #
    # def getN(self,j):
    #     return self.obj.N[j]
    #
    # def getLlist(self):
    #     return self.obj.L
    #
    # def getL(self,j):
    #     return self.obj.L[j]
    #
    # def getEquilFile(self):
    #     return self.obj.equilibrium_file
    #
    # def getPESFile(self):
    #     return self.obj.potential_energy_file
    #
    # def setEquilMolecule(self,eq):
    #     self.obj.EquilMolecule = eq
    #     return
    #
    # def setPES(self,pes):
    #     self.obj.PES = pes
    #     return
    #
    def test(self, obj):
        eq, pes = molecule_gui.molecule_testing(obj)
        gc.collect()
        self.obj.setEquilMolecule(eq)
        self.obj.setPES(pes)

    # def setVmethod(self,vmethod):
    #     self.obj.Vmethod = vmethod
    #     return
    #
    # def getVmethod(self):
    #     return self.obj.Vmethod
    #
    # def getEquilMolecule(self):
    #     return self.obj.EquilMolecule
    #
    # def getPES(self):
    #     return self.obj.PES
    #
    # def getCoresAmount(self):
    #     return int(self.obj.cores_amount)
    #
    # def getPsi4Method(self):
    #     return self.obj.psi4method

 #   def getNumberOfEigenvalues(self):
  #      return int(self.obj.NoEigen)

    # def getEigenvalueMethod(self):
    #     return self.obj.EigenMethod
    #
    # def setEigenvalueMethod(self, eigenmethod):
    #     self.obj.EigenMethod = eigenmethod
    #     return
    #
    # def getgui(self):
    #     return self.obj.gui

# obj = InputObj()
# win = GUI(obj)
# win.mainloop()
# print(obj.D, obj.N, obj.L, obj.cores, obj.NoEigen, obj.PEMethod, obj.EigenMethod)

