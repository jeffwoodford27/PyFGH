from util import model_objects
import numpy as np
import math
import time
import sys
import scipy.linalg

#Remove the numpy print limits
np.set_printoptions(threshold=sys.maxsize)


def calc_idx(D, N, idx):
    ans = np.zeros(D,int)
    ans[D-1] = idx%N[0]
    frac = idx/N[0]
    for i in range(1,D):
        ans[D-1-i] = frac%N[i]
        frac = frac/N[i]
    return(ans)


# Input:
# L (float) - length of grid
# N (int) - number of points
# i (int) - the integer argument for the cosine function, equal to (k-j) (given below)
# Output:
# The element of the C matrix (float), used for second derivatives, calculated as follows.
# C_jk = (-8*pi^2)/(N*L^2) * sum_{p=1}^n { p^2 cos(2*pi*p*(k-j)/N) }
# where n = (N-1)/2

def calc_C(L, N, i):
    Nfl = float(N)
    ifl = float(i)
    n = int((N-1)/2)
    ans = 0
    for p in range(1,n+1):
        pflsq = float(p*p)
        ans += pflsq*math.cos(2*math.pi*pfl*ifl/Nfl)
    ans *= (-8.0*math.pi*math.pi)/(Nfl*L*L)
    return(ans)

# Input:
# j, k (two ints)
# Output:
# The Kroenecker delta function \delta_{j,k} (as int), equals 1 if j = k, and equals 0 if j != k.

def calc_delta(j,k):
    if (j == k):
        return 1
    else:
        return 0

# Input:
# D (int): number of dimensions
# N (array of ints): an array of length D of the number of points in each dimension
# L (array of floats): an array of length D of the length of each dimension
# mu (array of floats): an array of lenght D of the reduced mass in each dimension
# Output:
# The T matrix of Model 4 for model oscillators only, defined as:

# T[a,b] = (-hbar^2)/(2*mu[1]) * C[j1,t1] * delta[j2,t2] * delta[j3,t3] * ... * delta[jD,tD]
#        + (-hbar^2)/(2*mu[2]) * delta[j1,t1] * C[j2,t2] * delta[j3,t3] * ... * delta[jD,tD]
#        + (-hbar^2)/(2*mu[3]) * delta[j1,t1] * delta[j2,t2] * C[j3,t3] * ... * delta[jD,tD]
#        + ...
#        + (-hbar^2)/(2*mu[D]) * delta[j1,t1] * delta[j2,t2] * delta[j3,t3] * ... * C[jD,tD]
#
# where delta[i,j] is the Kroenecker delta function, and C[i,j] is the C matrix element.
# a and b are each of length Npt = N1 * N2 * N3 * ... * ND
# The T matrix is symmetric, T[a,b] = T[b,a].
# The strategy is:
# 1. Loop over a = 0,...,Npt-1
# 2. Loop over b = a,...,Npt-1
# 3. Loop over the dimensions i = 0,...,D-1 to accumulate each line of the above sum for each dimension
# 4. Loop over the dimensions j = 0,...,D-1 to evaluate the product occurring on each line above.
# 5. For j =/= i, calculate the Kroenecker delta function.  If any are zero, then skip - the value is zero.
#    But, if all are equal to 1, then evaluate the appropriate C matrix element and accumulate it into T[a,b].

def TMatrixCalc(D, N, L, mu):
    hbar = 1.0
    Npt = np.prod(N)
    tmatrix = np.zeros((Npt,Npt),float)
    Cobj = np.empty(D,dtype=list)
    for i in range(0,D):
        Cobj[i] = np.zeros(N[i])
        for j in range(0,N[i]):
            Cobj[i][j] = calc_C(L[i],N[i],j)
    for a in range(0,Npt):
        a_idx = calc_idx(D, N, a)
        for b in range(a,Npt):
            b_idx = calc_idx(D, N, b)
#            print("alpha: " + str(a) + str(a_idx) + " b: " + str(b) + str(b_idx))

            for i in range(0,D):
                deltacounter = 1
                for j in range(0,D):
                    if(i != j):
                        deltacounter = deltacounter*calc_delta(a_idx[j],b_idx[j])
                if (deltacounter == 1):
                    tmatrix[a,b] += (-hbar*hbar)/(2*mu[i])*Cobj[i][abs(a_idx[i]-b_idx[i])]
            tmatrix[b,a] = tmatrix[a,b]

#            for i in range(0,D):
#                ans = 1.0
#                for j in range(0,D):
#                    if (i == j):
#                        ans = ans * (-hbar*hbar)/(2*mu[i])*Cobj[i][abs(a_idx[i]-b_idx[i])]
#                    else:
#                        ans = ans * calc_delta(a_idx[j],b_idx[j])
#                print ("i: " + str(i) + " contribution " + str(ans))
#                tmatrix[a,b] += ans
#            tmatrix[b,a] = tmatrix[a,b]

    return tmatrix

def CalcPotentialEnergy(x, VModel):
    if (VModel.type == 0):     # Harmonic Oscillator
        k = VModel.param[1]
        return (0.5 * k * x * x)
    elif (VModel.type == 1):   # Morse Oscillator
        De = VModel.param[1]
        a = VModel.param[2]
        return (De*(1-math.exp(-a*x))**2)
    else:
        print("Invalid Potential Energy Model")
        return(0)

# The function to calculate a VMatrix using the mol class from input
def VMatrixCalc(D, N, L, VModel):
    Npt = np.prod(N)
    vmatrix = np.zeros((Npt, Npt), float)

    deltax = np.zeros(D, float)
    for i in range(0, D):
        deltax[i] = L[i] / float(N[i])

    for alpha in range(0, Npt):
        alpha_idx = calc_idx(D, N, alpha)
        for beta in range(alpha, Npt):
            beta_idx = calc_idx(D, N, beta)
            deltaproduct = 1
            for i in range(0, D):
                for j in range(0, D):
                    deltaproduct *= calc_delta(alpha_idx[j], beta_idx[j])
            if (deltaproduct == 1):
                for i in range(0,D):
                    x = (float(alpha_idx[i])+0.5)*deltax[i] - 0.5*L[i]
                    vmatrix[alpha,beta] += CalcPotentialEnergy(x,VModel[i])
            vmatrix[beta,alpha] = vmatrix[alpha,beta]
    return vmatrix


D = 3

VModel = []
N = np.zeros(D, int)
L = np.zeros(D, float)
mu = np.zeros(D, float)
for j in range(0, D):
    N[j] = 5
    L[j] = 2
    mu[j] = 919
    param_list = [919, 0.37]
    VModelObj = model_objects.Harmonic_Oscillator()
    VModelObj.set_param(param_list)
    VModel.append(VModelObj)
TMatrix = TMatrixCalc(D, N, L, mu)
VMatrix = VMatrixCalc(D, N, L, VModel)
HMatrix = TMatrix + VMatrix

try:
    EValues = np.sort(scipy.linalg.eigvals(HMatrix))
except:
    EValues = np.sort(scipy.linalg.eigvals(HMatrix))
opdata = DataObject.OutputData()
opdata.setEigenvalues(EValues)
print(opdata.eigenvalues)