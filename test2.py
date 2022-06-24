import numpy as np
from scipy.fft import ifft
import math
import time

#This file has an improved method for calculating the B and C matrices, using Inverse FFT's.



def bmatrixgen(NValue, LValue):
    n = int((NValue - 1) / 2)
    b_matrix = np.zeros((NValue, NValue), float)
    for j in range(NValue):
        for l in range(NValue):
            for p in range(1, n + 1):
                b_matrix[j][l] += float(p) * math.sin(2 * math.pi * float(p) * float(l - j) / float(NValue))
            b_matrix[j][l] *= (4.0 * math.pi) / (LValue * float(NValue))

    return (b_matrix)

def Bnew(N,L):
    n = (N-1)//2
    B = np.zeros((N,N),dtype=float)
    a = np.zeros(N,dtype=complex)
    for i in range(N):
        a[i] = 2*math.pi*(1j)*(i-n)/L
    aifft = ifft(a,n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * math.pi * (1j) * n * k / N)
#    print(aifft)
    for j in range(N):
        for t in range(N):
            B[j,t] = np.real(aifft[(N+j-t)%N])
    return B

def cmatrixgen(NValue, LValue):
    #Generate the CMatrix
    c_matrix_local = np.zeros((NValue, NValue), float)
    #Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = np.zeros((NValue, 1), float)
    for a in range(NValue):
        for b in range(int((NValue-1)/2)):
            difc_matrix[a] += (((b+1)*(b+1))*math.cos(((b+1)*2*math.pi*a)/ NValue))
        difc_matrix[a] *= (-8.0*(math.pi*math.pi)/(float(NValue)*(float(LValue)*float(LValue))))
    #Push the difc_matrix values to their respective c_matrix spots
    for y in range(NValue):
        for x in range(NValue):
            c_matrix_local[x, y] = (difc_matrix[abs(x-y)])
    #Return the matrix
    return c_matrix_local

def Cnew(N,L):
    n = (N - 1) // 2
    C = np.zeros((N, N), dtype=float)
    a = np.zeros(N, dtype=complex)
    for i in range(N):
        a[i] = -4 * math.pi * math.pi * (i-n) * (i-n) / (L*L)
    aifft = ifft(a, n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * math.pi * (1j) * n * k / N)
    print(aifft)
    for j in range(N):
        for t in range(N):
            C[j, t] = np.real(aifft[(N+j-t)%N])
    return C

N = 15
L = 10
n = (N-1) // 2
a = np.zeros(N,dtype=complex)
for i in range(N):
    a[i] = 2*math.pi*(1j)*(-n*i)/L

#print(a)

for N in range(15,35,2):
    print(N)

    t0 = time.perf_counter()
#    B_orig = bmatrixgen(N,L)
    C_orig = cmatrixgen(N,L)
    t1 = time.perf_counter()
#    print(B_orig)
#    print(C_orig)
    print(t1-t0)

    t0 = time.perf_counter()
#    B_new = Bnew(N,L)
    C_new = Cnew(N,L)
    t1 = time.perf_counter()
#    print(B_new)
#    print(C_new)
    print(t1-t0)

    chisq = 0
    for j in range(N):
        for t in range(N):
#            chisq = chisq + (B_orig[t,j]-B_new[t,j])*(B_orig[t,j]-B_new[t,j])
            chisq = chisq + (C_orig[t,j]-C_new[t,j])*(C_orig[t,j]-C_new[t,j])
    chisq = np.sqrt(chisq)

    print(chisq)

    print("\n")
