# Testing whether calculating everything as FFT's is faster than not.

import numpy as np
from scipy.fft import fft, ifft, fftn, ifftn

def bmatrixgen(N,L):
    n = (N-1)//2
    B = np.zeros((N,N),dtype=float)
    a = np.zeros(N,dtype=complex)
    for i in range(N):
        a[i] = 2*np.pi*(1j)*(i-n)/L
    aifft = ifft(a,n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)
    for j in range(N):
        for t in range(N):
            B[j,t] = np.real(aifft[(N+j-t)%N])
    return B

#x = np.array([[2*np.pi*0,2*np.pi*1j,2*np.pi*2j],[2*np.pi*0,2*np.pi*1j,2*np.pi*2j]],dtype=complex)
x = np.array([[2*np.pi*0*np.exp(2*np.pi*(1j)*-1/3),2*np.pi*1j*np.exp(2*np.pi*(1j)*0/3),2*np.pi*2j*np.exp(2*np.pi*(1j)*1/3)],[2*np.pi*-1j,2*np.pi*0,2*np.pi*1j]],dtype=complex)
print(x)
xk = ifftn(x,axes=[1])
for i in range(3):
    xk[1,i] = xk[1,i] * np.exp(-2*np.pi*(1j)*i/3)
print(xk)

#y = np.array([[6,-2+2*1j,-2,-2-2*1j],[6,-2+2*1j,-2,-2-2*1j]],dtype=complex)
#print(y)
#print(ifftn(y,axes=0))