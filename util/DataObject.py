class holdData:
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
    file_name = 0
    model_data = []

class Harmonic_Oscillator:
    def __init__(self):
        self.type = 0
        self.name = "Harmonic Oscillator"
        self.nparam = 2
        self.label = ["\u03BC", "k"]
        self.param = np.zeros(self.nparam, float)

    def set_param(self, param_list):
        for i in range(self.nparam):
            self.param[i] = param_list[i]
        return

class Morse_Oscillator:
    def __init__(self):
        self.type = 1
        self.name = "Morse Oscillator"
        self.nparam = 3
        self.label = ["\u03BC", "De", "a"]
        self.param = np.zeros(self.nparam, float)

    def set_param(self, param_list):
        for i in range(self.nparam):
            self.param[i] = param_list[i]
        return

class Test_Oscillator:
    def __init__(self):
        self.type = 2
        self.name = "Test Oscillator"
        self.nparam = 4
        self.mu = 0
        self.label = ["a", "b", "c", "d"]
        self.param = np.zeros(self.nparam, float)

    def set_param(self, param_list):
        for i in range(self.nparam):
            self.param[i] = param_list[i]
        return


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
        self.model_data = []

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


class OutputData:
    def __init__(self):
        self.eigenvalues = []

    def setEigenvalues(self, evalues):
        for i in range(len(evalues)):
            self.eigenvalues.append(evalues[i])
        return

