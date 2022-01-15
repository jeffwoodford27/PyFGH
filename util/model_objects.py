
import numpy as np
# For every new model, it must be add to the oscillator list
Oscillator_List = ['Harmonic_Oscillator', 'Morse_Oscillator', 'Test_Oscillator', 'Hi']
Models_List = []

class Harmonic_Oscillator:
    def __init__(self):
        self.type = 0
        self.name = "Harmonic Oscillator"
        self.nparam = 2
        self.label = ["\u03BC", "k"]
        self.param = np.zeros(self.nparam, float)
        Models_List.append(self)

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
        Models_List.append(self)

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
        Models_List.append(self)

    def set_param(self, param_list):
        for i in range(self.nparam):
            self.param[i] = param_list[i]
        return

class Hi:
    def __init__(self):
        self.type = 3
        self.name = "Hi"
        self.nparam = 4
        self.mu = 0
        self.label = ["z", "y", "x", "w"]
        self.param = np.zeros(self.nparam, float)
        Models_List.append(self)

    def set_param(self, param_list):
        for i in range(self.nparam):
            self.param[i] = param_list[i]
        return

