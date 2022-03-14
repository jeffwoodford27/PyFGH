import scipy
from scipy import interpolate
import math
from scipy import linalg
import numpy as np
import pandas
import sys
import csv
import Tmatrix
import Vmatrix
from util import pyfghutil
np.set_printoptions(threshold=sys.maxsize)

class Molecule:
    def __init__(self,s,m,x,y):
        self.s = s
        self.m = m
        self.x = x
        self.y = y
        
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

def main():
    R1eq = 0.9520380
    R2eq = 1.3757822
    #Converts angstroms to bohr
    R1eq = R1eq * 1.889726
    R2eq = R2eq * 1.889726
    theta_eq = 99.8018287 * math.pi / 180.0
    m = [15.999, 1.00782, 18.998]
    for i in range(3):
        m[i] = m[i] * 1822.89
    M = np.sum(m)

    N = [11,11,11]
    L = [0.9150, 0.4289, 1.4425]
    pesfile = "potential_surface.csv"

    s = ['O','H','F']
    x_eq = np.zeros(3,float)
    y_eq = np.zeros(3,float)

    x_eq[0] = (m[1] * R1eq - m[2] * R2eq) * math.sin(theta_eq / 2) / M
    y_eq[0] = -(m[2] * R2eq + m[1] * R1eq) * math.cos(theta_eq / 2) / M
    x_eq[1] = x_eq[0] - R1eq * math.sin(theta_eq / 2)
    y_eq[1] = y_eq[0] + R1eq * math.cos(theta_eq / 2)
    x_eq[2] = x_eq[0] + R2eq * math.sin(theta_eq / 2)
    y_eq[2] = y_eq[0] + R2eq * math.cos(theta_eq / 2)

    equilMol = Molecule(s,m,x_eq,y_eq)
    equilPESpoint = pyfghutil.PESpoint(-1,[0,0,0],equilMol,0)
    df = pandas.read_csv(pesfile,names=['q1','q2','q3','x1','y1','x2','y2','x3','y3','en'])
    waterpot = pyfghutil.PotentialEnergySurface(N,df,equilPESpoint)


    eckartTranslation(N,waterpot,equilPESpoint)
    eckartRotation(N,waterpot,equilPESpoint)
    Gmatrix = calcGMatrix(N,waterpot,equilPESpoint)

    params = pyfghutil.Parameters(3, N, L, 2, "File", None, waterpot, Gmatrix)
    print("TMat")
    TMat = Tmatrix.TMatrixCalc(params, 3)
    print("VMat")
    VMat = Vmatrix.VMatrixCalc(params, 3)

    Hmatrix = TMat + VMat

    eigenval,eigenvec = scipy.linalg.eigh(Hmatrix)
    eigenval = eigenval*219474.6

    wfnorder = np.argsort(eigenval)
    for i in range(1,20):
        print(eigenval[wfnorder[i]]-eigenval[wfnorder[0]])

    Npts = int(np.prod(N))
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
if __name__ == "__main__":
    main()
