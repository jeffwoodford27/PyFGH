# Interface between GUI and Calculation Scripts
import os
# from tqdm.contrib.concurrent import process_map

import numpy as np
import scipy
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import csv
from tkinter import *

import RemoteGmatrix
import RemoteTmatrix
import RemoteVmatrix
from util import DataObject


list2 = []
list3 = []

with open('countries.csv') as f:
    for row in f:
        list2.append(row.split(',')[0])
        print(row)
        list2.append(row)

    for element in list2:
        list3.append(element.strip())


list3.pop(0)
list3.pop(2)
list3.pop(1)
list3[0].split(",")
list5 = []
list6 = []

with open('PES.csv') as f:
    for row in f:
        list5.append(row.split(',')[0])
        print(row)
        list5.append(row)

with open('EquilMolecule.csv') as f:
    for row in f:
        list6.append(row.split(',')[0])
        print(row)
        list6.append(row)


PES = list5[0]
EquilMolecule = list6[0]

N1 = list3[0][0]
N2 = list3[0][1]
N3 = list3[0][3]
L1 = list3[0][4]
L2 = list3[0][5]
L3 = list3[0][6]


def window(x):
    File = open(x)
    Reader = csv.reader(File)
    Data = list(Reader)
    del (Data[0])

    list_of_entries = []
    x = 0
    for x in list(range(0, len(Data))):
        list_of_entries.append(Data[x])
        x += 1

    root = Tk()
    v = Scrollbar(root)
    v2 = Scrollbar(root)
    root.geometry('1550x800')
    root.title('Results')
    v.pack(side=RIGHT, fill=Y)
    SHBar = tk.Scrollbar(root,
                         orient=tk.HORIZONTAL)
    SHBar.pack(side=tk.BOTTOM,
               fill="x")
    var = StringVar(value=list_of_entries)
    listbox1 = Listbox(root, listvariable=var)
    listbox1.pack(side=LEFT, fill=BOTH)
    listbox1.config(width=1550, height=800, yscrollcommand=v.set)
    SHBar.config(command=listbox1.xview)
    root.mainloop()


def main():
    pass


def passToCalc(dataObj):
    print("Got an object.")
    # print(dataObj)
    print("Creating GMatrix")
    N = [N1, N2, N3]
    GMat = RemoteGmatrix.calcGMatrix(N, PES, EquilMolecule)
    holder = DataObject.InputData()
    VMat = RemoteVmatrix.VMatrixCalc(dataObj)
    print("Done with VMatrix")
    TMat = RemoteTmatrix.TMatrixCalc(dataObj, GMat)
    print("Done with TMatrix")
    HMat = VMat + TMat
    pd.DataFrame(HMat).to_csv("testing.csv") # changed this one
    holder.setHmat(HMat)

    print("Calculating eigenvalues")
    eigenval, eigenvec = scipy.linalg.eigh(HMat)
    eigenval = eigenval * 219474.6
    wfnorder = np.argsort(eigenval)
    print("Eigenvalues:")
    for i in range(1, 20):
        print(eigenval[wfnorder[i]] - eigenval[wfnorder[0]])

    z = str(holder.name_of_file) + ".csv"
    window(z)
    if os.path.exists("holder.csv"):
        os.remove("holder.csv")


# r = process_map(main, range(0, 30), max_workers=12)
if __name__ == '__main__':
    main()
