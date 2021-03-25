import inputstuff as inputstuff
import matrixfunctions as matfunc
import scipy
import numpy as np



D = inputstuff.inputValidInt("\nEnter the number of dimensions:\n",1,5)
Vtype = inputstuff.inputValidInt("\nEnter Potential Energy Method (0 = model, 1 = file):\n",0,1)
mol = inputstuff.Molecule(D,Vtype)

for i in range(0,D):
    print ("the number of points in dimension " + str(i+1) + " is " + str(mol.N[i]))

#hmatrix = matfunc.mdhmatrix(mol, D, Vtype)
hmatrix = matfunc.TMatrixCalc(mol, D, Vtype) + matfunc.VMatrixCalc(mol, D, Vtype)
print(hmatrix)
hmateigenv = scipy.linalg.eigvals(hmatrix)
heigensort = np.sort(hmateigenv)
print(heigensort)
