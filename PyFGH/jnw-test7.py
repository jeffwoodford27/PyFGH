import numpy as np
from util import pyfghutil
from util import DataObject
import csv
from scipy import linalg

def TranslateToCOM(mol):
    Nat = mol.getNatom()
    m = mol.getMassList()
    x = mol.getXList()
    y = mol.getYList()
    z = mol.getZList()

    M = 0
    for j in range(Nat):
        M += m[j]

    xcm = ycm = zcm = 0
    for j in range(Nat):
        xcm += m[j] * x[j]
        ycm += m[j] * y[j]
        zcm += m[j] * z[j]
    xcm = xcm / M
    ycm = ycm / M
    zcm = zcm / M
    xnew = np.zeros(Nat, dtype=float)
    ynew = np.zeros(Nat, dtype=float)
    znew = np.zeros(Nat, dtype=float)

    for j in range(Nat):
        xnew[j] = x[j] - xcm
        ynew[j] = y[j] - ycm
        znew[j] = z[j] - zcm

    mol.setXList(xnew)
    mol.setYList(ynew)
    mol.setZList(znew)
    return

def RotateToPA(mol):
    Nat = mol.getNatom()
    m = mol.getMassList()
    x = mol.getXList()
    y = mol.getYList()
    z = mol.getZList()

    I = np.zeros((3,3),dtype=float)
    for j in range(Nat):
        I[0,0] += m[j]*(y[j]*y[j]+z[j]*z[j])
        I[1,1] += m[j]*(x[j]*x[j]+z[j]*z[j])
        I[2,2] += m[j]*(x[j]*x[j]+y[j]*y[j])
        I[0,1] += -m[j]*(x[j]*y[j])
        I[0,2] += -m[j]*(x[j]*z[j])
        I[1,2] += -m[j]*(y[j]*z[j])
    I[1,0] = I[0,1]
    I[2,0] = I[0,2]
    I[2,1] = I[1,2]
    return I

def eckartRotationCheck(equil, mol):
    Nat = equil.getNatom()
    m = equil.getMassList()
    xe = equil.getXList()
    ye = equil.getYList()
    ze = equil.getZList()
    x = mol.getXList()
    y = mol.getYList()
    z = mol.getZList()

    xd = np.zeros(Nat,dtype=float)
    yd = np.zeros(Nat,dtype=float)
    zd = np.zeros(Nat,dtype=float)

    for j in range(Nat):
        xd[j] = x[j] - xe[j]
        yd[j] = y[j] - ye[j]
        zd[j] = z[j] - ze[j]

    eckartcheck = np.zeros(3,dtype=float)
    for j in range(Nat):
        eckartcheck[0] += m[j]*(yd[j]*ze[j] - zd[j]*ye[j])
        eckartcheck[1] += m[j]*(xd[j]*ze[j] - zd[j]*xe[j])
        eckartcheck[2] += m[j]*(xd[j]*ye[j] - yd[j]*xe[j])

    return eckartcheck


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

D = 3
inp = DataObject.InputData()
inp.setN1(11)
inp.setN2(11)
inp.setN3(11)
inp.setL1(1.1)
inp.setL2(1.1)
inp.setL3(1.65)
inp.setequilibrium_file("./testingfiles/water-equil.csv")
inp.setpotential_energy("./testingfiles/water-potential.csv")

Nat = 3
equil = pyfghutil.Molecule()
with open(inp.equilibrium_file, newline='') as csvfile:
    eqfile = csv.reader(csvfile)
    A = np.empty(Nat, dtype=int)
    Z = np.empty(Nat, dtype=int)
    x = np.empty(Nat, dtype=float)
    y = np.empty(Nat, dtype=float)
    z = np.empty(Nat, dtype=float)
    m = np.empty(Nat, dtype=float)
    n = 0
    for row in eqfile:
        for key, value in pyfghutil.AtomicSymbolLookup.items():
            if (value == row[0]):
                Z[n] = key
                break
        A[n] = int(row[1])
        x[n] = float(row[2])
        y[n] = float(row[3])
        z[n] = float(row[4])
        nucl = row[0] + "-" + row[1]
        m[n] = pyfghutil.MassLookup.get(nucl) * 1822.89
        n = n + 1

equil.setXList(x)
equil.setYList(y)
equil.setZList(z)
equil.setAtomicNoList(Z)
equil.setMassNoList(A)
equil.setMassList(m)

N = np.zeros(D,dtype=int)
N[0] = inp.getN1()
N[1] = inp.getN2()
N[2] = inp.getN3()
Npts = np.prod(N)

pes = pyfghutil.PotentialEnergySurface()
pes.setN(N)
with open(inp.potential_energy_file, newline='') as csvfile:
    pesfile = csv.reader(csvfile)

    n = 0
    for row in pesfile:
        pespt = pyfghutil.PESpoint()
        pespt.setN(n)

        q = np.zeros(D, dtype=float)
        q[0] = float(row[0])
        q[1] = float(row[1])
        q[2] = float(row[2])
        pespt.setQList(q)

        x = np.zeros(Nat, dtype=float)
        y = np.zeros(Nat, dtype=float)
        z = np.zeros(Nat, dtype=float)

        x[0] = float(row[3])
        y[0] = float(row[4])
        x[1] = float(row[5])
        y[1] = float(row[6])
        x[2] = float(row[7])
        y[2] = float(row[8])
        pespt.setXList(x)
        pespt.setYList(y)
        pespt.setZList(z)

        pespt.setEnergy(float(row[9]))

        pes.appendPESpt(pespt)
        n = n + 1

TranslateToCOM(equil)

xe = equil.getXList()
ye = equil.getYList()
ze = equil.getZList()

print(xe)
print(ye)
print(ze)

Npt = 10
newmol = []
for p in range(Npt):
    print("p")
    print(p)
    pespt = pes.getPointByPt(p)
    mol = pyfghutil.Molecule()
    mol.setXList(pespt.getXList())
    mol.setYList(pespt.getYList())
    mol.setZList(pespt.getZList())
    mol.setMassList(equil.getMassList())
    mol.setAtomicNoList(equil.getAtomicNoList())
    mol.setMassNoList(equil.getMassNoList())

    TranslateToCOM(mol)

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
    eval1sort = np.zeros(3,dtype=float)
    eval2sort = np.zeros(3,dtype=float)
    evec1sort = np.zeros((3,3),dtype=float)
    evec2sort = np.zeros((3,3),dtype=float)
    for i in range(3):
        eval1sort[i] = eval1[sortidx1[i]]
        eval2sort[i] = eval2[sortidx2[i]]
        for j in range(3):
            evec1sort[i,j] = evec1[sortidx1[i],j]
            evec2sort[i,j] = evec2[sortidx2[i],j]

#print("eval1sort")
#print(eval1sort)
#print("evec1sort")
#print(evec1sort)
#print("eval2sort")
#print(eval2sort)
#print("evec2sort")
#print(evec2sort)


    for i in range(3):
        f = np.zeros(3,dtype=float)
        ev = np.zeros(3,dtype=float)
        for j in range(3):
            ev[j] = evec1[i,j]
        f[0] = (A1[0,0]-eval1[i])*ev[0] + A1[0,1]*ev[1] + A1[0,2]*ev[2]
        f[1] = A1[1,0]*ev[0] + (A1[1,1]-eval1[i])*ev[1] + A1[1,2]*ev[2]
        f[2] = A1[2,0]*ev[0] + A1[2,1]*ev[1] + (A1[2,2]-eval1[i])*ev[2]
#        print(str(i+1))
#        print(eval1[i])
#        print(ev)
#        print(f)

#    print("dot products")
#    for i in range(3):
#        print(np.dot(evec1sort[i],evec2sort[i]))

 #   print("cross products")
 #   print(np.cross(evec1sort[0], evec1sort[1]))
 #   print(evec1sort[2])
    cp1 = np.cross(evec1sort[0],evec1sort[1])
 #   print(np.dot(cp1,evec1sort[2]))

#    print(np.cross(evec2sort[0], evec2sort[1]))
#    print(evec2sort[2])
    cp2 = np.cross(evec2sort[0],evec2sort[1])
#    print(np.dot(cp2,evec2sort[2]))

    if (np.dot(cp1,evec1sort[2]) < 0):
        evec1sort[2] *= -1.0
        print("changed sign for p = "+str(p))

    if (np.dot(cp2,evec2sort[2]) < 0):
        evec2sort[2] *= -1.0
        print("changed sign for p = "+str(p))

    T = np.zeros((3,3),dtype=float)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                T[i,j] += evec1sort[k,i]*evec2sort[k,j]

#    print("T")
#    print(T)
#    print(linalg.det(T))

    xr = np.zeros(Nat, dtype=float)
    yr = np.zeros(Nat, dtype=float)
    zr = np.zeros(Nat, dtype=float)

    for j in range(Nat):
        xr[j] = T[0,0]*x[j] + T[0,1]*y[j] + T[0,2]*z[j]
        yr[j] = T[1,0]*x[j] + T[1,1]*y[j] + T[1,2]*z[j]
        zr[j] = T[2,0]*x[j] + T[2,1]*y[j] + T[2,2]*z[j]

    mol.setXList(xr)
    mol.setYList(yr)
    mol.setZList(zr)

#    print("eckart test")
#    print(eckartRotationCheck(equil,mol))

#    print("rotated molecule")
#    print(mol.getXList())
#    print(mol.getYList())
#    print(mol.getZList())

    newmol.append(mol)

    print("\n")

xe = equil.getXList()
ye = equil.getYList()
ze = equil.getZList()
print(xe)
print(ye)
print(ze)

for i in range(Npt):
    print(newmol[i].getXList())
    print(newmol[i].getYList())
    print(newmol[i].getZList())