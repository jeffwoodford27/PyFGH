
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
        self.N1 = 0
        self.L1 = 0
        self.N2 = 0
        self.L2 = 0
        self.N3 = 0
        self.L3 = 0
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
        self.dimensionvaluesN = []
        self.dimensionvaluesL = []
        self.EquilMolecule = 0
        self.PES = 0



    """
    The following methods are setters. These values get set in test1.py
    """


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

    def setN1(self, N1):
        self.N1 = int(N1)
        return

    def setL1(self, L1):
        self.L1 = L1
        return

    def setN2(self, N2):
        self.N2 = int(N2)
        return

    def setL2(self, L2):
        self.L2 = L2
        return

    def setN3(self, N3):
        self.N3 = int(N3)
        return

    def setL3(self, L3):
        self.L3 = L3
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

    def getD(self):
        return self.D

    def getN1(self):
        return self.N1

    def getN2(self):
        return self.N2

    def getN3(self):
        return self.N3

    def getL1(self):
        return self.L1

    def getL2(self):
        return self.L2

    def getL3(self):
        return self.L3

    def getEquilMolecule(self):
        return self.EquilMolecule

    def getPES(self):
        return self.PES

#TODO take the values in Eignevalues and Eigenvectos and write them to a CSV file in main on line 104.
class OutputData:
    def __init__(self):
        self.eigenvalues = []
        self.eigenvectors = []

    def setEigenvalues(self, evalues):
        self.eigenvalues = evalues
        return

    def setEigenvectors(self, evectors):
        self.eigenvectors = evectors
        return

    def getEigenvalues(self):
        return self.eigenvalues

    def getEigenvectors(self):
        return self.eigenvectors

