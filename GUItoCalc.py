# Interface between GUI and Calculation Scripts
import os
# from tqdm.contrib.concurrent import process_map
import Vmatrix
import Tmatrix
import Gmatrix
import numpy as np
import scipy
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, NW, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import csv
from tkinter import *
from util import DataObject
from util.DataObject import OutputData


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
    # print("Got an object.")
    # print(dataObj)

    N = [dataObj.N1, dataObj.N2, dataObj.N3]
    print("Creating G Matrix")
    GMat = Gmatrix.calcGMatrix(N, dataObj.PES, dataObj.EquilMolecule)
    holder = DataObject.InputData()
    print("Creating V Matrix")
    VMat = Vmatrix.VMatrixCalc(dataObj)
    print("Done with V Matrix")
    print("Creating T Matrix")
    TMat = Tmatrix.TMatrixCalc(dataObj, GMat)
    print("Done with T Matrix")
    HMat = VMat + TMat
    # pd.DataFrame(HMat).to_csv(str(holder.name_of_file) + ".csv")
    # holder.setHmat(HMat)

    print("Calculating eigenvalues")
    eigenval, eigenvec = scipy.linalg.eigh(HMat)
    eigenval = eigenval * 219474.6
    wfnorder = np.argsort(eigenval)

    Npts = np.prod(N)
    eigenvalsort = np.zeros(Npts, float)
    eigenvecsort = np.zeros([Npts, Npts], float)

    for i in range(Npts):
        eigenvalsort[i] = eigenval[wfnorder[i]]
        for j in range(Npts):
            eigenvecsort[i] = eigenvec[j][wfnorder[i]]

    ResultObj = OutputData()
    ResultObj.setEigenvalues(eigenvalsort)
    ResultObj.setEigenvectors(eigenvecsort)
    hola = []
    hola.append(ResultObj.getEigenvectors())
    hi = []
    print("Eigenvalues:")
    for i in range(1, 20):
        value = eigenval[wfnorder[i]] - eigenval[wfnorder[0]]
        print(value)
        hi.append(value)

    with open("./output files/Eigenvalues.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        for word in hi:
            writer.writerow([word])

        # write the data
        # writer.writerow(data)

        # writer.writerow(data2)
        f.close()

    with open("./output files/Eigenvectors.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        for word in hola:
            writer.writerow([word])

        # write the data
        # writer.writerow(data)

        # writer.writerow(data2)
        f.close()

    # z = str(holder.name_of_file) + ".csv"
    # window(z)
    # if os.path.exists("holder.csv"):
    #    os.remove("holder.csv")

    return ResultObj


# r = process_map(main, range(0, 30), max_workers=12)
if __name__ == '__main__':
    main()
