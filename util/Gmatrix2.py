import pyfghutil
import scipy
from scipy import interpolate
from scipy import misc
from scipy import linalg
import numpy as np

def compute_derivative (x, y, N):
    dx = 1e-5
    spl = scipy.interpolate.interp1d(x,y)
    yprime = np.zeros(N)
    yprime[0] = scipy.misc.derivative(spl,x[0]+dx,dx=dx)
    for i in range(1,N-1):
        yprime[i] = scipy.misc.derivative(spl,x[i],dx=dx)
    yprime[N-1] = scipy.misc.derivative(spl,x[N-1]-dx,dx=dx)
    return yprime

def calcGMatrix(atomlist, N, PES):
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
                q3[k] = PES.getPointByN(i,j,k).getq3()
                x1[k] = PES.getPointByN(i,j,k).struct.x[0]
                y1[k] = PES.getPointByN(i,j,k).struct.y[0]
                x2[k] = PES.getPointByN(i,j,k).struct.x[1]
                y2[k] = PES.getPointByN(i,j,k).struct.y[1]
                x3[k] = PES.getPointByN(i,j,k).struct.x[2]
                y3[k] = PES.getPointByN(i,j,k).struct.y[2]
            x1p = compute_derivative(q3,x1,N[2])
            y1p = compute_derivative(q3,y1,N[2])
            x2p = compute_derivative(q3,x2,N[2])
            y2p = compute_derivative(q3,y2,N[2])
            x3p = compute_derivative(q3,x3,N[2])
            y3p = compute_derivative(q3,y3,N[2])
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
                q2[j] = PES.getPointByN(i,j,k).getq2()
                x1[j] = PES.getPointByN(i,j,k).struct.x[0]
                y1[j] = PES.getPointByN(i,j,k).struct.y[0]
                x2[j] = PES.getPointByN(i,j,k).struct.x[1]
                y2[j] = PES.getPointByN(i,j,k).struct.y[1]
                x3[j] = PES.getPointByN(i,j,k).struct.x[2]
                y3[j] = PES.getPointByN(i,j,k).struct.y[2]
            x1p = compute_derivative(q2,x1,N[1])
            y1p = compute_derivative(q2,y1,N[1])
            x2p = compute_derivative(q2,x2,N[1])
            y2p = compute_derivative(q2,y2,N[1])
            x3p = compute_derivative(q2,x3,N[1])
            y3p = compute_derivative(q2,y3,N[1])
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
                q1[i] = PES.getPointByN(i,j,k).getq1()
                x1[i] = PES.getPointByN(i,j,k).struct.x[0]
                y1[i] = PES.getPointByN(i,j,k).struct.y[0]
                x2[i] = PES.getPointByN(i,j,k).struct.x[1]
                y2[i] = PES.getPointByN(i,j,k).struct.y[1]
                x3[i] = PES.getPointByN(i,j,k).struct.x[2]
                y3[i] = PES.getPointByN(i,j,k).struct.y[2]
            x1p = compute_derivative(q1,x1,N[0])
            y1p = compute_derivative(q1,y1,N[0])
            x2p = compute_derivative(q1,x2,N[0])
            y2p = compute_derivative(q1,y2,N[0])
            x3p = compute_derivative(q1,x3,N[0])
            y3p = compute_derivative(q1,y3,N[0])
            for i in range(N[0]):
                dx1dq1[i][j][k] = x1p[i]
                dy1dq1[i][j][k] = y1p[i]
                dx2dq1[i][j][k] = x2p[i]
                dy2dq1[i][j][k] = y2p[i]
                dx3dq1[i][j][k] = x3p[i]
                dy3dq1[i][j][k] = y3p[i]

    m1 = atomlist[0].m
    m2 = atomlist[1].m
    m3 = atomlist[2].m

    GMatrix = np.zeros([int(np.prod(N)),3,3],float)

    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                G = np.zeros([3,3])
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

                dimensionCounterArray = np.zeros((6, 1), int)
                dimensionCounterArray[1] = i
                dimensionCounterArray[3] = j
                dimensionCounterArray[5] = k
                alpha = pyfghutil.AlphaCalc(3, dimensionCounterArray, N)

                for r in range(3):
                    for s in range(3):
                        GMatrix[alpha[0]][r][s] = Ginv[r][s]

    return GMatrix
