import numpy as np
from util import pyfghutil
from util import DataObject
import csv

D = 3
inp = DataObject.InputData(D)
inp.setN1(11)
inp.setN2(11)
inp.setN3(11)
inp.setL1(1.1)
inp.setL2(1.1)
inp.setL3(1.65)
inp.setequilibrium_file("./testingfiles/water-equil.csv")
inp.setpotential_energy("./testingfiles/water-potential.csv")

Nat = 3
equil = pyfghutil.Molecule(Nat)
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

equil.setx(x)
equil.sety(y)
equil.setz(z)
equil.setZ(Z)
equil.setA(A)
equil.setM(m)

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
        pespt.setQ(q)

        x = np.zeros(Nat, dtype=float)
        y = np.zeros(Nat, dtype=float)
        z = np.zeros(Nat, dtype=float)

        x[0] = float(row[3])
        y[0] = float(row[4])
        x[1] = float(row[5])
        y[1] = float(row[6])
        x[2] = float(row[7])
        y[2] = float(row[8])
        pespt.setX(x)
        pespt.setY(y)
        pespt.setZ(z)

        pespt.setEnergy(float(row[9]))

        pes.appendPESpt(pespt)
        n = n + 1

f = np.zeros((3*Nat, D, Npts), dtype=float)
dxdqcalc = np.zeros((3*Nat, D, Npts), dtype=int)

for n in range(Npts):
    for d in range(D-1, -1, -1):
        for c in range(3*Nat):
            if (dxdqcalc[c,d,n] == 0):
                x = np.zeros(N[d],dtype=float)
                y = np.zeros(N[d],dtype=float)
                for i in range(N[d]):
                    pt = n + i * np.prod(N[d + 1:])
                    idx = pyfghutil.PointToIndex(D, N, pt)
                    x[i] = pes.getPointByIdx(idx).getq(d + 1)
                    y[i] = pes.getPointByIdx(idx).getCoord(c)
                    f[c,d,pt] = y[i]
                    dxdqcalc[c,d,pt] = 1
                idx = pyfghutil.PointToIndex(D, N, n)
                for i in range(D):
                    if (i != d):
                        print("q"+str(i+1)+"="+str(pes.getPointByIdx(idx).getq(i+1)))
                for i in range(D):
                    if (i == d):
                        print("q"+str(i+1)+": "+str(x))
                        print("x"+str(c+1)+": "+str(y))

print(f[0,0])