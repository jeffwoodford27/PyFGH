import numpy as np
import scipy
from scipy import interpolate

# This testing file has an improved method for calculating the G matrix.
# The PointToIdxs feature should be harmonized with that in test1.

def PointToIdxs(D,N,pt):
    idx = np.zeros(D,dtype=int)

    for i in range(D-1,-1,-1):
        idx[i] = np.mod(pt,N[i])
        pt = pt//N[i]
    return idx

def compute_derivative (x, y):
#    print(x,y)
    spl = scipy.interpolate.splrep(x,y,s=0)
    yprime = scipy.interpolate.splev(x,spl,der=1)
#    print(yprime)
    return yprime

D = 3
N = np.zeros(D,dtype=int)
N[0] = 5
N[1] = 7
N[2] = 9

dq = 0.1
q = []
for i in range(D):
    q.append(np.zeros(N[i],dtype=float))

for i in range(D):
    for j in range(N[i]):
        q[i][j] = (j-N[i]//2)*dq

Npts = np.prod(N)
f = np.zeros(Npts,dtype=float)
for i in range(Npts):
    idx = PointToIdxs(D,N,i)
    f[i] = np.pow(q[0][idx[0]],2)*np.pow(q[1][idx[1]],3)*q[2][idx[2]]

dfdq = []
dfdqcalc = []
for i in range(D):
    dfdq.append(np.zeros(Npts,dtype=float))
    dfdqcalc.append(np.zeros(Npts,dtype=int))

for n in range(Npts):
    for d in range(D-1,-1,-1):
        if (dfdqcalc[d][n] == 0):
#            print ("for point " + str(n) + " in dimension " + str(d))
            x = np.zeros(N[d],dtype=float)
            y = np.zeros(N[d],dtype=float)
            dy = np.zeros(N[d],dtype=float)
            for i in range(N[d]):
                x[i] = q[d][i]
                y[i] = f[n+i*np.prod(N[d+1:])]
#            print(x,y)
            dy = compute_derivative(x,y)
            for i in range(N[d]):
                dfdq[d][n+i*np.prod(N[d+1:])] = dy[i]
                dfdqcalc[d][n+i*np.prod(N[d+1:])] = 1
#                print ("   setting derivative using point " + str(n+i*np.prod(N[d+1:])))
        else:
            pass
#            print("skip point " + str(n) + " for dimension " + str(d))

for n in range(Npts):
    idx = PointToIdxs(D,N,n)
    print(n,q[0][idx[0]],q[1][idx[1]],q[2][idx[2]],dfdq[0][n],dfdq[1][n],dfdq[2][n])

