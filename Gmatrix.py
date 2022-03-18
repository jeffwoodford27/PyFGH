import scipy
from scipy import interpolate
import math
from scipy import linalg
import numpy as np

def compute_derivative (x, y):
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
    return yprime

def eckartTranslation(N,pes,equil):
    m = equil.getM()
    M = 0.0
    for i in range(3):
        M += m[i]

    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                x = pes.getPointByN(i,j,k).getX()
                y = pes.getPointByN(i,j,k).getY()
                xcm = ycm = 0.0
                for p in range(3):
                    xcm += m[p]*x[p]
                    ycm += m[p]*y[p]
                xcm = xcm/M
                ycm = ycm/M
                xnew = np.zeros(3)
                ynew = np.zeros(3)
                for p in range(3):
                    xnew[p] = x[p] - xcm
                    ynew[p] = y[p] - ycm
                pes.getPointByN(i,j,k).setX(xnew)
                pes.getPointByN(i,j,k).setY(ynew)
    return

def eckartRotation(N,pes,equil):
    xeq = equil.getX()
    yeq = equil.getY()
    m = equil.getM()
    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                numer = denom = 0.0
                x = pes.getPointByN(i,j,k).getX()
                y = pes.getPointByN(i,j,k).getY()
                for p in range(3):
                    numer += m[p]*(x[p]*yeq[p] - y[p]*xeq[p])
                    denom += m[p]*(x[p]*xeq[p] + y[p]*yeq[p])
                theta = math.atan2(numer,denom)
                xnew = np.zeros(3)
                ynew = np.zeros(3)
                for p in range(3):
                    xnew[p] = x[p]*math.cos(theta) - y[p]*math.sin(theta)
                    ynew[p] = x[p]*math.sin(theta) + y[p]*math.cos(theta)
                pes.getPointByN(i,j,k).setX(xnew)
                pes.getPointByN(i,j,k).setY(ynew)
    return

def calcGMatrix(N,pes,equil):
    eckartTranslation(N,pes,equil)
    eckartRotation(N,pes,equil)

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
                x = pes.getPointByN(i,j,k).getX()
                y = pes.getPointByN(i,j,k).getY()
                q3[k] = pes.getPointByN(i,j,k).getq3()
                x1[k] = x[0]
                y1[k] = y[0]
                x2[k] = x[1]
                y2[k] = y[1]
                x3[k] = x[2]
                y3[k] = y[2]
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
                x = pes.getPointByN(i,j,k).getX()
                y = pes.getPointByN(i,j,k).getY()
                q2[j] = pes.getPointByN(i,j,k).getq2()
                x1[j] = x[0]
                y1[j] = y[0]
                x2[j] = x[1]
                y2[j] = y[1]
                x3[j] = x[2]
                y3[j] = y[2]
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
                x = pes.getPointByN(i,j,k).getX()
                y = pes.getPointByN(i,j,k).getY()
                q1[i] = pes.getPointByN(i,j,k).getq1()
                x1[i] = x[0]
                y1[i] = y[0]
                x2[i] = x[1]
                y2[i] = y[1]
                x3[i] = x[2]
                y3[i] = y[2]
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

    m = equil.getM()
    m1 = m[0]
    m2 = m[1]
    m3 = m[2]

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
