import numpy as np
from scipy.fft import ifft

def bmatrixgen(NValue, LValue):
    n = int((NValue - 1) / 2)
    b_matrix = np.zeros((NValue, NValue), dtype=float)
    for j in range(NValue):
        for t in range(NValue):
            for p in range(1, n + 1):
                b_matrix[j][t] += float(p) * np.sin(2 * np.pi * float(p) * float(j - t) / float(NValue))
            b_matrix[j][t] *= (-4.0 * np.pi) / (LValue * float(NValue))

    return (b_matrix)

def Bnew(N,L):
    n = (N-1)//2
    B = np.zeros((N,N),dtype=float)
    a = np.zeros(N,dtype=complex)
    for i in range(N):
        a[i] = 2*np.pi*(1j)*(i-n)/L
    aifft = ifft(a,n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)
#    print(aifft)
    for j in range(N):
        for t in range(N):
            B[j,t] = np.real(aifft[(N+j-t)%N])
    return B


L = 1
N = int(55)
dx = L/float(N)
x = np.zeros(N,dtype=float)
f = np.zeros(N,dtype=float)
f1 = np.zeros(N,dtype=float)
f2 = np.zeros(N,dtype=float)
df = np.zeros(N,dtype=float)
df2 = np.zeros(N,dtype=float)
for i in range(N):
#    x[i] = float(i)*dx
    x[i] = float(i-(N-1)/2)*dx
    f[i] = x[i]*x[i]*x[i]
#    f2[i] = (-x[i])*(-x[i])*(-x[i])
#    f[i] = (f1[i]+f2[i])/2
    df[i] = 3*x[i]*x[i]
    df2[i] = 12*x[i]*x[i]

dfn = np.zeros(N,dtype=float)
df2n = np.zeros(N,dtype=float)
B = Bnew(N,L)
#print(B)

for j in range(N):
    for t in range(N):
        dfn[j] += B[j,t] * f[t]

#print(x)
#print(f)
print(df)
print(dfn)
print((df-dfn)/df*100)



