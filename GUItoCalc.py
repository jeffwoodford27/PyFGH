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


from util import DataObject

def window():
    window = tk.Tk()
    style = Style()
    window.title('Results')
    window.geometry('800x500')
    text = "Results"
    Results = ttk.Label(window, text=DataObject.holdData.Hmat, font=("Times New Roman", 15), background='green',
                        foreground="white")
    Results.pack()
    Results.place(x=350, y=0)
    window.mainloop()


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
    window()

    print(HMat)
    
    
    

if __name__ == '__main__':
    r = process_map(main, range(0, 30), max_workers=12)
    #main()
