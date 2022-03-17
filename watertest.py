import scipy
from scipy import interpolate
import math
from scipy import linalg
import numpy as np
import pandas
import sys
import csv

np.set_printoptions(threshold=sys.maxsize)

class Molecule:
    def __init__(self,s,m,x,y):
        self.s = s
        self.m = m
        self.x = x
        self.y = y

class PESpoint:
    def __init__(self, n, q, mol, en):
        self.n = n
        self.q = q
        self.mol = mol
        self.en = en

    def getq1(self):
        return self.q[0]

    def getq2(self):
        return self.q[1]

    def getq3(self):
        return self.q[2]

    def getMol(self):
        return self.mol

    def getEnergy(self):
        return self.en

class PotentialEnergySurface:
    def __init__(self, N, df, equil):
        s = equil.mol.s
        m = equil.mol.m
        self.N = N
        n = 0
        self.pts = []
        for i in range(N[0]):
            self.pts.append([])
            for j in range(N[1]):
                self.pts[i].append([])
                for k in range(N[2]):
                    q = np.zeros(3)
                    q[0] = df['q1'][n]
                    q[1] = df['q2'][n]
                    q[2] = df['q3'][n]
                    x = np.zeros(3)
                    x[0] = df['x1'][n]
                    x[1] = df['x2'][n]
                    x[2] = df['x3'][n]
                    y = np.zeros(3)
                    y[0] = df['y1'][n]
                    y[1] = df['y2'][n]
                    y[2] = df['y3'][n]
                    mol = Molecule(s,m,x,y)
                    en = df['en'][n]
#                    if (en > 0.1):
#                        en = 0.1
                    self.pts[i][j].append(PESpoint(n,q,mol,en))
                    n = n + 1

    def getPointByN(self,t,u,v):
        return self.pts[t][u][v]

def eckartTranslation(N,pes,equil):
    M = 0.0
    for i in range(3):
        M += equil.mol.m[i]

    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                xcm = ycm = 0.0
                for p in range(3):
                    xcm += pes.pts[i][j][k].mol.m[p]*pes.pts[i][j][k].mol.x[p]
                    ycm += pes.pts[i][j][k].mol.m[p]*pes.pts[i][j][k].mol.y[p]
                xcm = xcm/M
                ycm = ycm/M
                for p in range(3):
                    pes.pts[i][j][k].mol.x[p] = pes.pts[i][j][k].mol.x[p] - xcm
                    pes.pts[i][j][k].mol.y[p] = pes.pts[i][j][k].mol.y[p] - ycm

    return

def eckartRotation(N,pes,equil):
    xeq = equil.mol.x
    yeq = equil.mol.y
    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                numer = denom = 0.0
                for p in range(3):
                    m = pes.pts[i][j][k].mol.m[p]
                    x = pes.pts[i][j][k].mol.x[p]
                    y = pes.pts[i][j][k].mol.y[p]
                    numer += m*(x*yeq[p] - y*xeq[p])
                    denom += m*(x*xeq[p] + y*yeq[p])
                theta = math.atan2(numer,denom)
                for p in range(3):
                    x = pes.pts[i][j][k].mol.x[p]
                    y = pes.pts[i][j][k].mol.y[p]
                    xnew = x*math.cos(theta) - y*math.sin(theta)
                    ynew = x*math.sin(theta) + y*math.cos(theta)
                    pes.pts[i][j][k].mol.x[p] = xnew
                    pes.pts[i][j][k].mol.y[p] = ynew
    return

def compute_derivative (x, y):
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
    return yprime

def calcGMatrix(N,pes,equil):
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
                x1[k] = pes.getPointByN(i,j,k).mol.x[0]
                y1[k] = pes.getPointByN(i,j,k).mol.y[0]
                x2[k] = pes.getPointByN(i,j,k).mol.x[1]
                y2[k] = pes.getPointByN(i,j,k).mol.y[1]
                x3[k] = pes.getPointByN(i,j,k).mol.x[2]
                y3[k] = pes.getPointByN(i,j,k).mol.y[2]
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
                x1[j] = pes.getPointByN(i,j,k).mol.x[0]
                y1[j] = pes.getPointByN(i,j,k).mol.y[0]
                x2[j] = pes.getPointByN(i,j,k).mol.x[1]
                y2[j] = pes.getPointByN(i,j,k).mol.y[1]
                x3[j] = pes.getPointByN(i,j,k).mol.x[2]
                y3[j] = pes.getPointByN(i,j,k).mol.y[2]
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
                x1[i] = pes.getPointByN(i,j,k).mol.x[0]
                y1[i] = pes.getPointByN(i,j,k).mol.y[0]
                x2[i] = pes.getPointByN(i,j,k).mol.x[1]
                y2[i] = pes.getPointByN(i,j,k).mol.y[1]
                x3[i] = pes.getPointByN(i,j,k).mol.x[2]
                y3[i] = pes.getPointByN(i,j,k).mol.y[2]
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

    m1 = equil.mol.m[0]
    m2 = equil.mol.m[1]
    m3 = equil.mol.m[2]

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

def calcGMatrix2(N,L,m,R1eq,R2eq,theta_eq):
    q1 = np.zeros(N[0], float)
    q2 = np.zeros(N[1], float)
    q3 = np.zeros(N[2], float)

    m1 = m[0]
    m2 = m[1]
    m3 = m[2]

    dq = np.zeros(3,float)
    for i in range(3):
        dq[i] = L[i]/float(N[i])

    for i in range(N[0]):
        q1[i] = dq[0]*float(i-int(N[0]/2))

    for i in range(N[1]):
        q2[i] = dq[1]*float(i-int(N[1]/2))

    for i in range(N[2]):
        q3[i] = dq[2]*float(i-int(N[2]/2))

    Gmatrix2 = np.zeros([N[0], N[1], N[2], 3, 3], float)

    for i in range(N[0]):
        for j in range(N[1]):
            for k in range(N[2]):
                Gmat = np.zeros([3, 3], float)

                R1 = R1eq + q1[i] + q2[j]
                R2 = R2eq + q2[j] - q1[i]
                theta = theta_eq + q3[k]
                Gmat[0][0] = (2 * m2 * m3 * math.cos(theta) + 2 * m2 * m3 + m1 * m3 + m1 * m2) / M
                Gmat[1][1] = (-2 * m2 * m3 * math.cos(theta) + 2 * m2 * m3 + m1 * m3 + m1 * m2) / M
                Gmat[2][2] = (2 * R1 * R2 * m2 * m3 * math.cos(theta)
                              + R2 * R2 * m2 * m3 + R1 * R1 * m2 * m3 + R2 * R2 * m1 * m3 + R1 * R1 * m1 * m2) / (4 * M)

                Gmat[0][1] = Gmat[1][0] = -m1 * (m3 - m2) / M
                Gmat[0][2] = Gmat[2][0] = -m2 * m3 * (2 * q1[i] - R2eq + R1eq) * math.sin(theta) / (2 * M)
                Gmat[1][2] = Gmat[2][1] = m2 * m3 * (2 * q2[j] + R1eq + R2eq) * math.sin(theta) / (2 * M)

                Ginv = scipy.linalg.inv(Gmat)
                for r in range(3):
                    for s in range(3):
                        Gmatrix2[i][j][k][r][s] = Ginv[r][s]
    return Gmatrix2

def calcHMatrix(N,L,Gmatrix,pes):
    mu = 919.0
    fc = 0.37

    B1 = np.zeros([N[0],N[0]],float)
    B2 = np.zeros([N[1],N[1]],float)
    B3 = np.zeros([N[2],N[2]],float)
    C1 = np.zeros([N[0],N[0]],float)
    C2 = np.zeros([N[1],N[1]],float)
    C3 = np.zeros([N[2],N[2]],float)

    for j in range(N[0]):
        for l in range(N[0]):
            n = int((N[0]-1)/2)
            for p in range(1,n+1):
                theta = 2.0*math.pi*float(p)*float(l-j)/float(N[0])
                B1[j][l] += float(p)*math.sin(theta)
                C1[j][l] += float(p)*float(p)*math.cos(theta)
            B1[j][l] *= (4.0*math.pi)/(float(N[0])*L[0])
            C1[j][l] *= (-8.0*math.pi*math.pi)/(float(N[0])*L[0]*L[0])
    for j in range(N[1]):
        for l in range(N[1]):
            n = int((N[1]-1)/2)
            for p in range(1,n+1):
                theta = 2.0 * math.pi * float(p) * float(l - j) / float(N[1])
                B2[j][l] += float(p) * math.sin(theta)
                C2[j][l] += float(p) * float(p) * math.cos(theta)
            B2[j][l] *= (4.0 * math.pi) / (float(N[1]) * L[1])
            C2[j][l] *= (-8.0 * math.pi * math.pi) / (float(N[1]) * L[1] * L[1])
    for j in range(N[2]):
        for l in range(N[2]):
            n = int((N[2]-1)/2)
            for p in range(1,n+1):
                theta = 2.0 * math.pi * float(p) * float(l - j) / float(N[2])
                B3[j][l] += float(p) * math.sin(theta)
                C3[j][l] += float(p) * float(p) * math.cos(theta)
            B3[j][l] *= (4.0 * math.pi) / (float(N[2]) * L[2])
            C3[j][l] *= (-8.0 * math.pi * math.pi) / (float(N[2]) * L[2] * L[2])

    Npts = int(np.prod(N))
    Tmatrix = np.zeros([Npts,Npts],float)
    Vmatrix = np.zeros([Npts,Npts],float)
    Hmatrix = np.zeros([Npts,Npts],float)

    def delta(i,j):
        if (i == j):
            return float(1)
        else:
            return float(0)

    dq = np.zeros(3,float)
    for i in range(3):
        dq[i] = L[i]/float(N[i])

    for alpha in range(Npts):
        l = np.mod(alpha,N[2])
        f = int(alpha/N[2])
        k = np.mod(f,N[1])
        f2 = int(f/N[1])
        j = np.mod(f2,N[0])

        for beta in range(Npts):
            v = np.mod(beta, N[2])
            f = int(beta / N[2])
            u = np.mod(f, N[1])
            f2 = int(f / N[1])
            t = np.mod(f2, N[0])

            sum = 0.0
            for p in range(N[0]):
                sum += B1[j][p]*B1[p][t]*Gmatrix[p][k][l][0][0]
            Tmatrix[alpha,beta] += -0.5*sum * delta(k,u) * delta(l,v)

            sum = 0.0
            for p in range(N[1]):
                sum += B2[k][p]*B2[p][u]*Gmatrix[j][p][l][1][1]
            Tmatrix[alpha,beta] += -0.5*sum*delta(j,t) * delta(l,v)

            sum = 0.0
            for p in range(N[2]):
                sum += B3[l][p]*B3[p][v]*Gmatrix[j][k][p][2][2]
            Tmatrix[alpha,beta] += -0.5*sum*delta(j,t)*delta(k,u)

            Tmatrix[alpha,beta] += -0.5*(B1[j][t]*B2[k][u]*Gmatrix[t][k][l][0][1]) * delta(v,l)
            Tmatrix[alpha,beta] += -0.5*(B1[j][t]*B3[l][v]*Gmatrix[t][k][l][0][2]) * delta(k,u)
            Tmatrix[alpha,beta] += -0.5*(B2[k][u]*B1[j][t]*Gmatrix[j][u][l][1][0]) * delta(v,l)
            Tmatrix[alpha,beta] += -0.5*(B2[k][u]*B3[l][v]*Gmatrix[j][u][l][1][2]) * delta(j,t)
            Tmatrix[alpha,beta] += -0.5*(B3[l][v]*B1[j][t]*Gmatrix[j][k][v][2][0]) * delta(k,u)
            Tmatrix[alpha,beta] += -0.5*(B3[l][v]*B2[k][u]*Gmatrix[j][k][v][2][1]) * delta(j,t)

            Vmatrix[alpha,beta] += pes.getPointByN(t,u,v).en*delta(t,j)*delta(u,k)*delta(v,l)

    for alpha in range(Npts):
        for beta in range(Npts):
            Hmatrix[alpha,beta] = Tmatrix[alpha,beta] + Vmatrix[alpha,beta]

    return Hmatrix

R1eq = R2eq = 1.790172
theta_eq = 105.499838 * math.pi / 180.0
m = [15.99491,1.007825,1.007825]
for i in range(3):
    m[i] = m[i] * 1822.89
M = np.sum(m)

#N = [7,7,7]
#L = [0.7,0.7,0.7]
#pesfile = "waterpot-data.csv"

#N = [11,11,11]
#L = [0.44,0.44,0.22]
#pesfile = "waterpot11A-data.csv"

#N = [11,11,11]
#L = [1.0,1.0,0.5]
#pesfile = "waterpot11B-data.csv"

#N = [11,11,11]
#L = [0.8,0.8,0.8]
#pesfile = "waterpot11C-data.csv"

#N = [11,11,11]
#L = [1.0,1.0,1.0]
#pesfile = "waterpot11D-data.csv"

#N = [11,11,11]
#L = [0.55,0.55,1.1]
#pesfile = "waterpot11E-data.csv"

#N = [11,11,11]
#L = [0.55,0.55,1.65]
#pesfile = "waterpot11F-data.csv"

N = [11,11,11]
L = [1.10,1.10,1.65]
pesfile = "waterpot11G-data.csv"

s = ['O','H','H']
x_eq = np.zeros(3,float)
y_eq = np.zeros(3,float)

x_eq[0] = (m[1] * R1eq - m[2] * R2eq) * math.sin(theta_eq / 2) / M
y_eq[0] = -(m[2] * R2eq + m[1] * R1eq) * math.cos(theta_eq / 2) / M
x_eq[1] = x_eq[0] - R1eq * math.sin(theta_eq / 2)
y_eq[1] = y_eq[0] + R1eq * math.cos(theta_eq / 2)
x_eq[2] = x_eq[0] + R2eq * math.sin(theta_eq / 2)
y_eq[2] = y_eq[0] + R2eq * math.cos(theta_eq / 2)

equilMol = Molecule(s,m,x_eq,y_eq)
equilPESpoint = PESpoint(-1,[0,0,0],equilMol,0)
df = pandas.read_csv(pesfile,names=['q1','q2','q3','x1','y1','x2','y2','x3','y3','en'])
waterpot = PotentialEnergySurface(N,df,equilPESpoint)

Gmatrix = calcGMatrix(N,waterpot,equilPESpoint)
eckartTranslation(N,waterpot,equilPESpoint)
eckartRotation(N,waterpot,equilPESpoint)
Hmatrix = calcHMatrix(N,L,Gmatrix,waterpot)

eigenval,eigenvec = scipy.linalg.eigh(Hmatrix)
eigenval = eigenval*219474.6

wfnorder = np.argsort(eigenval)
for i in range(1,20):
    print(eigenval[wfnorder[i]]-eigenval[wfnorder[0]])

wfn = np.zeros([Npts,N[0],N[1],N[2]],float)

for p in range(Npts):
    for alpha in range(Npts):
        l = np.mod(alpha, N[2])
        f = int(alpha / N[2])
        k = np.mod(f, N[1])
        f2 = int(f / N[1])
        j = np.mod(f2, N[0])

        wfn[p][j][k][l] = eigenvec[alpha][wfnorder[p]]

for p in range(8):
    fname = "eigenvec-"+str(p)+".csv"
    with open(fname, 'w', newline='') as csvfile:
        wfnwriter = csv.writer(csvfile)
        for l in range(N[2]):
            for k in range(N[1]):
                row = []
                for j in range(N[0]):
                    row.append(wfn[p][j][k][l])
                wfnwriter.writerow(row)
            wfnwriter.writerow([])
