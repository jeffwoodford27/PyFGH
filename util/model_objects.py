import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style

import numpy as np

from util import InputData


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


def model_prompt(potential_model):
    window1 = tk.Tk()
    style = Style()
    window1.title('PyFGH Parameters')
    box_length = 103
    for q in range(3):
        box_length = box_length + 33 * potential_model[q].nparam
    box_len_str = '300x' + str(box_length)
    window1.geometry(box_len_str)

    entries = []
    qvar = np.empty(3, dtype=list)
    for i in range(3):
        qvar[i] = []
    j = 0
    y = 5

    for q in range(3):
        for qparam in range(potential_model[q].nparam):
            qvar[q].append(tk.StringVar())

            ttk.Label(window1, text=potential_model[q].label[qparam] + " for Q:" + str(q + 1) + ":",
                      font=("Times New Roman", 15)).place(x=50, y=y)
            # set text variable as q1var[j] , each entry will have separate index in the list
            a1 = ttk.Entry(window1, textvariable=qvar[q][qparam], font=("Times New Roman", 10)).place(x=140, y=y)

            j += 1
            y += 35

    def enter_button():
        for q in range(3):
            param_list = []
            for qparam in range(potential_model[q].nparam):
                param_list.append(qvar[q][qparam].get())
            potential_model[q].set_param(param_list)
        for q in range(3):
            for qparam in range(potential_model[q].nparam):
                print(potential_model[q].param[qparam])
        InputData.output.items.model_data = potential_model
        print(InputData.output.items.model_data)
        window1.destroy()

    enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                      command=enter_button).place(x=110, y=y)

    window1.mainloop()


def output():
    sections = []
    for i in range(3):
        if InputData.output.items.v[i] == "Model-Harmonic Oscillator":
            sections.append(Harmonic_Oscillator())
        elif InputData.output.items.v[i] == "Model-Morse Oscillator":
            sections.append(Harmonic_Oscillator())
        elif InputData.output.items.v[i] == "Model-Test Oscillator":
            sections.append(Harmonic_Oscillator())


#test = [Harmonic_Oscillator(), Morse_Oscillator(), Test_Oscillator()]
#model_prompt(test)

"""

def model_prompt(section_1, section_2, section_3):

    if section_1 == "Harmonic Oscillator":  # Harmonic Oscillator
        modelName = "Harmonic Oscillator"
        modelParam = 2
        modelLabel = ["\u03BC", "k"]

    if section_1 == "Morse Oscillator":  # Morse Oscillator
        modelName = "Morse Oscillator"
        modelParam = 3
        modelLabel = ["\u03BC", "De", "a"]

    if section_1 == "Test Oscillator":
        modelName = "Test Oscillator"
        modelParam = 4
        modelLabel = ["a", "b", "c", "d"]

    if section_2 == "Test Oscillator":
        modelName2 = "Test Oscillator"
        modelParam2 = 4
        modelLabel2 = ["a", "b", "c", "d"]

    if section_3 == "Test Oscillator":
        modelName3 = "Test Oscillator"
        modelParam3 = 4
        modelLabel3 = ["a", "b", "c", "d"]

    if section_2 == "Harmonic Oscillator":  # Harmonic Oscillator
        modelName2 = "Harmonic Oscillator"
        modelParam2 = 2
        modelLabel2 = ["\u03BC", "k"]

    if section_2 == "Morse Oscillator":  # Morse Oscillator
        modelName2 = "Morse Oscillator"
        modelParam2 = 3
        modelLabel2 = ["\u03BC", "De", "a"]

    if section_3 == "Harmonic Oscillator":  # Harmonic Oscillator
        modelName3 = "Harmonic Oscillator"
        modelParam3 = 2
        modelLabel3 = ["\u03BC", "k"]

    if section_3 == "Morse Oscillator":  # Morse Oscillator
        modelName3 = "Morse Oscillator"
        modelParam3 = 3
        modelLabel3 = ["\u03BC", "De", "a"]

    window1 = tk.Tk()
    style = Style()
    window1.title('PyFGH')
    box_length = 103
    box_length = box_length + 33 * (modelParam + modelParam2 + modelParam3)
    box_len_str = '300x' + str(box_length)
    window1.geometry(box_len_str)

    j = 0
    y = 5

    entries = []
    # create 3 variable lists, for Q1, Q2 and Q3
    q1var = []
    q2var = []
    q3var = []

    for j in range(modelParam):
        # append a string variable to the q1var list
        q1var.append(tk.StringVar())
        ttk.Label(window1, text=modelLabel[j] + " for Q1:",
                  font=("Times New Roman", 15)).place(x=50, y=y)
        # set text variable as q1var[j] , each entry will have separate index in the list
        ttk.Entry(window1, textvariable=q1var[j], font=("Times New Roman", 10)).place(x=140, y=y)

        j += 1
        y += 35

    for j in range(modelParam2):
        # append a string variable to the q2var list
        q2var.append(tk.StringVar())
        ttk.Label(window1, text=modelLabel2[j] + " for Q2:",
                  font=("Times New Roman", 15)).place(x=50, y=y)
        # set text variable as q3var[j] , each entry will have separate index in the list
        ttk.Entry(window1, textvariable=q2var[j], font=("Times New Roman", 10)).place(x=140, y=y)
        j += 1
        y += 35

    for j in range(modelParam3):
        # append a string variable to the q3var list
        q3var.append(tk.StringVar())
        ttk.Label(window1, text=modelLabel3[j] + " for Q3:",
                  font=("Times New Roman", 15)).place(x=50, y=y)
        # set text variable as q3var[j] , each entry will have separate index in the list
        ttk.Entry(window1, textvariable=q3var[j], font=("Times New Roman", 10)).place(x=140, y=y)
        j += 1
        y += 35

    def enter_button():
        # add values from entry to the list using text variable
        for values in range(modelParam):
            entries.append(modelName + ': Q1 ' + modelLabel[values] + ' is ' + q1var[values].get())
        for values in range(modelParam2):
            entries.append(modelName2 + ': Q2 ' + modelLabel2[values] + ' is ' + q2var[values].get())
        for values in range(modelParam3):
            entries.append(modelName3 + ': Q3 ' + modelLabel3[values] + ' is ' + q3var[values].get())

        InputData.output.items.model_data = entries
        print(InputData.output.items.model_data, 'this is from input data')

        # save_file_prompt()
        window1.destroy()

    enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                      command=enter_button).place(x=110, y=y)

    window1.mainloop()



"""
