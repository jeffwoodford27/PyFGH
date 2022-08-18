
"""
DataObject is a place to hold data. All values in these classes are first assigned to zero. In GUI.py these values get 
reassigned new values based on the input of the GUI. When the GUI is terminated, these values change from zero to the 
values from the input. After the GUI is terminated, these new values can be called from any file in this project.
"""
class test:
    equilibrium_file = 0
    potential_energy_file = 0
    testing = 0
    N1 = 0
    L1 = 0
    N2 = 0
    L2 = 0
    N3 = 0
    L3 = 0
    PES = 0
    NewFileholder = 0


    def setEqulibrium(self, equilibrium_file):
        self.equilibrium_file = equilibrium_file
        return

    def settesting(self, testing):
        self.testing = testing
        return


class InputData:

    def __init__(self):
        self.D = 3
        self.name_of_file = 0
        self.cores_amount = 1
        self.N = None
        self.L = None
        self.file_name = 0
        self.message = 0
        self.sum = 0
        self.host = 0
        self.user = 0
        self.password = 0
        self.remote = 0
        self.equilibrium_file = 0
        self.potential_energy_file = 0
        self.value_holder = 0
        self.EquilMolecule = 0
        self.PES = 0
        self.error = 0

        self.num_eigenvalues = 10
        self.eigenvalue_flag = True

        self.Vmethod = 0
        self.model_data = None

        self.psi4method = None

        self.psi4method = None

        self.inputobject = None

        self.calculation = None

        self.calculation2 = None

        self.valuesN = None

        self.valuesL = None

    """
    The following methods are setters. These values get set in test1.py
    """

    def setvaluesN(self, valuesN):
        self.valuesN = valuesN
        return

    def getvaluesN(self):
        return self.valuesN

    def setvaluesL(self, valuesL):
        self.valuesL = valuesL
        return

    def getvaluesL(self):
        return self.valuesL

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

    def seterror(self, error):
        self.error = error
        return
    def setvalue_holder(self, value_holder):
        self.value_holder = value_holder
        return

    def setcores_amount(self, cores):
        self.cores_amount = cores
        return

    def setequilibrium_file(self, equilibrium_file):
        self.equilibrium_file = equilibrium_file
        return

    def setpotential_energy(self, potential_energy):
        self.potential_energy_file = potential_energy
        return

    def setname_of_file(self, name_of_file):
        self.name_of_file = name_of_file
        return

    def setHmat(self, Hmat):
        self.Hmat = Hmat
        return

    def setD(self,D):
        self.D = D
        return

    def setNlist(self,N):
        self.N = N
        return

    def setLlist(self,L):
        self.L = L
        return

    def setFileName(self, file_name):
        self.file_name = file_name
        return

    def setModelData(self, model_data):
        self.model_data = model_data
        return

    def setMessage(self, message):
        self.message = message
        return

    def set_sum(self, sum):
        self.sum = sum
        return

    def set_host(self, host):
        self.host = host
        return

    def set_user(self, user):
        self.user = user
        return

    def set_password(self, password):
        self.password = password
        return

    def set_remote(self, remote):
        self.remote = remote
        return

    def set_name_of_file(self, name_of_file):
        self.name_of_file = name_of_file
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

    def getError(self):
        return self.error

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues

    def getEigenvalueMethod(self):
        return self.eigenvalue_flag

    def getVmethod(self):
        return self.Vmethod

    def getPsi4Method(self):
        return self.psi4method


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

    def getEigenvalues(self):
        return self.eigenvalues

    def getEigenvectors(self):
        return self.eigenvectors

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues
