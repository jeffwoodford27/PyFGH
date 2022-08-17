import scipy
from scipy import interpolate
import numpy as np
from PyFGHVersion2.util import pyfghutil

def compute_derivative (x, y):
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
    return yprime

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
                        idx = pyfghutil.PointToIndex(N, pt)
                        x[i] = pes.getPointByIdx(idx).getQ(d)
                        y[i] = pes.getPointByIdx(idx).getCoord(c)
                    dy = compute_derivative(x, y)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        dxdq[c, d, pt] = dy[i]
                        dxdqcalc[c, d, pt] = 1

    Gmatrix = np.zeros([Npts,D,D],dtype=float)
    m = equil.getMassList()

    for p in range(Npts):
        G = np.zeros([D,D],dtype=float)
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
