import numpy as np
from scipy.fft import fft,ifft, fftfreq

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



N = 8
L = 8
dx = L/N
#f = [np.exp(2*np.pi*(1j)*i*dx/L) for i in range(N)]
f = [(i*dx)*(i*dx) for i in range(N)]
print(f)
fp = ifft(f,n=N)
print(fp)
print(fft(fp,n=N))
k = fftfreq(n=N,d=dx)
hp = k*(-1j)
print("ifft of hp")
print(ifft(hp,n=N))
print(k)
for p in range(N):
    fp[p] = fp[p]*(-1j)*k[p]
#    kp = 2*np.pi*p/L
#    fp[p] = fp[p] * (-1j)*kp

ff = fft(fp,n=N)
print(ff)



'''
F = np.zeros(N,dtype=complex)

for p in range(N):
    for t in range(N):
        F[p] += f[t]*np.exp(-2*np.pi*(1j)*p*t/N)

print(F)
print(fq)

F[0] = F[0]*2*np.pi*(1j)*(0)/L
F[1] = F[1]*2*np.pi*(1j)*(1)/L
F[2] = F[2]*2*np.pi*(1j)*(-2)/L
F[3] = F[3]*2*np.pi*(1j)*(-1)/L

ff = np.zeros(N,dtype=complex)
for p in range(N):
    ff[0] += F[p]
    ff[1] += F[p]*np.exp(2*np.pi*(1j)*1*p/N)
    ff[2] += F[p]*np.exp(2*np.pi*(1j)*(-2)*p/N)
    ff[3] += F[p]*np.exp(2*np.pi*(1j)*(-1)*p/N)

print(ff)
'''

#for p in range(N):
#    if (p < N/2):
#        fp[p] = fp[p] * (2*np.pi*(1j)*(p)/L)
#    else:
#        fp[p] = fp[p] * (2*np.pi*(1j)*(p-N)/L)
#ff = ifft(fp,n=N)
#print(f)
#print(fp)
#print(ff)


#aifft = ifft(a,n=2*N)

#for k in range(2*N):
#    aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)

#b1 = bmatrixgen(N,L)
#b2 = bmatrixgen_old(N,L)

#print(aifft)
#print(fftfreq(N))

#print(b1)
#print(b2)

#sum = 0
#for j in range(N):
#    for t in range(N):
#       sum += (b2[j,t]-b1[j,t])*(b2[j,t]-b1[j,t])

#sum = np.sqrt(sum)
#print(sum)
