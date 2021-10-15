#Interface between GUI and Calculation Scripts
import Vmatrix
import Tmatrix
import numpy as np
import scipy
import pandas as pd

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
    filename = str(input("File name?\n"))
    pd.DataFrame(HMat).to_csv(filename+".csv")
    
    
    

if __name__ == '__main__':
    main()
