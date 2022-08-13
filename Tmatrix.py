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

def bmatrixgen_old(NValue, LValue):
    n = int((NValue - 1)/2)
    b_matrix = np.zeros((NValue, NValue), float)
    for j in range(NValue):
        for l in range(NValue):
            for p in range(1, n+1):
                b_matrix[j][l] += float(p)*np.sin(2*np.pi*float(p)*float(l-j)/float(NValue))
            b_matrix[j][l] *= (4.0*np.pi)/(LValue*float(NValue))

    return(b_matrix)

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

def cmatrixgen_old(NValue, LValue):
    #Generate the CMatrix
    c_matrix_local = np.zeros((NValue, NValue), float)
    #Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = np.zeros((NValue, 1), float)
    for a in range(NValue):
        for b in range(int((NValue-1)/2)):
            difc_matrix[a] += (((b+1)*(b+1))*np.cos(((b+1)*2*np.pi*a)/ NValue))
        difc_matrix[a] *= (-8.0*(np.pi*np.pi)/(float(NValue)*(float(LValue)*float(LValue))))
    #Push the difc_matrix values to their respective c_matrix spots
    for y in range(NValue):
        for x in range(NValue):
            c_matrix_local[x, y] = (difc_matrix[abs(x-y)])
    #Return the matrix
    return c_matrix_local

#A function to calculate the individual values for the TMatrix
# Right now, only "approximation 2" is tested.  The other approximations will be for a
# future release.

def Tab(D, N, alpha, beta, B, G):
    total = 0.0

    idx_a = pyfghutil.PointToIndex(D, N, alpha)
    idx_b = pyfghutil.PointToIndex(D, N, beta)

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
                        pt = pyfghutil.IndexToPoint(D, N, idx)
                        val += B[r][idx_a[r], p] * B[r][p, idx_b[r]] * G[pt][r][r]
                else:
                    idx[s] = idx_b[s]
                    pt = pyfghutil.IndexToPoint(D, N, idx)
                    val = B[r][idx_a[r], idx_b[r]] * B[s][idx_a[s], idx_b[s]] * G[pt][r][s]

                total += val

    return (-0.5 * total)


def Tab_old(d, NValue, LValue, mu, c_matrix_insert, dimensionCounterArray, approximation, b_matrix_insert, GMat):
    #Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0
    #Total is return value
    def delta(x,y):
        if(x==y):
            return float(1)
        else:
            return float(0)

    total = 0.0
    if(approximation == 4):
        for T in range(d):
            #Check if the T counter is not equal to the index of the C value being tested, and if so it checks for if the dimension's corrosponding x and y values equal each other.
            Deltacounter = 0
            for Ccounter in range(d):
                if(Ccounter != T):
                    if(dimensionCounterArray[Ccounter*2] == dimensionCounterArray[(Ccounter*2)+1]):
                        Deltacounter += 1
                else:
                    pass
            #If deltacounter equals the dimensions - 1, add the formula to the total for that C value
            if (Deltacounter == (d-1)):
                    #print(dimensionCounterArray)
                    try:
                        total += (-1.0/2.0)*(GMat[T][T])*(c_matrix_insert[T][dimensionCounterArray[(T * 2) + 1], dimensionCounterArray[T * 2]])
                    except:
                        print("Trying to access: "+str(dimensionCounterArray[(T*2)+1])+", "+str(dimensionCounterArray[T*2]))
                        print(c_matrix_insert[T])
                        print("TAB error")
    elif(approximation == 3):
        #Perform all of the "C" calcuations first
        for C in range(d):
            Deltacounter = 0
            for Ccounter in range(d):
                if(Ccounter != C):
                    if(dimensionCounterArray[Ccounter*2] == dimensionCounterArray[(Ccounter*2)+1]):
                        Deltacounter += 1
            if(Deltacounter == d-1):
                total += float((GMat[C][C])) * (c_matrix_insert[C][dimensionCounterArray[(C*2)+1], dimensionCounterArray[C*2]])
        #Perform all of the "B" calculations second
        for B in range(d):
            if(dimensionCounterArray[B*2] == dimensionCounterArray[(B*2)+1]):
                temptotal = 1.0
                for BSecond in range(d):
                    if(BSecond != B):
                        temptotal *= b_matrix_insert[BSecond][dimensionCounterArray[(BSecond*2)+1], dimensionCounterArray[BSecond*2]]
                #This will be the first set of numbers and then the flipped ones
                GRange = [*range(d)]
                GRange.remove(B)
                Gx = min(GRange)
                Gy = max(GRange)
                total +=  float((GMat[Gx][Gy])) * temptotal * 2
        #Outside of summation multiplication of -hbar^2/2
        total *= (-1.0*1.0**2)/(2.0)
    elif(approximation == 2):
        t = int(dimensionCounterArray[0])
        j = int(dimensionCounterArray[1])
        u = int(dimensionCounterArray[2])
        k = int(dimensionCounterArray[3])
        v = int(dimensionCounterArray[4])
        l = int(dimensionCounterArray[5])
        #BMatrix calls are backwards
        #So BMatrix[0] would be B1, but it's actually B3
        sums = 0.0
        for p in range(NValue[0]):
            pt = pyfghutil.IndexToPoint(d,NValue,[p,k,l])
            sums += b_matrix_insert[2][j,p]*b_matrix_insert[2][p,t]*GMat[pt][0][0]
#            sums += b_matrix_insert[2][j, p] * b_matrix_insert[2][p, t] * GMat[p][k][l][0][0]
        total += -0.5*sums * delta(k,u) * delta(l,v)

        sums = 0.0
        for p in range(NValue[1]):
            pt = pyfghutil.IndexToPoint(d,NValue,[j,p,l])
            sums += b_matrix_insert[1][k,p]*b_matrix_insert[1][p,u]*GMat[pt][1][1]
#            sums += b_matrix_insert[1][k,p]*b_matrix_insert[1][p,u]*GMat[j][p][l][1][1]
        total += -0.5*sums*delta(j,t) * delta(l,v)

        sums = 0.0
        for p in range(NValue[2]):
            pt = pyfghutil.IndexToPoint(d,NValue,[j,k,p])
            sums += b_matrix_insert[0][l,p]*b_matrix_insert[0][p,v]*GMat[pt][2][2]
#            sums += b_matrix_insert[0][l, p] * b_matrix_insert[0][p, v] * GMat[j][k][p][2][2]
        total += -0.5*sums*delta(j,t)*delta(k,u)

        pt = pyfghutil.IndexToPoint(d,NValue,[t,k,l])
        total += -0.5*(b_matrix_insert[2][j,t]*b_matrix_insert[1][k,u]*GMat[pt][0][1]) * delta(v,l)
        total += -0.5*(b_matrix_insert[2][j,t]*b_matrix_insert[0][l,v]*GMat[pt][0][2]) * delta(k,u)

        pt = pyfghutil.IndexToPoint(d,NValue,[j,u,l])
        total += -0.5*(b_matrix_insert[1][k,u]*b_matrix_insert[2][j,t]*GMat[pt][1][0]) * delta(v,l)
        total += -0.5*(b_matrix_insert[1][k,u]*b_matrix_insert[0][l,v]*GMat[pt][1][2]) * delta(j,t)

        pt = pyfghutil.IndexToPoint(d,NValue,[j,k,v])
        total += -0.5*(b_matrix_insert[0][l,v]*b_matrix_insert[2][j,t]*GMat[pt][2][0]) * delta(k,u)
        total += -0.5*(b_matrix_insert[0][l,v]*b_matrix_insert[1][k,u]*GMat[pt][2][1]) * delta(j,t)

    else:
        print("This current approximation is incorrect or not supported: "+str(approximation))
        exit()

    return(total)

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
def TMatrixCalc(dataObject, GMatrix):
    #Establish variables needed
    NValue = dataObject.getNlist()
    LValue = dataObject.getLlist()
    D = dataObject.getD()

    #Create the TMatrix and the TFlagMatrix
    #The alpha and beta values are used to create the TMatrix in the correct position
    Npts = np.prod(NValue)
    tmatrix = lil_matrix((Npts,Npts), dtype=float)

    #Create the C_Matrix
#    c_matrix = []
#    for x in reversed(range(len(NValue))):
#        c_matrix.append(cmatrixgen(NValue[x], LValue[x]))

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
    p = mp.Pool(dataObject.cores_amount)
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




