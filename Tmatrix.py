import numpy as np
from util import pyfghutil
import multiprocessing as mp
from scipy.fft import ifft
from scipy.sparse import lil_matrix

#A function to calculate the BMatrix
# B(j,l) = ((4*pi)/(L*N) * sum(p=1,n)(p*sin(2*pi*p*(l-j)/N))
# where n = (N-1)/2
# LValue = L = length of the dimension
# NValue = N = number of points in the dimension
# Each dimension has its own set of B matrices

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

#A function to calculate the CMatrix
# C(j,l) = ((-8*pi*pi)/(L*L*N) * sum(p=1,n)(p*p*cos(2*pi*p*(l-j)/N))
# where n = (N-1)/2
# LValue = L = length of the dimension
# NValue = N = number of points in the dimension
# Each dimension has its own set of C matrices

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

#A function to calculate the individual values for the TMatrix
# Right now, only "approximation 2" is tested.  The other approximations will be for a
# future release.

def Tab(D, N, alpha, beta, B, G):
    total = 0.0

    idx_a = pyfghutil.PointToIndex(N, alpha)
    idx_b = pyfghutil.PointToIndex(N, beta)

    for r in range(D):
        for s in range(D):
            deltacounter = True
            j = 0
            while (deltacounter and (j < D)):
                if ((r != j) and (s != j)):
                    if (idx_a[j] != idx_b[j]):
                        deltacounter = False
                j = j + 1

            if (deltacounter):
                idx = np.copy(idx_a)
                if (r == s):
                    val = 0.0
                    for p in range(N[r]):
                        idx[r] = p
                        pt = pyfghutil.IndexToPoint(N, idx)
                        val += B[r][idx_a[r], p] * B[r][p, idx_b[r]] * G[pt][r][r]
                else:
                    idx[s] = idx_b[s]
                    pt = pyfghutil.IndexToPoint(N, idx)
                    val = B[r][idx_a[r], idx_b[r]] * B[s][idx_a[s], idx_b[s]] * G[pt][r][s]

                total += val

    return (-0.5 * total)

# A function that splits the Tmatrix calculation into blocks to be calculated in parallel.
# Each block uses the Tab function above to calculate individual matrix elements.

def TBlockCalc(dimensions, NValue, blockX, blockY, b_matrix, gmatrix):
    #Blocks will be 0 index
    blockHolder = np.zeros((NValue[0], NValue[0]), float)
    #The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0+NValue[0]*blockX, NValue[0]+NValue[0]*blockX):
        for beta in range(0+NValue[0]*blockY, NValue[0]+NValue[0]*blockY):
            blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, alpha, beta, b_matrix, gmatrix)
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

#The function to calculate a TMatrix using the dataObject class from input
def TMatrixCalc(D, NValue, LValue, GMatrix, cores):
    #Create the TMatrix
    #The alpha and beta values are used to create the TMatrix in the correct position
    Npts = np.prod(NValue)
    tmatrix = lil_matrix((Npts,Npts), dtype=float)

    #Create the B_Matrix
    b_matrix = []
    for x in range(D):
        b_matrix.append(bmatrixgen(NValue[x], LValue[x]))

    blockCoords = []
    blocks = []
    paramz = []
    totalwidth = int(np.prod(NValue))
    repeatamount = int(totalwidth // NValue[0])
    for x in range(repeatamount):
        for y in range(repeatamount):
            blockCoords.append((x,y))
    for coords in blockCoords:
        paramz.append((D, NValue, coords[0], coords[1], b_matrix, GMatrix))
    #Pool and run
    p = mp.Pool(cores)
#    print("Pool go T")
    blocks = p.starmap(TBlockCalc, paramz)
#    print("Pool's done T")
    p.close()

    precalc = 0
    for i in range(len(blockCoords)):
        block = blocks[i]
        x = blockCoords[i][0]
        y = blockCoords[i][1]
        tmatrix[(0+NValue[precalc]*x):(NValue[precalc]+NValue[precalc]*x), (0+NValue[precalc]*y):(NValue[precalc]+NValue[precalc]*y)] = block

    return tmatrix




