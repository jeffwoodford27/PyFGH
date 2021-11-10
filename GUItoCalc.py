#Interface between GUI and Calculation Scripts
from tqdm.contrib.concurrent import process_map

import Vmatrix
import Tmatrix
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
    print(dataObj)
    for i in dataObj.holdData.v:
        print("a vtype: "+str(i))
    print("Model data")
    print(dataObj.holdData.model_data)
    VMat = Vmatrix.VMatrixCalc(dataObj)
    print("Done with VMatrix")
    TMat = Tmatrix.TMatrixCalc(dataObj)
    print("Done with TMatrix")
    HMat = VMat + TMat
    pd.DataFrame(HMat).to_csv(DataObject.holdData.name_of_file+".csv")
    DataObject.holdData.Hmat = HMat
    z = DataObject.holdData.name_of_file+".csv"
    window(z)

    print(HMat)
    
    
    

if __name__ == '__main__':
    r = process_map(main, range(0, 30), max_workers=12)
    #main()
