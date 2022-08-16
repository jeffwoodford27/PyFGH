import numpy as np
from scipy.fft import fft,ifft, fftfreq
import matplotlib.pyplot as plt

def bmatrixgen(N, L):
    n = (N - 1) // 2
    B = np.zeros((N, N), dtype=float)
    a = np.zeros(N, dtype=complex)
    for i in range(N):
        a[i] = 2 * np.pi * (1j) * (n-i) / L
    afft = fft(a, n=N)
    for k in range(N):
        afft[k] = afft[k] * np.exp(2 * np.pi * (1j) * n * k / N) / N
#        afft[k] = afft[k] / N
    for j in range(N):
        for t in range(N):
            B[j,t] = np.real(afft[(N + j - t) % N])
    return B

def bmatrixgen_old(NValue, LValue):
    n = int((NValue - 1)/2)
    b_matrix = np.zeros((NValue, NValue), float)
    for j in range(NValue):
        for l in range(NValue):
            for p in range(1, n+1):
                b_matrix[j][l] += float(p)*np.sin(2*np.pi*float(p)*float(l-j)/float(NValue))
            b_matrix[j][l] *= (4.0*np.pi)/(LValue*float(NValue))

    return(b_matrix)

def cmatrixgen(N,L):
    n = (N - 1) // 2
    C = np.zeros((N, N), dtype=float)
    a = np.zeros(N, dtype=complex)
    for i in range(N):
        a[i] = -4 * np.pi * np.pi * (i-n) * (i-n) / (L*L)
    aifft = ifft(a, n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)
    for j in range(N):
        for t in range(N):
            C[j, t] = np.real(aifft[(N+j-t)%N])
    return C

'''
N = 8
T = 1

xx = np.array([i*i*i + 2*i*i for i in range(N)], dtype=complex)
print(xx)
print("true derivative")
xpxtrue = np.array([3*i*i + 4*i for i in range(N)], dtype=float)
print(xpxtrue)

xk = fft(xx,n=N)

print("derivative filter")
hk = np.zeros(N,dtype=complex)
for k in range(N):
    if (k < N/2):
        hk[k] = (1j)*2*np.pi*k/N
    else:
        hk[k] = (1j)*2*np.pi*(k-N)/N
#print(hk)
xpk = hk*xk
xpx = ifft(xpk,n=N)
print(xpx)

print("forward difference exponential")
hk = np.array([np.exp((1j)*2*np.pi*k/N)-1 for k in range(N)],dtype=complex)
xpk = hk*xk
xpx = ifft(xpk,n=N)
print(xpx)

print("forward difference power series - exp")
hk = np.zeros(N,dtype=complex)
for k in range(N):
    for m in range(50):
        hk[k] += np.power(((1j)*2*np.pi*k)/N,m)/np.math.factorial(m)
    hk[k] = hk[k] - 1
xpk = hk*xk
xpx = ifft(xpk,n=N)
print(xpx)

print("two-sided difference - sine")
hk = np.array([(1j)*np.sin(2*np.pi*k/N) for k in range(N)],dtype=complex)
xpk = hk*xk
xpx = ifft(xpk,n=N)
print(xpx)

print("expansion in basis functions")
B = np.zeros((N,N),dtype=complex)
for n in range(N):
    for m in range(N):
        for k in range(N):
            B[n,m] += (1j)*np.sin(2*np.pi*k/N)*np.exp((1j)*2*np.pi*k*(n-m)/N)
        B[n,m] = B[n,m] / N
print(B)
xpx = np.zeros(N,dtype=complex)
for n in range(N):
    for m in range(N):
        xpx[n] += B[n,m]*xx[m]
print(xpx)
'''

N1 = 25
N2 = 21
L1 = 12
L2 = 12
dx1 = L1/N1
dx2 = L2/N2
x = np.zeros(N1,dtype=float)
y = np.zeros(N2,dtype=float)
for i in range(N1):
    x[i] = (i-N1/2+1/2)*dx1
for j in range(N2):
    y[j] = (j-N2/2+1/2)*dx2
hermite_max = 10
hermite1 = 6
hermite2 = 8
hpidx1 = np.zeros(hermite_max,dtype=int)
hpidx1[hermite1] = 1
hpidx2 = np.zeros(hermite_max,dtype=int)
hpidx2[hermite2] = 1

#    p = np.polynomial.Hermite(hpidx,domain=[-L/2,L/2])
p1 = np.polynomial.Hermite(hpidx1)
pd1 = p1.deriv(1)
pdd1 = p1.deriv(2)

p2 = np.polynomial.Hermite(hpidx2)
pd2 = p2.deriv(1)
pdd2 = p2.deriv(2)

f = np.zeros((N1,N2),dtype=float)
fpx = np.zeros((N1,N2),dtype=float)
fpy = np.zeros((N1,N2),dtype=float)
fpxx = np.zeros((N1,N2),dtype=float)
fpyy = np.zeros((N1,N2),dtype=float)
fpyx = np.zeros((N1,N2),dtype=float)

for i in range(N1):
    for j in range(N2):
        f[i,j] = p1(x[i]) * p2(y[j]) * np.exp(-(x[i]*x[i]+y[j]*y[j])/2)
        fpx[i,j] = (pd1(x[i]) - x[i]*p1(x[i]))*p2(y[j])*np.exp(-(x[i]*x[i]+y[j]*y[j])/2)
        fpy[i,j] = (pd2(y[j]) - y[j]*p2(y[j]))*p1(x[i])*np.exp(-(x[i]*x[i]+y[j]*y[j])/2)
        fpxx[i,j] = (pdd1(x[i]) - 2*x[i]*pd1(x[i]) + (x[i]*x[i]-1)*p1(x[i])) * p2(y[j]) * np.exp(-(x[i]*x[i]+y[j]*y[j])/2)
        fpyy[i,j] = (pdd2(y[j]) - 2*y[j]*pd2(y[j]) + (y[j]*y[j]-1)*p2(y[j])) * p1(x[i]) * np.exp(-(x[i]*x[i]+y[j]*y[j])/2)
        fpyx[i,j] = (pd1(x[i]) - x[i]*p1(x[i])) * (pd2(y[j]) - y[j]*p2(y[j])) * np.exp(-(x[i]*x[i]+y[j]*y[j])/2)

A1 = np.zeros((N1,N1),dtype=float)
for n in range(N1):
    A1[n,n] = 1

A2 = np.zeros((N2,N2),dtype=float)
for n in range(N2):
    A2[n,n] = 1

B1 = bmatrixgen(N1,L1)
B2 = bmatrixgen(N2,L2)

C1 = cmatrixgen(N1,L1)
C2 = cmatrixgen(N2,L2)

fpxcalc = np.zeros((N1,N2),dtype=float)
fpycalc = np.zeros((N1,N2),dtype=float)

for n1 in range(N1):
    for n2 in range(N2):
        for m1 in range(N1):
            for m2 in range(N2):
                fpxcalc[n1,n2] += B1[n1,m1]*A2[n2,m2]*f[m1,m2]
                fpycalc[n1,n2] += A1[n1,m1]*B2[n2,m2]*f[m1,m2]

fpxxcalc1 = np.zeros((N1,N2),dtype=float)
fpyycalc1 = np.zeros((N1,N2),dtype=float)
fpyxcalc1 = np.zeros((N1,N2),dtype=float)

for n1 in range(N1):
    for n2 in range(N2):
        for m1 in range(N1):
            for m2 in range(N2):
                fpxxcalc1[n1,n2] += B1[n1,m1]*A2[n2,m2]*f[m1,m2]
                fpyycalc1[n1,n2] += A1[n1,m1]*B2[n2,m2]*f[m1,m2]
                fpyxcalc1[n1,n2] += B1[n1,m1]*A2[n2,m2]*f[m1,m2]

fpxxcalc = np.zeros((N1,N2),dtype=float)
fpyycalc = np.zeros((N1,N2),dtype=float)
fpyxcalc = np.zeros((N1,N2),dtype=float)

for n1 in range(N1):
    for n2 in range(N2):
        for m1 in range(N1):
            for m2 in range(N2):
               fpxxcalc[n1,n2] += B1[n1,m1]*A2[n2,m2]*fpxxcalc1[m1,m2]
               fpyycalc[n1,n2] += A1[n1,m1]*B2[n2,m2]*fpyycalc1[m1,m2]
               fpyxcalc[n1,n2] += A1[n1,m1]*B2[n2,m2]*fpyxcalc1[m1,m2]


fpxxcalc2 = np.zeros((N1,N2),dtype=float)
Bp1 = np.matmul(B1,B1)
Ap2 = np.matmul(A2,A2)

for n1 in range(N1):
    for n2 in range(N2):
        for m1 in range(N1):
            for m2 in range(N2):
                fpxxcalc2[n1,n2] += Bp1[n1,m1]*Ap2[n2,m2]*f[m1,m2]



'''

for i in range(N1):
    for j in range(N2):
        print("i = {0} j = {1} fpx = {2} fpxcalc = {3}".format(i, j, fpx[i,j], fpxcalc[i,j]))

for i in range(N1):
    for j in range(N2):
        print("i = {0} j = {1} fpy = {2} fpycalc = {3}".format(i, j, fpy[i,j], fpycalc[i,j]))

for i in range(N1):
    for j in range(N2):
        print("i = {0} j = {1} fpyx = {2} fpyxcalc = {3}".format(i, j, fpyx[i,j], fpyxcalc[i,j]))
'''

for i in range(N1):
    y = np.zeros(N2, dtype=float)
    ycalc = np.zeros(N2, dtype=float)
    for j in range(N2):
        y[j] = fpxx[i,j]
        ycalc[j] = fpxxcalc2[i,j]
    plt.plot(y)
    plt.plot(ycalc)
    plt.show()




#print(x)
#for i in range(10):
#    xx = np.polynomial.hermite.hermval(x,[i])


#    print(xx)
