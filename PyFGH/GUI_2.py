import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import multiprocessing
import sys
import numpy as np
from PyFGH import GUI_Classes as guc
from PyFGH import Constants as co
from PyFGH.util import DataObject

# This is the second and current GUI implementation
# It will be given an object of type DataObject that the GUI will input values into
# The calculate button command will drive the placing of values
# The majority of error checking happens here or in the DataObject

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Sets the self.obj to the input data object
        self.obj = DataObject.InputData()
        self.obj.setgui(True)
        # Creation of the GUI window and buttons along with it onward
        self.title('PyFGH')
        self.geometry('910x255')
        self.resizable(False, False)

        for i in range(3):
            self.columnconfigure(i,weight=1)
        for i in range(5):
            self.rowconfigure(i,weight=3)

        self.TitleFrame = guc.LabelFrame(self, "A Python Implementation of the Fourier Grid Hamiltonian Method")
        self.TitleFrame.config(borderwidth=5)
        self.TitleFrame.config(padding=(5,5,5,5))
        self.TitleFrame.config(relief='solid')
        self.TitleFrame.grid(columnspan=3, row=0)

        DimensionRange = [i for i in range(1,co.MAXDIM+1)]
        self.DimensionInput = guc.ComboboxFrame(self, "Dimensions: ", DimensionRange)
        self.DimensionInput.set(DimensionRange.index(self.obj.get("D")))
        self.DimensionInput.grid(column=0, row=1)

        CoresRange = [i for i in range(1,multiprocessing.cpu_count()+1)]
        self.CoresInput = guc.ComboboxFrame(self, "Computer Cores: ", CoresRange)
        self.CoresInput.set(CoresRange.index(self.obj.get("NCores")))
        self.CoresInput.grid(column=0, row=3)

        NumEigenRange = [i for i in range(1, co.MAXEIG+1)]
        self.NumEigenInput = guc.ComboboxFrame(self, "Number of Eigenvalues: ", NumEigenRange)
        self.NumEigenInput.set(NumEigenRange.index(self.obj.get("NEigen")))
        self.NumEigenInput.grid(column=1, row=1)

        self.PEButton = guc.ButtonFrame(self, "Choose Potential Energy Method", self.ChoosePEMethod)
        self.PEButton.grid(column=1, row=3)

        EigenMethod = co.MATRIX
        self.EigenMethodInput = guc.ComboboxFrame(self, "Eigenvalue Calculation Method: ", EigenMethod)
        self.EigenMethodInput.set(EigenMethod.index(self.obj.get("EigenMethod")))
        self.EigenMethodInput.grid(column=1, row=2)

        self.GetValuesButton = guc.ButtonFrame(self, "Get N, L Values", self.getNLvalues)
        self.GetValuesButton.grid(column=0, row=2)

        self.AboutButton = guc.ButtonFrame(self, "About", self.AboutButtonCommand)
        self.AboutButton.grid(column=2, row=1)

        self.HelpButton = guc.ButtonFrame(self, "Help", self.HelpButtonCommand)
        self.HelpButton.grid(column=2, row=2)

        self.ClearButton = guc.ButtonFrame(self, "Clear", self.ClearButtonCommand)
        self.ClearButton.grid(column=2, row=3)

        self.ExitButton = guc.ButtonFrame(self, "Exit", self.ExitButtonCommand)
        self.ExitButton.grid(column=2, row=4)

        self.GetEquilCoordButton = guc.ButtonFrame(self, "Get Equilibrium Coordinates", self.GetEquilFileCommand)
        self.GetEquilCoordButton.grid(column=0, row=4)

        self.CalculateButton = guc.ButtonFrame(self, "CALCULATE!", self.CalculateButtonCommand)
        self.CalculateButton.grid(column=1, row=4)

    # getNLvalues will take the value of D and generate corresponding amount of N L values
    # User will then directly type N and L into boxes in a new window
    def getNLvalues(self):
        D = self.DimensionInput.get()
        if (D == ''):
            tk.messagebox.showerror(title="Error", message="Error: First Select D Value")
            return

        D = int(D)
        self.obj.set("D",D)

        w = 200
        h = 20 + 50 * D

        NLwindow = tk.Toplevel(self)
        NLwindow.title("Get N and L Values")
        NLwindow.geometry(str(w) + "x" + str(h))
        NLwindow.attributes("-topmost",1)

        NFrame = []
        LFrame = []

        Ndefault = self.obj.get("N")
        Ldefault = self.obj.get("L")
        for i in range(D):
            Nobj = guc.TextBoxFrame(NLwindow, "N"+str(i+1))
            if (i < len(Ndefault)):
                Nobj.insert(Ndefault[i])
            Nobj.grid(column=0, row=i)
            NFrame.append(Nobj)

            Lobj = guc.TextBoxFrame(NLwindow, "L"+str(i+1))
            if (i < len(Ldefault)):
                Lobj.insert(Ldefault[i])
            Lobj.grid(column=1, row=i)
            LFrame.append(Lobj)
        # Function within getNLValues to error check values inputted
        # If correct it will proceed to set the values
        def get_values():
            Nval = []
            Lval = []

            error_state = False
            msg = ""


            [Nval.append(NFrame[i].get()) for i in range(D)]
            self.obj.set("N",Nval)
            error_state = not self.obj.validate(param="N")
            if error_state:
                msg = msg + self.obj.validate_msg
                [NFrame[i].clear() for i in range(D)]
                self.obj.set("N",[])

            [Lval.append(LFrame[i].get()) for i in range(D)]
            self.obj.set("L",Lval)
            error_state = not self.obj.validate(param="L")
            if error_state:
                msg = msg + self.obj.validate_msg
                [LFrame[i].clear() for i in range(D)]
                self.obj.set("L",[])

            if error_state:
                tk.messagebox.showerror(title="Error", message=msg)
            else:
                NLwindow.destroy()

            return

        getValuesButton = guc.ButtonFrame(NLwindow, "Get Values", get_values)
        getValuesButton.grid(columnspan=2, row=D)
        return

    # Minor command buttons onward
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

    # This will open file explorer to input the equilibrium file
    def GetEquilFileCommand(self):
        print ('Get Equilibrium Coordinate Button Clicked')
        self.obj.set("EqFile",self.Read_Structures_Button('File Explorer for Equilibrium Structure'))
        return

    # This method prompts the user to choose read from file or calculate with psi4
    def ChoosePEMethod(self):
        window = tk.Toplevel(self)
        window.title("Choose potential energy method")
        window.geometry("500x235")
        PEMethodInput = guc.ComboboxFrame(window, "PE Input Method: ", co.CMETHOD)
        PEMethodInput.set(co.CMETHOD.index(self.obj.get("PEMethod")))
        PEMethodInput.grid(column=0, row=0)

        # Internal method that directs the user depending on the choice from above
        def PEMethodget():
            PEMethod = PEMethodInput.get()
            if PEMethod == co.READ:
                self.obj.set("PEMethod",co.READ)
                self.obj.set("Psi4Method",None)
                self.obj.set("PEFile",self.Read_Structures_Button('File Explorer for Potential Energy'))
                window.destroy()
            if PEMethod == co.CPSI:
                self.obj.set("PEMethod",co.CPSI)
                self.obj.set("PEFile",None)
                self.InputPsi4Method(window)
            return

        getMethodButton = guc.ButtonFrame(window, "Get Method", PEMethodget)
        getMethodButton.grid(column=0, row=1)
        return

    # This method runs if user selected psi4 calculation
    def InputPsi4Method(self, window):

        # IMPORTANT: This line underneath are the options of psi4 calculation
        Psi4method = guc.ComboboxFrame(window,"Choose Method", co.PSI4M)
        Psi4method.set(co.PSI4M.index(self.obj.get("Psi4Method")))
        Psi4method.grid(column=1, row=0)

        # Internal method to receive choice user selected
        def InputPsi4Methodget():
            self.obj.set("Psi4Method",Psi4method.get())
            window.destroy()
            return

        getMethodButton = guc.ButtonFrame(window, "Get Method", InputPsi4Methodget)
        getMethodButton.grid(column=1, row=1)
        return

    # This command drives the entire GUI, many values are set here
    # The calculation will proceed if the validate function returns True
    # Otherwise the user will have to fix any errors
    def CalculateButtonCommand(self):
        self.obj.set("D",int(self.DimensionInput.get()))
        print(self.obj.get("EqFile"))
        if self.obj.get("EqFile") is None or self.obj.get("EqFile") == "":
            self.GetEquilFileCommand()
        self.obj.set("NCores",int(self.CoresInput.get()))
        self.obj.set("NEigen",int(self.NumEigenInput.get()))
        self.obj.set("EigenMethod",self.EigenMethodInput.get())

        #destroy window
        if self.obj.validate_all():
            self.destroy()
            return
        else:
            print("Wrong Input")
            return

    #collect data function and return self.obj
    def DataReturner(self):
        return self.obj

    # Method that opens the file explorer
    def Read_Structures_Button(self, Etitle):
        global opened
        """
            Note: xlsx files are not accepted. Can only take CSV files or else the code will break.
            XLSX files do not abide by UTF-8 formatting and is a pain to get it to work. So to save everyone
            time just only use a CSV file format!!!!!!!!!! Excel has the ability to save it to CSV format. To find out 
            how to save it to that format, just google it. This is the end of my rant. Happy Coding!
        """

        y = askopenfilename(title=Etitle)
        return y
