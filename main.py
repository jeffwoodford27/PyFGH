import inputparam
import Tmatrix
import Vmatrix
import scipy
import numpy as np

#Remove the numpy print limits
np.set_printoptions(threshold=sys.maxsize)

D = inputparam.inputValidInt("\nEnter the number of dimensions:\n",1,5)
Vtype = inputparam.inputValidInt("\nEnter Potential Energy Method (0 = model, 1 = file):\n",0,1)
mol = inputparam.Molecule(D,Vtype)

for i in range(0,D):
    #Currently broken
    print ("the number of points in dimension " + str(i+1) + " is " + str(mol.N[i]))

#hmatrix = matfunc.mdhmatrix(mol, D, Vtype)
hmatrix = Tmatrix.TMatrixCalc(mol, D, Vtype) + Vmatrix.VMatrixCalc(mol, D, Vtype)
print(hmatrix)
print("hmatrix done")
hmateigenv = scipy.linalg.eigvals(hmatrix)
heigensort = np.sort(hmateigenv)
print("eigendone")
print(heigensort)
