# Interface between GUI and Calculation Scripts
import gc
import PyFGH.Vmatrix as Vmatrix
import PyFGH.Tmatrix as Tmatrix
import PyFGH.Gmatrix as Gmatrix
import numpy as np
from scipy import linalg
from scipy.sparse import linalg as sparse_linalg
from PyFGH.util.DataObject import OutputData as OutputData
from PyFGH.util import pyfghutil as pyfghutil
from PyFGH import Constants as co
import time


'''
eckartTranslation enforces the translational Eckart condition on the input structure by translating each structure to the center of mass.
Input:
N: a numpy array of length D (no. of dimensions) with the number of grid points in each dimension
equil: a Molecule object with the equilibrium structure
pes: a PotentialEnergySurface object with the potential energy surface

This function modifies the data in the objects
'''



def eckartTranslation(N,equil,pes):
    Nat = equil.getNatom()
    Npts = np.prod(N)
    m = equil.getMassList()
    M = np.sum(m)

    for p in range(Npts):
        idx = pyfghutil.PointToIndex(N, p)
        mol = pes.getPointByIdx(idx)
        xcm = ycm = zcm = 0.0
        x = mol.getXList()
        y = mol.getYList()
        z = mol.getZList()
        for j in range(Nat):
            xcm += m[j]*x[j]
            ycm += m[j]*y[j]
            zcm += m[j]*z[j]
        xcm = xcm/M
        ycm = ycm/M
        zcm = zcm/M
        for j in range(Nat):
            x[j] = x[j] - xcm
            y[j] = y[j] - ycm
            z[j] = z[j] - zcm
        pes.getPointByIdx(idx).setXList(x)
        pes.getPointByIdx(idx).setYList(y)
        pes.getPointByIdx(idx).setZList(z)
    return

'''
eckartRotation enforces the rotational Eckart condition by the method of foo.(look up this reference)
N: a numpy array of length D (no. of dimensions) with the number of grid points in each dimension
equil: a Molecule object with the equilibrium structure
pes: a PotentialEnergySurface object with the potential energy surface

This function modifies the data in the objects
'''


def eckartRotation(N,equil,pes):
    Nat = equil.getNatom()
    Npts = np.prod(N)
    m = equil.getMassList()

    xe = equil.getXList()
    ye = equil.getYList()
    ze = equil.getZList()
    for p in range(Npts):
        idx = pyfghutil.PointToIndex(N, p)
        mol = pes.getPointByIdx(idx)
        x = mol.getXList()
        y = mol.getYList()
        z = mol.getZList()

        A = np.zeros((3,3),dtype=float)
        for i in range(Nat):
            A[0,0] += m[i]*x[i]*xe[i]
            A[0,1] += m[i]*x[i]*ye[i]
            A[0,2] += m[i]*x[i]*ze[i]
            A[1,0] += m[i]*y[i]*xe[i]
            A[1,1] += m[i]*y[i]*ye[i]
            A[1,2] += m[i]*y[i]*ze[i]
            A[2,0] += m[i]*z[i]*xe[i]
            A[2,1] += m[i]*z[i]*ye[i]
            A[2,2] += m[i]*z[i]*ze[i]

        A1 = np.matmul(A.T,A)
        A2 = np.matmul(A,A.T)

        eval1,evec1 = linalg.eig(A1)
        eval2,evec2 = linalg.eig(A2)

        eval1 = np.real(eval1)
        eval2 = np.real(eval2)
        evec1 = evec1.T
        evec2 = evec2.T

        sortidx1 = eval1.argsort()
        sortidx2 = eval2.argsort()
        evec1sort = np.zeros((3,3),dtype=float)
        evec2sort = np.zeros((3,3),dtype=float)
        for i in range(3):
            for j in range(3):
                evec1sort[i,j] = evec1[sortidx1[i],j]
                evec2sort[i,j] = evec2[sortidx2[i],j]

        cp1 = np.cross(evec1sort[0],evec1sort[1])
        if (np.dot(cp1,evec1sort[2]) < 0):
            evec1sort[2] *= -1.0

        cp2 = np.cross(evec2sort[0],evec2sort[1])
        if (np.dot(cp2,evec2sort[2]) < 0):
            evec2sort[2] *= -1.0

        T = np.zeros((3,3),dtype=float)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    T[i,j] += evec1sort[k,i]*evec2sort[k,j]

        xr = np.zeros(Nat, dtype=float)
        yr = np.zeros(Nat, dtype=float)
        zr = np.zeros(Nat, dtype=float)

        for j in range(Nat):
            xr[j] = T[0,0]*x[j] + T[0,1]*y[j] + T[0,2]*z[j]
            yr[j] = T[1,0]*x[j] + T[1,1]*y[j] + T[1,2]*z[j]
            zr[j] = T[2,0]*x[j] + T[2,1]*y[j] + T[2,2]*z[j]

        pes.getPointByIdx(idx).setXList(xr)
        pes.getPointByIdx(idx).setYList(yr)
        pes.getPointByIdx(idx).setZList(zr)
    return

def passToCalc(dataObj):
    D = dataObj.get("D")
    N = dataObj.get("N")
    L = dataObj.get("L")

    equil = dataObj.get("EqMol")
    pes = dataObj.get("PES")

    t0 = t_start = time.perf_counter()
    print("Imposing Eckart conditions")
    eckartTranslation(N, equil, pes)
    eckartRotation(N, equil, pes)
    t1 = time.perf_counter()
    print("Done with Eckart conditions time = {:.2f} s".format(t1-t0))

    print("Creating G Matrix")

    equil = dataObj.get("EqMol")
    pes = dataObj.get("PES")

    t0 = t_start = time.perf_counter()
    G = Gmatrix.calcGMatrix(D, N, pes, equil)
    t1 = time.perf_counter()
    print("Done with G Matrix time = {:.2f} s".format(t1-t0))

    cores = dataObj.get("NCores")

    t0 = time.perf_counter()
    print("Creating V Matrix")
    gc.collect()
    Vmethod = dataObj.get("PEMethod")
    psi4method = dataObj.get("Psi4Method")
    V = Vmatrix.VMatrixCalc(D, N, Vmethod, equil, pes, psi4method, cores)
    t1 = time.perf_counter()
    print("Done with V Matrix time = {:.2f} s".format(t1-t0))

    t0 = time.perf_counter()
    print("Creating T Matrix")
    T = Tmatrix.TMatrixCalc(D, N, L, G, cores)
    t1 = time.perf_counter()
    print("Done with T Matrix time = {:.2f} s".format(t1-t0))

    t0 = time.perf_counter()
    print("Calculating eigenvalues")
    Neigen = dataObj.get("NEigen")
    EigenMethod = dataObj.get("EigenMethod")
    Npts = np.prod(N)

    H = V + T

    if (EigenMethod == co.SMAT):
        NIter = 10*Npts
        try:
            eigenval, eigenvec = sparse_linalg.eigsh(H, k=Neigen, which='SM', tol=1.0e-6, maxiter=NIter)
        except sparse_linalg.ArpackNoConvergence as error_obj:
            eigenval = error_obj.eigenvalues
            eigenvec = error_obj.eigenvectors
            Neigen = np.size(eigenval)
            print("could not find {0} eigenvalues in {1} iterations, found {2} instead.".format(dataObj.get("NEigen"),NIter, Neigen))
            print()
    else:
        H = H.toarray("C")
        eigenval, eigenvec = linalg.eigh(H)

    eigenval = eigenval * 219474.6  # conversion from hartree to cm-1

    t1 = t_end = time.perf_counter()
    print("Done with eigenvalue calculation time = {:.2f} s".format(t1-t0))

    print("Total calculation time = {:.2f} s".format(t_end - t_start))

    ResultObj = OutputData(dataObj.logfile)
    ResultObj.set("D",D)
    ResultObj.set("N",N)
    ResultObj.set("L",L)
    ResultObj.set("NEigen",Neigen)
    ResultObj.set("EVal",eigenval)
    ResultObj.set("EVec",eigenvec)

    return ResultObj


