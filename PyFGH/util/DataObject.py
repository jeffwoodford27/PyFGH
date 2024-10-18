import numpy as np
from PyFGH import molecule_gui
import gc

"""
DataObject is a place to hold data. All values in these classes are first assigned to zero. In GUI_old.py these values get 
reassigned new values based on the input of the GUI. When the GUI is terminated, these values change from zero to the 
values from the input. After the GUI is terminated, these new values can be called from any file in this project.
"""

class InputData:

    def __init__(self):
        self.D = 0
        self.cores_amount = 1
        self.N = None
        self.L = None
        self.equilibrium_file = None
        self.potential_energy_file = None
        self.EquilMolecule = 0
        self.PES = 0
        self.num_eigenvalues = 10
        self.eigenvalue_flag = False
        self.Vmethod = 0
        self.model_data = None
        self.psi4method = None
        self.inputobject = None
        self.calculation = None
        self.calculation2 = None
        self.gui = None

    """
    The following methods are setters. These values get set in test1.py
    """


    def setinputobject(self, inputobject):
        self.inputobject = inputobject
        return

    def getinputobject(self):
        return self.inputobject

    def setcalculation(self, calculation):
        self.calculation = calculation
        return

    def getcalculation(self):
        return self.calculation

    def setcalculation2(self, calculation2):
        self.calculation2 = calculation2
        return

    def getcalculation2(self):
        return self.calculation2

    """
    The following methods are setters. These values get set in test1.py
    """

    def setcores_amount(self, cores):
        self.cores_amount = cores
        return

    def setequilibrium_file(self, equilibrium_file):
        self.equilibrium_file = equilibrium_file
        return

    def setpotential_energy(self, potential_energy):
        self.potential_energy_file = potential_energy
        return

    def setD(self,D):
        self.D = D
        return

    def setNlist(self,N):
        self.N = np.array(N,dtype=int)
        return

    def setLlist(self,L):
        self.L = np.array(L,dtype=float)
        return

    def setEquilMolecule(self,eq):
        self.EquilMolecule = eq
        return

    def setPES(self,pes):
        self.PES = pes
        return

    def setNumberOfEigenvalues(self, num):
        self.num_eigenvalues = num
        return

    def setEigenvalueMethod(self, eigenmethod):
        print(self.eigenvalue_flag)
        self.eigenvalue_flag = eigenmethod
        return

    def setVmethod(self,vmethod):
        self.Vmethod = vmethod
        return

    def setPsi4Method(self,method):
        self.psi4method = method
        return

    def getD(self):
        return self.D

    def getNlist(self):
        return self.N

    def getN(self,j):
        return self.N[j]

    def getLlist(self):
        return self.L

    def getL(self,j):
        return self.L[j]

    def getEquilFile(self):
        return self.equilibrium_file

    def getPESFile(self):
        return self.potential_energy_file

    def getEquilMolecule(self):
        return self.EquilMolecule

    def getPES(self):
        return self.PES

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues

    def getEigenvalueMethod(self):
        print(self.eigenvalue_flag)
        return self.eigenvalue_flag

    def getVmethod(self):
        return self.Vmethod

    def getPsi4Method(self):
        return self.psi4method

    def getCoresAmount(self):
        return int(self.cores_amount)

    def getgui(self):
        return self.gui

    def validate(self):
        if not self.checkD():
            return False
        if not self.checkN():
            return False
        if not self.checkL():
            return False
        if not self.checkEqPes():
            return False
        return True

    def checkD(self):
        if self.D > 0 & self.D is int:
            print("D must be an integer")
            return True
        else:
            return False

    def checkN(self):
        for i in range(self.D):
            if(self.N[i] is not int):
                print("N must be an integer")
                return False
            if (self.N[i] < 5):
                print("N must be greater than 5")
                return False
            if (self.N[i] % 2 == 0):
                print("N must be an odd number")
                return False
            return True

    def checkL(self):
        for i in range(self.D):
            if(self.L[i] is not float):
                print("L must be a float")
                return False
            if (self.L[i] <= 0):
                print("L must be greater than 0")
                return False
            return True

    def checkEqPes(self):
        eq, pes = molecule_gui.molecule_testing(self)
        gc.collect()
        self.setEquilMolecule(eq)
        self.setPES(pes)



#TODO take the values in Eignevalues and Eigenvectos and write them to a CSV file in main on line 104.
class OutputData:
    def __init__(self):
        self.num_eigenvalues = 0
        self.eigenvalues = []
        self.eigenvectors = []

    def setEigenvalues(self, evalues):
        self.eigenvalues = evalues
        return

    def setEigenvectors(self, evectors):
        self.eigenvectors = evectors
        return

    def setNumberOfEigenvalues(self, num):
        self.num_eigenvalues = num
        return

    def getEigenvalue(self, idx):
        return self.eigenvalues[idx]

    def getEigenvalues(self):
        return self.eigenvalues

    def getEigenvector(self, idx):
        return self.eigenvectors[idx]

    def getEigenvectors(self):
        return self.eigenvectors

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues

    def getOutputAsJson(self):
        return {
            "num_eigenvalues": self.num_eigenvalues,
            "eigenvalues": self.eigenvalues,
            "eigenvectors": self.eigenvectors
        }
