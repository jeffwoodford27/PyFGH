import scipy
from scipy import interpolate
from scipy import linalg
import numpy as np
from util import pyfghutil

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
#                    print ("for point " + str(n) + " in dimension " + str(d))
                    x = np.zeros(N[d], dtype=float)
                    y = np.zeros(N[d], dtype=float)
                    for i in range(N[d]):
                        pt = n + i * np.prod(N[d + 1:])
                        idx = pyfghutil.PointToIndex(N, pt)
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