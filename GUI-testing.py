import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style


def model_prompt(section_1, section_2, section_3):
    global modelParam, modelParam2, modelParam3, modelLabel, modelLabel2, modelLabel3
    if section_1 == 0:  # Harmonic Oscillator
        modelName = "Harmonic Oscillator"
        modelParam = 2
        modelLabel = ["\u03BC", "k"]

    if section_1 == 1:  # Morse Oscillator
        modelName = "Morse Oscillator"
        modelParam = 3
        modelLabel = ["\u03BC", "De", "a"]

    if section_1 == 2:  # Test for models with 4 parameters
        modelName = "Test Oscillator"
        modelParam = 4
        modelLabel = ["a", "b", "c", "d"]

    if section_2 == 0:  # Harmonic Oscillator
        modelName2 = "Harmonic Oscillator"
        modelParam2 = 2
        modelLabel2 = ["\u03BC", "k"]

    if section_2 == 1:  # Morse Oscillator
        modelName2 = "Morse Oscillator"
        modelParam2 = 3
        modelLabel2 = ["\u03BC", "De", "a"]

    if section_3 == 0:  # Harmonic Oscillator
        modelName3 = "Harmonic Oscillator"
        modelParam3 = 2
        modelLabel3 = ["\u03BC", "k"]

    if section_3 == 1:  # Morse Oscillator
        modelName3 = "Morse Oscillator"
        modelParam3 = 3
        modelLabel3 = ["\u03BC", "De", "a"]

    window1 = tk.Tk()
    style = Style()
    window1.title('Testing')
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
        a1 = ttk.Entry(window1, textvariable=q1var[j], font=("Times New Roman", 10)).place(x=140, y=y)

        j += 1
        y += 35

    for j in range(modelParam2):
        # append a string variable to the q2var list
        q2var.append(tk.StringVar())
        ttk.Label(window1, text=modelLabel2[j] + " for Q2:",
                  font=("Times New Roman", 15)).place(x=50, y=y)
        # set text variable as q3var[j] , each entry will have separate index in the list
        a2 = ttk.Entry(window1, textvariable=q2var[j], font=("Times New Roman", 10)).place(x=140, y=y)
        j += 1
        y += 35

    for j in range(modelParam3):
        # append a string variable to the q3var list
        q3var.append(tk.StringVar())
        ttk.Label(window1, text=modelLabel3[j] + " for Q3:",
                  font=("Times New Roman", 15)).place(x=50, y=y)
        # set text variable as q3var[j] , each entry will have separate index in the list
        a3 = ttk.Entry(window1, textvariable=q3var[j], font=("Times New Roman", 10)).place(x=140, y=y)
        j += 1
        y += 35

    def enter_button():
        # add values from entry to the list using text variable
        for k in range(modelParam):
            entries.append('Q1 ' + modelLabel[k] + ' is ' + q1var[k].get())
        for k in range(modelParam2):
            entries.append('Q2 ' + modelLabel2[k] + ' is ' + q2var[k].get())
        for k in range(modelParam3):
            entries.append('Q3 ' + modelLabel3[k] + ' is ' + q3var[k].get())

        print(entries)
        #save_file_prompt()
        window1.destroy()

    enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                      command=enter_button).place(x=110, y=y)

    window1.mainloop()


model_prompt(1, 1, 1)