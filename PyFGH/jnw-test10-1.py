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

N = 25
L = 10
dx = L/N
x = np.zeros(N,dtype=float)
for i in range(N):
    x[i] = (i-N/2+1/2)*dx
print(x)
hermite_max = 20
hermite = 3
hpidx = np.zeros(hermite_max,dtype=int)
hpidx[hermite] = 1

p = np.polynomial.Hermite(hpidx)
pd = p.deriv(1)
pdd = p.deriv(2)

f = np.zeros(N,dtype=float)
fp = np.zeros(N,dtype=float)
fpxx = np.zeros(N,dtype=float)

for i in range(N):
    f[i] = p(x[i]) * np.exp(-x[i]*x[i]/2)
    fp[i] = (pd(x[i]) - x[i]*p(x[i]))*np.exp(-x[i]*x[i]/2)
    fpxx[i] = (pdd(x[i]) - 2 * x[i] * pd(x[i]) + (x[i] * x[i] - 1) * p(x[i])) * np.exp(-x[i] * x[i]/ 2)

A = np.zeros((N,N),dtype=float)
for n in range(N):
    A[n,n] = 1

B = bmatrixgen(N,L)

fpcalc = np.zeros(N,dtype=float)
fpxxcalc = np.zeros(N,dtype=float)

Bp = np.matmul(B,B)

for n in range(N):
    for m in range(N):
        fpcalc[n] += B[n,m]*f[m]
        fpxxcalc[n] += Bp[n,m]*f[m]


#for i in range(N):
#    print("i = {0} fp = {1} fpcalc = {2}".format(i, fp[i], fpcalc[i]))

plt.plot(fp)
plt.plot(fpcalc)
plt.show()

plt.plot(fpxx)
plt.plot(fpxxcalc)
plt.show()

#y = np.zeros(N,dtype=float)
#for i in range(N):
#    y[i] = B[N//2,i]

#plt.plot(y)
#plt.show()


#print(x)
#for i in range(10):
#    xx = np.polynomial.hermite.hermval(x,[i])


#    print(xx)
