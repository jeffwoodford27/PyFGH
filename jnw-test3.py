import numpy as np
from scipy.fft import ifft
import time

np.set_printoptions(threshold=np.inf)

#This file has an improved method for calculating the T matrix.

class InputData:

    def __init__(self, D):
        self.ncore = 1
        self.D = D
        self.N = np.zeros(D)
        self.L = np.zeros(D)

    def setCores(self, cores):
        self.ncore = cores
        return

# N is a list of length D
    def setN(self, N, ndim=None):
        if (ndim == None):
            self.N = N
        else:
            self.N[ndim-1] = N
        return

# L is a list of length D
    def setL(self, L, ndim=None):
        if (ndim == None):
            self.L = L
        else:
            self.L[ndim-1] = L
        return

    def getD(self):
        return self.D

    def getN(self, ndim=None):
        if (ndim == None):
            return self.N
        else:
            return self.N[ndim-1]

    def getL(self, ndim=None):
        if (ndim == None):
            return self.L
        else:
            return self.L[ndim-1]

def calcCmatrix(N,L):
    n = (N - 1) // 2
    C = np.zeros((N, N), dtype=float)
    a = np.zeros(N, dtype=complex)
    for i in range(N):
        a[i] = -4 * np.pi * np.pi * (i-n) * (i-n) / (L*L)
    aifft = ifft(a, n=N)
    for k in range(N):
        aifft[k] = aifft[k] * np.exp(-2 * np.pi * (1j) * n * k / N)
#    print(aifft)
    for j in range(N):
        for t in range(N):
            C[j, t] = np.real(aifft[(N+j-t)%N])
    return C

def PointToIndex(D,N,pt):
    idx = np.zeros(D,dtype=int)
    p = pt
    for j in range(D):
        idx[j] = p % N[j]
        p = p // N[j]
    return idx

def NewCounter(D,  N, alpha, beta):
    alphaidx = PointToIndex(D, N, alpha)
    betaidx = PointToIndex(D, N, beta)
    counter = np.zeros(D * 2, int)
    for j in range(D):
        counter[2 * j] = betaidx[D - j - 1]
        counter[2 * j + 1] = alphaidx[D - j - 1]
    return counter

def TBlockCalc(dimensions, NValue, LValue, b_matrix, c_matrix, approximation, blockX, blockY, gmatrix):
    #Blocks will be 0 index
    blockHolder = np.zeros((NValue[0], NValue[0]), float)
    #The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0+NValue[0]*blockX, NValue[0]+NValue[0]*blockX):
        for beta in range(0+NValue[0]*blockY, NValue[0]+NValue[0]*blockY):
            counter = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
            if(approximation > 2):
                counter1 = int(counter[0])
                counter2 = int(counter[2])
                counter3 = int(counter[4])
                blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, LValue, mu, c_matrix, counter, approximation, b_matrix, gmatrix[counter1][counter2][counter3])
            else:
                blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, LValue, mu, c_matrix, counter, approximation, b_matrix, gmatrix)
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

def TMatrixCalc(dataObject, GMatrix):
    # Establish variables needed
    NValue = dataObject.getN()
    LValue = dataObject.getL()
    D = dataObject.getD()
#    pes = dataObject.PES
    dimensionCounterArray = np.zeros( D *2, int)
    Tapprox = 2

    # Create the TMatrix and the TFlagMatrix
    # The alpha and beta values are used to create the TMatrix in the correct position
    tmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)
    tflag = np.zeros((np.prod(NValue), np.prod(NValue)), int)
    alpha = 0
    beta = 0

    # Create the C_Matrix
    c_matrix = []
    for x in reversed(range(D)):
        c_matrix.append(cmatrixgen(NValue[x], LValue[x]))

    # Create the B_Matrix if necessary
    if(Tapprox < 4):
        b_matrix = []
        for x in reversed(range(D)):
            b_matrix.append(bmatrixgen(NValue[x], LValue[x]))
    else:
        b_matrix = None

    blockCoords = []
    blocks = []
    paramz = []
    totalwidth = int(np.prod(NValue))
    repeatamount = int(totalwidth // NValue[0])
    for x in range(repeatamount):
        for y in range(repeatamount):
            blockCoords.append((x ,y))
    for coords in blockCoords:
        paramz.append((D, NValue, LValue, b_matrix, c_matrix, Tapprox, coords[0], coords[1], GMatrix))

    # Pool and run
    p = mp.Pool(dataObject.getCores())
    #    print("Pool go T")
    blocks = p.starmap(TBlockCalc, paramz)
    #    print("Pool's done T")
    p.close()

    precalc = 0
    for i in range(len(blockCoords)):
        block = blocks[i]
        x = blockCoords[i][0]
        y = blockCoords[i][1]
        tmatrix[( 0 +NValue[precalc ] *x):(NValue[precalc ] +NValue[precalc ] *x), ( 0 +NValue[precalc ] *y):(NValue[precalc ] +NValue[precalc ] *y)] = block


    return tmatrix

def DiracDelta(j,k):
    if (j == k):
        return 1
    else:
        return 0

D = 7
N = np.zeros(D,dtype=int)
L = np.zeros(D,dtype=float)
for i in range(D):
    N[i] = 3
    L[i] = 2.0

dataObject = InputData(D)
dataObject.setN(N)
dataObject.setL(L)

Cmatrix = []
for i in range(D):
    Cmatrix.append(calcCmatrix(N[i],L[i]))

Npts = np.prod(N)

t0 = time.perf_counter()
Tmatrix = np.zeros([Npts,Npts],dtype=float)
for alpha in range(Npts):
    idx_a = PointToIndex(D,N,alpha)
    for beta in range(Npts):
        idx_b = PointToIndex(D,N,beta)
        for i in range(D):
            deltacounter = False
            j = 0
            while ((not deltacounter) and (j < D)):
                if (i == j):
                    term = Cmatrix[i][idx_a[i],idx_b[i]]
                else:
                    if (DiracDelta(idx_a[j],idx_b[j]) == 0):
                        deltacounter = True
                        term = 0
                j = j + 1
            Tmatrix[alpha,beta] += term

        Tmatrix[alpha,beta] *= (-1.0/2.0)
t1 = time.perf_counter()
print(Tmatrix[0])
print(t1-t0)

print ("\n\n\n")

t0 = time.perf_counter()
Tmatrix2 = np.zeros([Npts,Npts],dtype=float)
for alpha in range(Npts):
    for beta in range(Npts):
        dimensionCounterArray = NewCounter(D,N,alpha,beta)
        total = 0

        for T in range(D):
            # Check if the T counter is not equal to the index of the C value being tested, and if so it checks for if the dimension's corrosponding x and y values equal each other.
            Deltacounter = 0
            for Ccounter in range(D):
                if (Ccounter != T):
                    if (dimensionCounterArray[Ccounter * 2] == dimensionCounterArray[(Ccounter * 2) + 1]):
                        Deltacounter += 1
                else:
                    pass
            # If deltacounter equals the dimensions - 1, add the formula to the total for that C value
            if (Deltacounter == (D - 1)):
                # print(dimensionCounterArray)
                try:
                    total += (-1.0 / 2.0) * (1) * (Cmatrix[T][dimensionCounterArray[(T * 2) + 1], dimensionCounterArray[T * 2]])
                except:
                    print("Trying to access: " + str(dimensionCounterArray[(T * 2) + 1]) + ", " + str(
                        dimensionCounterArray[T * 2]))
                    print(Cmatrix[T])
                    print("TAB error")
        Tmatrix2[alpha,beta] = total
t1 = time.perf_counter()
print (Tmatrix2[0])
print(t1-t0)

chisq = 0
for i in range(Npts):
    chisq = chisq + (Tmatrix2[0][i]-Tmatrix[0][i])*(Tmatrix2[0][i]-Tmatrix[0][i])
chisq = np.sqrt(chisq)
print(chisq)