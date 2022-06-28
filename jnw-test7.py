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
inp.setequilibrium_file("./testing files/water-equil.csv")
inp.setpotential_energy("./testing files/water-potential.csv")

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
print("equil:" + str(RotateToPA(equil)))

p = 0
pespt = pes.getPointByPt(p)
mol = pyfghutil.Molecule()
mol.setXList(pespt.getXList())
mol.setYList(pespt.getYList())
mol.setZList(pespt.getZList())
mol.setMassList(equil.getMassList())
mol.setAtomicNoList(equil.getAtomicNoList())
mol.setMassNoList(equil.getMassNoList())

print(mol.getXList())
print(mol.getYList())
print(mol.getZList())

TranslateToCOM(mol)

print(mol.getXList())
print(mol.getYList())
print(mol.getZList())

I = RotateToPA(mol)
print(I)

eval,evec = linalg.eig(I)
print(eval)
print(evec)

x = mol.getXList()
y = mol.getYList()
z = mol.getZList()
xr = np.zeros(Nat, dtype=float)
yr = np.zeros(Nat, dtype=float)
zr = np.zeros(Nat, dtype=float)
for j in range(Nat):
    xr[j] = x[j]*evec[0][0]+y[j]*evec[1][0]+z[j]*evec[2][0]
    yr[j] = x[j]*evec[0][1]+y[j]*evec[1][1]+z[j]*evec[2][1]
    zr[j] = x[j]*evec[0][2]+y[j]*evec[1][2]+z[j]*evec[2][2]
mol.setXList(xr)
mol.setYList(yr)
mol.setZList(zr)
Inew = RotateToPA(mol)
