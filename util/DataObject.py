import numpy as np

"""
DataObject is a place to hold data. All values in these classes are first assigned to zero. In GUI.py these values get 
reassigned new values based on the input of the GUI. When the GUI is terminated, these values change from zero to the 
values from the input. After the GUI is terminated, these new values can be called from any file in this project.
"""


class holdData:
    Hmat = []
    molecule = 0
    q_equation1 = 0
    q_equation2 = 0
    q_equation3 = 0
    N1 = 0
    L1 = 0
    N2 = 0
    L2 = 0
    N3 = 0
    L3 = 0
    t = 0
    g = 0
    v = []
    name_of_file = 0
    file_name = 0
    model_data = []  # This doesn't work
    host = 0
    user = 0
    password = 0
    remote = 0


class InputData:

    def __init__(self):
        self.molecule = 0
        self.q_equation1 = 0
        self.q_equation2 = 0
        self.q_equation3 = 0
        self.N1 = 0
        self.L1 = 0
        self.N2 = 0
        self.L2 = 0
        self.N3 = 0
        self.L3 = 0
        self.t = 0
        self.g = 0
        self.v = []
        self.file_name = 0
        self.model_data = []  # This does not work
        self.message = 0
        self.sum = 0
        self.host = 0
        self.user = 0
        self.password = 0
        self.remote = 0
        self.Hmat = []
        name_of_file = 0

    """
    The following methods are setters. These values get set in test1.py
    """
    def setname_of_file(self, name_of_file):
        self.name_of_file = name_of_file
        return
    def setHmat(self, Hmat):
        self.Hmat = Hmat
        return

    def setMolecule(self, molecule):
        self.molecule = molecule
        return

    def setQ1(self, q_equation1):
        self.q_equation1 = q_equation1
        return

    def setQ2(self, q_equation2):
        self.q_equation2 = q_equation2
        return

    def setQ3(self, q_equation3):
        self.q_equation3 = q_equation3
        return

    def setN1(self, N1):
        self.N1 = N1
        return

    def setL1(self, L1):
        self.L1 = L1
        return

    def setN2(self, N2):
        self.N2 = N2
        return

    def setL2(self, L2):
        self.L2 = L2
        return

    def setN3(self, N3):
        self.N3 = N3
        return

    def setL3(self, L3):
        self.L3 = L3
        return

    def setT(self, t):
        self.t = t
        return

    def setV(self, v):
        self.v = v
        return

    def setG(self, g):
        self.g = g
        return

    def setV(self, v):
        self.v = v
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


class OutputData:
    def __init__(self):
        self.eigenvalues = []

    def setEigenvalues(self, evalues):
        for i in range(len(evalues)):
            self.eigenvalues.append(evalues[i])
        return


class atom:
    def __init__(self,m,x,y,z):
        self.m = m
        self.x = x
        self.y = y
        self.z = z

class molecule:
    def __init__(self,N,m,x,y,z):
        self.N = N
        self.at = []
        for i in range(0,N):
            self.at.append(atom(m[i],x[i],y[i],z[i]))