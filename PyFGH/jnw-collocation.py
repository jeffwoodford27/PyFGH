import numpy as np
from scipy.linalg import eig,eigh,eigvals
import matplotlib.pyplot as plt
from numpy.polynomial.hermite import Hermite as He

def delta(x,y):
    if (x == y):
        return 1
    else:
        return 0

L = 1.4
N = 15
Ngr = N
n = (N-1)//2

hbar = 1
mu = 919
kf = 0.37
alpha = np.sqrt(kf*mu)/hbar

x = np.zeros(Ngr,dtype=float)
for i in range(Ngr):
    x[i] = (i-N//2)*L/N

Hfunc = []
Hfunc1d = []
Hfunc2d = []
for i in range(Ngr):
    coef = np.zeros(Ngr, dtype=int)
    coef[i] = 1
    Hfunc.append(He(coef))
    Hfunc1d.append(He(coef).deriv(m=1))
    Hfunc2d.append(He(coef).deriv(m=2))

phi = np.zeros([Ngr,Ngr],dtype=float)
phi2d = np.zeros([Ngr,Ngr],dtype=float)

T = np.zeros([Ngr,Ngr],dtype=float)
V = np.zeros([Ngr,Ngr],dtype=float)
H = np.zeros([Ngr,Ngr],dtype=float)

for k in range(Ngr):
    for i in range(Ngr):
        y = np.sqrt(alpha)*x[i]
        phi[k,i] = Hfunc[k](y)*np.exp(-y*y/2)
        phi2d[k,i] = alpha*((y*y-1)*Hfunc[k](y) - 2*y*Hfunc1d[k](y) + Hfunc2d[k](y))*np.exp(-y*y/2)

    for i in range(Ngr):
        T[k,i] = (-hbar*hbar)/(2*mu) * phi2d[k,i]
        V[k,i] = 0.5*kf*x[i]*x[i]*phi[k,i]
        H[k,i] = T[k,i] + V[k,i]

eval = eigvals(H,phi)
print(np.sort(eval))

phi = np.zeros([Ngr,Ngr],dtype=complex)
T = np.zeros([Ngr,Ngr],dtype=complex)
V = np.zeros([Ngr,Ngr],dtype=complex)

for k in range(Ngr):
    for i in range(Ngr):
        for p in range(-n,n+1,1):
            phi[k,i] += np.exp(-2*np.pi*(1j)*p*k/N)*np.exp(2*np.pi*(1j)*p*x[i]/L) / N

for k in range(Ngr):
    for i in range(Ngr):
        for p in range(-n,n+1,1):
            T[k,i] += (-hbar*hbar)/(2*mu)*(-4*np.pi*np.pi*p*p)/(L*L)*np.exp(2*np.pi*(1j)*p*x[i]/L)*np.exp(-2*np.pi*(1j)*p*k/N) / N
        V[k,i] = 0.5*kf*x[i]*x[i]*phi[k,i]

H = T + V

print(phi[0])

eval = eigvals(H,phi)
print(np.sort(eval))
