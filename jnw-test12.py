import numpy as np
from scipy.fft import ifft
import scipy.interpolate
from util import pyfghutil
from util import DataObject
import csv
import time


# A more general way to calculate T matrix.


def compute_derivative (x, y):
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
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
                x = np.zeros(N[d], dtype=float)
                y = np.zeros(N[d], dtype=float)
                for i in range(N[d]):
                    x[i] = q[d][i]
                    y[i] = f[n + i * np.prod(N[d + 1:])]
                dy = compute_derivative(x, y)
                for i in range(N[d]):
                    dfdq[d][n + i * np.prod(N[d + 1:])] = dy[i]
                    dfdqcalc[d][n + i * np.prod(N[d + 1:])] = 1
            else:
                pass
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
                    x = np.zeros(N[d], dtype=float)
                    y = np.zeros(N[d], dtype=float)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        idx = pyfghutil.PointToIndex(D, N, pt)
                        x[i] = pes.getPointByIdx(idx).getq(d + 1)
                        y[i] = pes.getPointByIdx(idx).getCoord(c)
                    dy = compute_derivative(x, y)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        dxdq[c, d, pt] = dy[i]
                        dxdqcalc[c, d, pt] = 1
            else:
                pass

    Gmatrix = np.zeros([Npts,D,D],dtype=float)
    m = equil.getMassList()

    for p in range(Npts):
        G = np.zeros([D,D],float)
        for r in range(D):
            for s in range(r,D):
                for j in range(Nat):
                    for k in range(3):
                        G[r][s] += m[j] * dxdq[3*j+k][r][p] * dxdq[3*j+k][s][p]

        for r in range(D):
            for s in range(r+1,D):
                G[s][r] = G[r][s]

        Ginv = scipy.linalg.inv(G)
        for r in range(D):
            for s in range(D):
                Gmatrix[p][r][s] = Ginv[r][s]
    return Gmatrix

def bmatrixgen(N,L):
    n = (N-1)//2
    B = np.zeros((N,N),dtype=float)
    a = np.zeros(N,dtype=complex)
    for i in range(N):
        a[i] = 2*np.pi*(1j)*(i-n)/L
    aifft = ifft(a,n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)
    for j in range(N):
        for t in range(N):
            B[j,t] = np.real(aifft[(N+j-t)%N])
    return B


def delta(x, y):
    if (x == y):
        return float(1)
    else:
        return float(0)

def Told(d,NValue,b_matrix_insert,GMat, alpha, beta):
    alpha_idx = pyfghutil.PointToIndex(d,NValue,alpha)
    beta_idx = pyfghutil.PointToIndex(d,NValue,beta)

    j = alpha_idx[0]
    t = beta_idx[0]
    k = alpha_idx[1]
    u = beta_idx[1]
    l = alpha_idx[2]
    v = beta_idx[2]

    total = 0.0

    sums = 0.0
    for p in range(NValue[0]):
        pt = pyfghutil.IndexToPoint(d,NValue,[p,k,l])
        sums += b_matrix_insert[2][j,p]*b_matrix_insert[2][p,t]*GMat[pt][0][0]
#        sums += b_matrix_insert[2][j, p] * b_matrix_insert[2][p, t] * GMat[p][k][l][0][0]
#        print(p, alpha_idx[0], beta_idx[0], b_matrix_insert[2][alpha_idx[0],p],b_matrix_insert[2][p,beta_idx[0]],GMat[pt][0][0],sums)
    total += -0.5*sums * delta(k,u) * delta(l,v)

    sums = 0.0
    for p in range(NValue[1]):
        pt = pyfghutil.IndexToPoint(d,NValue,[j,p,l])
        sums += b_matrix_insert[1][k,p]*b_matrix_insert[1][p,u]*GMat[pt][1][1]
#        sums += b_matrix_insert[1][k,p]*b_matrix_insert[1][p,u]*GMat[j][p][l][1][1]
    total += -0.5*sums*delta(j,t) * delta(l,v)

    sums = 0.0
    for p in range(NValue[2]):
        pt = pyfghutil.IndexToPoint(d,NValue,[j,k,p])
        sums += b_matrix_insert[0][l,p]*b_matrix_insert[0][p,v]*GMat[pt][2][2]
#        sums += b_matrix_insert[0][l, p] * b_matrix_insert[0][p, v] * GMat[j][k][p][2][2]
    total += -0.5*sums*delta(j,t)*delta(k,u)

    pt = pyfghutil.IndexToPoint(d, NValue, [t, k, l])
    total += -0.5 * (b_matrix_insert[2][j, t] * b_matrix_insert[1][k, u] * GMat[pt][0][1]) * delta(v, l)
    total += -0.5 * (b_matrix_insert[2][j, t] * b_matrix_insert[0][l, v] * GMat[pt][0][2]) * delta(k, u)

    pt = pyfghutil.IndexToPoint(d, NValue, [j, u, l])
    total += -0.5 * (b_matrix_insert[1][k, u] * b_matrix_insert[2][j, t] * GMat[pt][1][0]) * delta(v, l)
    total += -0.5 * (b_matrix_insert[1][k, u] * b_matrix_insert[0][l, v] * GMat[pt][1][2]) * delta(j, t)

    pt = pyfghutil.IndexToPoint(d, NValue, [j, k, v])
    total += -0.5 * (b_matrix_insert[0][l, v] * b_matrix_insert[2][j, t] * GMat[pt][2][0]) * delta(k, u)
    total += -0.5 * (b_matrix_insert[0][l, v] * b_matrix_insert[1][k, u] * GMat[pt][2][1]) * delta(j, t)

    return(total)

def Tnew(D, N, B, G, alpha, beta):
    total = 0.0

    idx_a = pyfghutil.PointToIndex(D,N,alpha)
    idx_b = pyfghutil.PointToIndex(D,N,beta)

    for r in range(D):
        for s in range(D):
            deltacounter = True
            j = 0
            while (deltacounter and (j < D)):
                if ((r != j) and (s != j)):
                    if (idx_a[j] != idx_b[j]):
                        deltacounter = False
                j = j + 1

            if (deltacounter):
                idx = np.copy(idx_a)
                if (r == s):
                    val = 0.0
                    for p in range(N[r]):
                        idx[r] = p
                        pt = pyfghutil.IndexToPoint(D,N,idx)
                        val += B[r][idx_a[r],p]*B[r][p,idx_b[r]]*G[pt][r][r]
#                       if d == 0:
#                           print(p, alpha_idx[d], beta_idx[d], B[d][alpha_idx[d],p],B[d][p,beta_idx[d]],G[pt][d][d],sums)
                else:
                    idx[s] = idx_b[s]
                    pt = pyfghutil.IndexToPoint(D,N,idx)
                    val = B[r][idx_a[r],idx_b[r]]*B[s][idx_a[s],idx_b[s]]*G[pt][r][s]

                total += val

    return(-0.5*total)

D = 3
inp = DataObject.InputData()
inp.setD(D)
N = np.zeros(D,dtype=int)
N[0] = 11
N[1] = 11
N[2] = 11
inp.setNlist(N)
L = np.zeros(D,dtype=float)
L[0] = 1.1
L[1] = 1.1
L[2] = 1.65
inp.setLlist(L)
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

b_matrix = []
for x in reversed(range(3)):
    b_matrix.append(bmatrixgen(N[x], L[x]))



#G = calcGMatrix(D, N, pes, equil)

D = 4
N = np.zeros(D,dtype=int)
N[0] = 7
N[1] = 7
N[2] = 7
N[3] = 7
L = np.zeros(D,dtype=float)
L[0] = L[1] = L[2] = L[3] = 1
Npts = np.prod(N)
B = []
for x in range(D):
    B.append(bmatrixgen(N[x],L[x]))
G = np.ones([Npts,D,D],dtype=float)

'''
t0 = time.perf_counter()
for alpha in range(Npts):
    for beta in range(Npts):
        total1 = Told(D,N,b_matrix,G,alpha,beta)
        if (alpha == 2 and beta == 3):
            print(total1)
t1 = time.perf_counter()
print(t1-t0)
'''

t0 = time.perf_counter()
for alpha in range(Npts):
    for beta in range(Npts):
        total2 = Tnew(D,N,B,G,alpha,beta)
        if (alpha == 2 and beta == 3):
            print(total2)
t1 = time.perf_counter()
print(t1-t0)
