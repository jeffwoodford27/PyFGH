# Interface between GUI and Calculation Scripts

import Vmatrix
import Tmatrix
import Gmatrix
import numpy as np
import scipy
import math
from util.DataObject import OutputData

def eckartTranslation(dataObj):
    equil = dataObj.getEquilMolecule()
    pes = dataObj.getPES()
    N1 = dataObj.getN1()
    N2 = dataObj.getN2()
    N3 = dataObj.getN3()
    m = equil.getM()
    M = 0.0
    for i in range(3):
        M += m[i]

    for i in range(N1):
        for j in range(N2):
            for k in range(N3):
                xcm = ycm = 0.0
                x = pes.getPointByN(i, j, k).getXlist()
                y = pes.getPointByN(i, j, k).getYlist()
                for p in range(3):
                    xcm += m[p]*x[p]
                    ycm += m[p]*y[p]
                xcm = xcm/M
                ycm = ycm/M
                xnew = np.zeros(3,float)
                ynew = np.zeros(3,float)
                for p in range(3):
                    xnew[p] = x[p] - xcm
                    ynew[p] = y[p] - ycm
                pes.getPointByN(i,j,k).setX(xnew)
                pes.getPointByN(i,j,k).setY(ynew)
    return

def eckartRotation(dataObj):
    equil = dataObj.getEquilMolecule()
    pes = dataObj.getPES()
    N1 = dataObj.getN1()
    N2 = dataObj.getN2()
    N3 = dataObj.getN3()
    m = equil.getM()
    xeq = equil.getXlist()
    yeq = equil.getYlist()
    for i in range(N1):
        for j in range(N2):
            for k in range(N3):
                x = pes.getPointByN(i, j, k).getXlist()
                y = pes.getPointByN(i, j, k).getYlist()
                numer = denom = 0.0
                for p in range(3):
                    numer += m[p]*(x[p]*yeq[p] - y[p]*xeq[p])
                    denom += m[p]*(x[p]*xeq[p] + y[p]*yeq[p])
                theta = math.atan2(numer,denom)
                xnew = np.zeros(3,float)
                ynew = np.zeros(3,float)
                for p in range(3):
                    xnew[p] = x[p]*math.cos(theta) - y[p]*math.sin(theta)
                    ynew[p] = x[p]*math.sin(theta) + y[p]*math.cos(theta)
                pes.getPointByN(i,j,k).setX(xnew)
                pes.getPointByN(i,j,k).setY(ynew)
    return

def main():
    pass

def passToCalc(dataObj):
    # print("Got an object.")
    # print(dataObj)

    D = dataObj.getD()
    N = np.zeros(D,dtype=int)
    N[0] = dataObj.getN1()
    N[1] = dataObj.getN2()
    N[2] = dataObj.getN3()

    print("Imposing Eckart conditions")
    eckartTranslation(dataObj)
    eckartRotation(dataObj)

    print("Creating G Matrix")
    GMat = Gmatrix.calcGMatrix(D, N, dataObj.PES, dataObj.EquilMolecule)
    print("Done with G Matrix")
    print("Creating V Matrix")
    VMat = Vmatrix.VMatrixCalc(dataObj)
    print("Done with V Matrix")
    print("Creating T Matrix")
    TMat = Tmatrix.TMatrixCalc(dataObj, GMat)
    print("Done with T Matrix")
    HMat = VMat + TMat

    print("Calculating eigenvalues")
    eigenval, eigenvec = scipy.linalg.eigh(HMat)
    eigenval = eigenval * 219474.6

    ResultObj = OutputData()
    ResultObj.setEigenvalues(eigenval)
    ResultObj.setEigenvectors(eigenvec)

    return ResultObj


# r = process_map(main, range(0, 30), max_workers=12)
if __name__ == '__main__':
    main()
