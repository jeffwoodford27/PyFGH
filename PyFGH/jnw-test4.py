import numpy as np
import scipy
from scipy import interpolate
from util import pyfghutil
from util import DataObject
import csv
import time

# This testing file has an improved method for calculating the G matrix.
# The PointToIdxs feature should be harmonized with that in test1.

def compute_derivative (x, y):
#    print(x,y)
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
#    print(yprime)
    return yprime

def calcderiv(D, N, q, f):
    Npts = np.prod(N)
    dfdq = []
    dfdqcalc = []
    for i in range(D):
        dfdq.append(np.zeros(Npts,dtype=float))
        dfdqcalc.append(np.zeros(Npts, dtype=int))

    for n in range(Npts):
        for d in range(D - 1, -1, -1):
            if (dfdqcalc[d][n] == 0):
                #            print ("for point " + str(n) + " in dimension " + str(d))
                x = np.zeros(N[d], dtype=float)
                y = np.zeros(N[d], dtype=float)
                for i in range(N[d]):
                    x[i] = q[d][i]
                    y[i] = f[n + i * np.prod(N[d + 1:])]
            #            print(x,y)
                dy = compute_derivative(x, y)
                for i in range(N[d]):
                    dfdq[d][n + i * np.prod(N[d + 1:])] = dy[i]
                    dfdqcalc[d][n + i * np.prod(N[d + 1:])] = 1
        #                print ("   setting derivative using point " + str(n+i*np.prod(N[d+1:])))
            else:
                pass
#            print("skip point " + str(n) + " for dimension " + str(d))
    return dfdq

def calcGMatrix(D, N, pes, equil):
    Nat = equil.getNatom()
    Npts = np.prod(N)

    dxdq = np.zeros((3*Nat,D,Npts),dtype=float)
    dxdqcalc = np.zeros((3 * Nat, D, Npts), dtype=int)

    for n in range(Npts):
        for d in range(D-1, -1, -1):
            for c in range(3*Nat):
                if (dxdqcalc[c,d,n] == 0):
#                    print ("for point " + str(n) + " in dimension " + str(d))
                    x = np.zeros(N[d], dtype=float)
                    y = np.zeros(N[d], dtype=float)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        idx = pyfghutil.PointToIndex(D, N, pt)
                        x[i] = pes.getPointByIdx(idx).getq(d + 1)
                        y[i] = pes.getPointByIdx(idx).getCoord(c)
#                    print(x, y)
                    dy = compute_derivative(x, y)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        dxdq[c, d, pt] = dy[i]
                        dxdqcalc[c, d, pt] = 1

#                    if (d == 2):
#                        idx = pyfghutil.PointToIndex(D, N, n)
#                        for i in range(D):
#                            if (i != d):
#                                print("q" + str(i + 1) + "=" + str(pes.getPointByIdx(idx).getq(i + 1)))
#                        for i in range(D):
#                            if (i == d):
#                                print("q" + str(i + 1) + ": " + str(x))
#                                print("x" + str(c + 1) + ": " + str(y))
            else:
                pass
    #            print("skip point " + str(n) + " for dimension " + str(d))

    Gmatrix = np.zeros([Npts,3,3],dtype=float)
    m = equil.getMassList()

    for p in range(Npts):
        G = np.zeros([3,3],float)
        for r in range(3):
            for s in range(r,3):
                for j in range(Nat):
                    for k in range(3):
                        G[r][s] += m[j] * dxdq[3*j+k][r][p] * dxdq[3*j+k][s][p]

        for r in range(3):
            for s in range(r+1,3):
                G[s][r] = G[r][s]

        Ginv = scipy.linalg.inv(G)
        for r in range(3):
            for s in range(3):
                Gmatrix[p][r][s] = Ginv[r][s]
    return Gmatrix


'''        
        G[0][0] = m1 * (dxdq[0][0][p] * dxdq[0][0][p] + dxdq[1][0][p] * dxdq[1][0][p]) \
                + m2 * (dxdq[3][0][p] * dxdq[3][0][p] + dxdq[4][0][p] * dxdq[4][0][p]) \
                + m3 * (dxdq[6][0][p] * dxdq[6][0][p] + dxdq[7][0][p] * dxdq[7][0][p])
        G[0][1] = m1 * (dxdq[0][0][p] * dxdq[0][1][p] + dxdq[1][0][p] * dxdq[1][1][p]) \
                + m2 * (dxdq[3][0][p] * dxdq[3][1][p] + dxdq[4][0][p] * dxdq[4][1][p]) \
                + m3 * (dxdq[6][0][p] * dxdq[6][1][p] + dxdq[7][0][p] * dxdq[7][1][p])
        G[0][2] = m1 * (dxdq[0][0][p] * dxdq[0][2][p] + dxdq[1][0][p] * dxdq[1][2][p]) \
                + m2 * (dxdq[3][0][p] * dxdq[3][2][p] + dxdq[4][0][p] * dxdq[4][2][p]) \
                + m3 * (dxdq[6][0][p] * dxdq[6][2][p] + dxdq[7][0][p] * dxdq[7][2][p])
        G[1][1] = m1 * (dxdq[0][1][p] * dxdq[0][1][p] + dxdq[1][1][p] * dxdq[1][1][p]) \
                + m2 * (dxdq[3][1][p] * dxdq[3][1][p] + dxdq[4][1][p] * dxdq[4][1][p]) \
                + m3 * (dxdq[6][1][p] * dxdq[6][1][p] + dxdq[7][1][p] * dxdq[7][1][p])
        G[1][2] = m1 * (dxdq[0][1][p] * dxdq[0][2][p] + dxdq[1][1][p] * dxdq[1][2][p]) \
                + m2 * (dxdq[3][1][p] * dxdq[3][2][p] + dxdq[4][1][p] * dxdq[4][2][p]) \
                + m3 * (dxdq[6][1][p] * dxdq[6][2][p] + dxdq[7][1][p] * dxdq[7][2][p])
        G[2][2] = m1 * (dxdq[0][2][p] * dxdq[0][2][p] + dxdq[1][2][p] * dxdq[1][2][p]) \
                + m2 * (dxdq[3][2][p] * dxdq[3][2][p] + dxdq[4][2][p] * dxdq[4][2][p]) \
                + m3 * (dxdq[6][2][p] * dxdq[6][2][p] + dxdq[7][2][p] * dxdq[7][2][p])
        G[1][0] = G[0][1]
        G[2][0] = G[0][2]
        G[2][1] = G[1][2]
        Ginv = scipy.linalg.inv(G)
        idx = pyfghutil.PointToIndex(D,N,p)
        for r in range(3):
            for s in range(3):
                Gmatrix[idx[0]][idx[1]][idx[2]][r][s] = Ginv[r][s]

'''


def calcGMatrix_Old(D, N, pes, equil):
    dx1dq1 = np.zeros([N[0],N[1],N[2]])
    dy1dq1 = np.zeros([N[0],N[1],N[2]])
    dx2dq1 = np.zeros([N[0],N[1],N[2]])
    dy2dq1 = np.zeros([N[0],N[1],N[2]])
    dx3dq1 = np.zeros([N[0],N[1],N[2]])
    dy3dq1 = np.zeros([N[0],N[1],N[2]])
    dx1dq2 = np.zeros([N[0],N[1],N[2]])
    dy1dq2 = np.zeros([N[0],N[1],N[2]])
    dx2dq2 = np.zeros([N[0],N[1],N[2]])
    dy2dq2 = np.zeros([N[0],N[1],N[2]])
    dx3dq2 = np.zeros([N[0],N[1],N[2]])
    dy3dq2 = np.zeros([N[0],N[1],N[2]])
    dx1dq3 = np.zeros([N[0],N[1],N[2]])
    dy1dq3 = np.zeros([N[0],N[1],N[2]])
    dx2dq3 = np.zeros([N[0],N[1],N[2]])
    dy2dq3 = np.zeros([N[0],N[1],N[2]])
    dx3dq3 = np.zeros([N[0],N[1],N[2]])
    dy3dq3 = np.zeros([N[0],N[1],N[2]])

    for i in range(N[0]):
        for j in range(N[1]):
            q3 = np.zeros(N[2])
            x1 = np.zeros(N[2])
            y1 = np.zeros(N[2])
            x2 = np.zeros(N[2])
            y2 = np.zeros(N[2])
            x3 = np.zeros(N[2])
            y3 = np.zeros(N[2])
            for k in range(N[2]):
                q3[k] = pes.getPointByN(i,j,k).getq3()
                x1[k] = pes.getPointByN(i,j,k).x[0]
                y1[k] = pes.getPointByN(i,j,k).y[0]
                x2[k] = pes.getPointByN(i,j,k).x[1]
                y2[k] = pes.getPointByN(i,j,k).y[1]
                x3[k] = pes.getPointByN(i,j,k).x[2]
                y3[k] = pes.getPointByN(i,j,k).y[2]
            x1p = compute_derivative(q3,x1)
            y1p = compute_derivative(q3,y1)
            x2p = compute_derivative(q3,x2)
            y2p = compute_derivative(q3,y2)
            x3p = compute_derivative(q3,x3)
            y3p = compute_derivative(q3,y3)
            for k in range(N[2]):
                dx1dq3[i][j][k] = x1p[k]
                dy1dq3[i][j][k] = y1p[k]
                dx2dq3[i][j][k] = x2p[k]
                dy2dq3[i][j][k] = y2p[k]
                dx3dq3[i][j][k] = x3p[k]
                dy3dq3[i][j][k] = y3p[k]

    print("old")
    print(q3)
    print(x1)

    for i in range(N[0]):
        for k in range(N[2]):
            q2 = np.zeros(N[1])
            x1 = np.zeros(N[1])
            y1 = np.zeros(N[1])
            x2 = np.zeros(N[1])
            y2 = np.zeros(N[1])
            x3 = np.zeros(N[1])
            y3 = np.zeros(N[1])
            for j in range(N[1]):
                q2[j] = pes.getPointByN(i,j,k).getq2()
                x1[j] = pes.getPointByN(i,j,k).x[0]
                y1[j] = pes.getPointByN(i,j,k).y[0]
                x2[j] = pes.getPointByN(i,j,k).x[1]
                y2[j] = pes.getPointByN(i,j,k).y[1]
                x3[j] = pes.getPointByN(i,j,k).x[2]
                y3[j] = pes.getPointByN(i,j,k).y[2]
            x1p = compute_derivative(q2,x1)
            y1p = compute_derivative(q2,y1)
            x2p = compute_derivative(q2,x2)
            y2p = compute_derivative(q2,y2)
            x3p = compute_derivative(q2,x3)
            y3p = compute_derivative(q2,y3)
            for j in range(N[1]):
                dx1dq2[i][j][k] = x1p[j]
                dy1dq2[i][j][k] = y1p[j]
                dx2dq2[i][j][k] = x2p[j]
                dy2dq2[i][j][k] = y2p[j]
                dx3dq2[i][j][k] = x3p[j]
                dy3dq2[i][j][k] = y3p[j]

    for j in range(N[1]):
        for k in range(N[2]):
            q1 = np.zeros(N[0])
            x1 = np.zeros(N[0])
            y1 = np.zeros(N[0])
            x2 = np.zeros(N[0])
            y2 = np.zeros(N[0])
            x3 = np.zeros(N[0])
            y3 = np.zeros(N[0])
            for i in range(N[0]):
                q1[i] = pes.getPointByN(i,j,k).getq1()
                x1[i] = pes.getPointByN(i,j,k).x[0]
                y1[i] = pes.getPointByN(i,j,k).y[0]
                x2[i] = pes.getPointByN(i,j,k).x[1]
                y2[i] = pes.getPointByN(i,j,k).y[1]
                x3[i] = pes.getPointByN(i,j,k).x[2]
                y3[i] = pes.getPointByN(i,j,k).y[2]
            x1p = compute_derivative(q1,x1)
            y1p = compute_derivative(q1,y1)
            x2p = compute_derivative(q1,x2)
            y2p = compute_derivative(q1,y2)
            x3p = compute_derivative(q1,x3)
            y3p = compute_derivative(q1,y3)
            for i in range(N[0]):
                dx1dq1[i][j][k] = x1p[i]
                dy1dq1[i][j][k] = y1p[i]
                dx2dq1[i][j][k] = x2p[i]
                dy2dq1[i][j][k] = y2p[i]
                dx3dq1[i][j][k] = x3p[i]
                dy3dq1[i][j][k] = y3p[i]

    m1 = equil.m[0]
    m2 = equil.m[1]
    m3 = equil.m[2]

    Gmatrix = np.zeros([N[0],N[1],N[2],3,3],float)

    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                G = np.zeros([3,3],float)
                G[0][0] = m1 * (dx1dq1[i][j][k] * dx1dq1[i][j][k] + dy1dq1[i][j][k] * dy1dq1[i][j][k]) \
                      + m2 * (dx2dq1[i][j][k] * dx2dq1[i][j][k] + dy2dq1[i][j][k] * dy2dq1[i][j][k]) \
                      + m3 * (dx3dq1[i][j][k] * dx3dq1[i][j][k] + dy3dq1[i][j][k] * dy3dq1[i][j][k])
                G[0][1] = m1 * (dx1dq1[i][j][k] * dx1dq2[i][j][k] + dy1dq1[i][j][k] * dy1dq2[i][j][k]) \
                      + m2 * (dx2dq1[i][j][k] * dx2dq2[i][j][k] + dy2dq1[i][j][k] * dy2dq2[i][j][k]) \
                      + m3 * (dx3dq1[i][j][k] * dx3dq2[i][j][k] + dy3dq1[i][j][k] * dy3dq2[i][j][k])
                G[0][2] = m1 * (dx1dq1[i][j][k] * dx1dq3[i][j][k] + dy1dq1[i][j][k] * dy1dq3[i][j][k]) \
                      + m2 * (dx2dq1[i][j][k] * dx2dq3[i][j][k] + dy2dq1[i][j][k] * dy2dq3[i][j][k]) \
                      + m3 * (dx3dq1[i][j][k] * dx3dq3[i][j][k] + dy3dq1[i][j][k] * dy3dq3[i][j][k])
                G[1][1] = m1 * (dx1dq2[i][j][k] * dx1dq2[i][j][k] + dy1dq2[i][j][k] * dy1dq2[i][j][k]) \
                      + m2 * (dx2dq2[i][j][k] * dx2dq2[i][j][k] + dy2dq2[i][j][k] * dy2dq2[i][j][k]) \
                      + m3 * (dx3dq2[i][j][k] * dx3dq2[i][j][k] + dy3dq2[i][j][k] * dy3dq2[i][j][k])
                G[1][2] = m1 * (dx1dq2[i][j][k] * dx1dq3[i][j][k] + dy1dq2[i][j][k] * dy1dq3[i][j][k]) \
                      + m2 * (dx2dq2[i][j][k] * dx2dq3[i][j][k] + dy2dq2[i][j][k] * dy2dq3[i][j][k]) \
                      + m3 * (dx3dq2[i][j][k] * dx3dq3[i][j][k] + dy3dq2[i][j][k] * dy3dq3[i][j][k])
                G[2][2] = m1 * (dx1dq3[i][j][k] * dx1dq3[i][j][k] + dy1dq3[i][j][k] * dy1dq3[i][j][k]) \
                      + m2 * (dx2dq3[i][j][k] * dx2dq3[i][j][k] + dy2dq3[i][j][k] * dy2dq3[i][j][k]) \
                      + m3 * (dx3dq3[i][j][k] * dx3dq3[i][j][k] + dy3dq3[i][j][k] * dy3dq3[i][j][k])
                G[1][0] = G[0][1]
                G[2][0] = G[0][2]
                G[2][1] = G[1][2]
                Ginv = scipy.linalg.inv(G)
                for r in range(3):
                    for s in range(3):
                        Gmatrix[i][j][k][r][s] = Ginv[r][s]
    return Gmatrix

D = 3
inp = DataObject.InputData()
inp.setD(D)
N = np.zeros(D,dtype=int)
N[0] = 11
N[1] = 11
N[2] = 11
inp.setNlist(N)
inp.setLlist([1.1,1.1,1.65])
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

N = inp.getNlist()

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

Npts = np.prod(N)



#q = []
#for d in range(D):
#    q.append(np.zeros(N[d],dtype=float))

#x = []
#for d in range(D):
#    x.append(np.zeros(N[d],dtype=float))

'''
dfdq = []
dfdqcalc = []
for d in range(D):
    dfdq.append(np.zeros(Npts,dtype=float))
    dfdqcalc.append(np.zeros(Npts, dtype=int))

for n in range(Npts):
    for d in range(D - 1, -1, -1):
        if (dfdqcalc[d][n] == 0):
#            print("for point " + str(n) + " in dimension " + str(d))
            x = np.zeros(N[d], dtype=float)
            y = np.zeros(N[d], dtype=float)
            for i in range(N[d]):
                idx = pyfghutil.PointToIndex(D, N, n + i * np.prod(N[d + 1:]))
                x[i] = pes.getPointByIdx(idx).getq(d+1)
                y[i] = pes.getPointByIdx(idx).getX(1)

            for i in range(N[d]):
                dfdqcalc[d][n + i * np.prod(N[d + 1:])] = 1
'''
Gold = calcGMatrix_Old(D, N, pes, equil)
t0 = time.perf_counter()
G = calcGMatrix(D, N, pes, equil)
t1 = time.perf_counter()
print(t1-t0)

chisq = 0
for p in range(Npts):
    idx = pyfghutil.PointToIndex(D, N, p)
    for r in range(3):
        for s in range(3):
            chisq = chisq + (G[p][r][s]-Gold[idx[0]][idx[1]][idx[2]][r][s])*(G[p][r][s]-Gold[idx[0]][idx[1]][idx[2]][r][s])

chisq = np.sqrt(chisq)
print(chisq)


#dfdq = compute_derivative(q,x)


#dfdq = calcderiv(D, N, q, f)






#dq = 0.1
#q = []
#for i in range(D):
#    q.append(np.zeros(N[i],dtype=float))
#
#for i in range(D):
#    for j in range(N[i]):
#        q[i][j] = (j-N[i]//2)*dq

#Npts = np.prod(N)
#f = np.zeros(Npts,dtype=float)
#for i in range(Npts):
#    idx = pyfghutil.PointToIndex(D,N,i)
#    f[i] = np.power(q[0][idx[0]],2)*np.power(q[1][idx[1]],3)*q[2][idx[2]]

#dfdq = calcderiv(D, N, q, f)

#dfdq_analytical = []
#for i in range(D):
#    dfdq_analytical.append(np.zeros(Npts,dtype=float))

#for n in range(Npts):
#    idx = pyfghutil.PointToIndex(D,N,n)
#    q1 = q[0][idx[0]]
#    q2 = q[1][idx[1]]
#    q3 = q[2][idx[2]]
#    dfdq_analytical[0][n] = 2*q1*q2*q2*q2*q3
#    dfdq_analytical[1][n] = 3*q1*q1*q2*q2*q3
#    dfdq_analytical[2][n] = q1*q1*q2*q2*q2

#chisq = 0
#for n in range(Npts):
#    idx = pyfghutil.PointToIndex(D,N,n)
#    print(n,q[0][idx[0]],dfdq[0][n],dfdq_analytical[0][n])
#    print(n,q[1][idx[1]],dfdq[1][n],dfdq_analytical[1][n])
#    print(n, q[2][idx[2]], dfdq[2][n], dfdq_analytical[2][n])
#    print("\n")
#    chisq = chisq + (dfdq[0][n] - dfdq_analytical[0][n]) * (dfdq[0][n] - dfdq_analytical[0][n])
#    chisq = chisq + (dfdq[1][n] - dfdq_analytical[1][n]) * (dfdq[1][n] - dfdq_analytical[1][n])
#    chisq = chisq + (dfdq[2][n] - dfdq_analytical[2][n]) * (dfdq[2][n] - dfdq_analytical[2][n])

#chisq = np.sqrt(chisq)
#print(chisq)
