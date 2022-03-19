# Import the needed modules
import numpy as np
import scipy as scipy
import scipy.linalg
from util import pyfghutil, DataObject
import math
import multiprocessing as mp
import sys
import pandas


# A function to calculate the BMatrix
def bmatrixgen(NValue, LValue):
    n = int((NValue - 1) / 2)
    b_matrix = np.zeros((NValue, NValue), float)
    for j in range(NValue):
        for l in range(NValue):
            for p in range(1, n + 1):
                b_matrix[j][l] += float(p) * math.sin(2 * math.pi * float(p) * float(l - j) / float(NValue))
            b_matrix[j][l] *= (4.0 * math.pi) / (LValue * float(NValue))

    return (b_matrix)


# A function to calculate the CMatrix
def cmatrixgen(NValue, LValue):
    # Generate the CMatrix
    c_matrix_local = scipy.zeros((NValue, NValue), float)
    # Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = scipy.zeros((NValue, 1), float)
    for a in range(NValue):
        for b in range(int((NValue - 1) / 2)):
            difc_matrix[a] += (((b + 1) * (b + 1)) * math.cos(((b + 1) * 2 * math.pi * a) / NValue))
        difc_matrix[a] *= (-8.0 * (math.pi * math.pi) / (float(NValue) * (float(LValue) * float(LValue))))
    # Push the difc_matrix values to their respective c_matrix spots
    for y in range(NValue):
        for x in range(NValue):
            c_matrix_local[x, y] = (difc_matrix[abs(x - y)])
    # Return the matrix
    return c_matrix_local


# A function to calculate the individual values for the TMatrix
def Tab(d, NValue, LValue, mu, c_matrix_insert, dimensionCounterArray, approximation, b_matrix_insert, GMat):
    # Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0

    # Total is return value
    def delta(x, y):
        if (x == y):
            return float(1)
        else:
            return float(0)

    total = 0.0
    if (approximation == 4):
        for T in range(d):
            # Check if the T counter is not equal to the index of the C value being tested, and if so it checks for if the dimension's corrosponding x and y values equal each other.
            Deltacounter = 0
            for Ccounter in range(d):
                if (Ccounter != T):
                    if (dimensionCounterArray[Ccounter * 2] == dimensionCounterArray[(Ccounter * 2) + 1]):
                        Deltacounter += 1
                else:
                    pass
            # If deltacounter equals the dimensions - 1, add the formula to the total for that C value
            if (Deltacounter == (d - 1)):
                # print(dimensionCounterArray)
                try:
                    total += (-1.0 / 2.0) * (GMat[T][T]) * (
                    c_matrix_insert[T][dimensionCounterArray[(T * 2) + 1], dimensionCounterArray[T * 2]])
                except:
                    print("Trying to access: " + str(dimensionCounterArray[(T * 2) + 1]) + ", " + str(
                        dimensionCounterArray[T * 2]))
                    print(c_matrix_insert[T])
                    print("TAB error")
    elif (approximation == 3):
        # Perform all of the "C" calcuations first
        for C in range(d):
            Deltacounter = 0
            for Ccounter in range(d):
                if (Ccounter != C):
                    if (dimensionCounterArray[Ccounter * 2] == dimensionCounterArray[(Ccounter * 2) + 1]):
                        Deltacounter += 1
            if (Deltacounter == d - 1):
                total += float((GMat[C][C])) * (
                c_matrix_insert[C][dimensionCounterArray[(C * 2) + 1], dimensionCounterArray[C * 2]])
                # Perform all of the "B" calculations second
        for B in range(d):
            if (dimensionCounterArray[B * 2] == dimensionCounterArray[(B * 2) + 1]):
                temptotal = 1.0
                for BSecond in range(d):
                    if (BSecond != B):
                        temptotal *= b_matrix_insert[BSecond][
                            dimensionCounterArray[(BSecond * 2) + 1], dimensionCounterArray[BSecond * 2]]
                # This will be the first set of numbers and then the flipped ones
                GRange = [*range(d)]
                GRange.remove(B)
                Gx = min(GRange)
                Gy = max(GRange)
                total += float((GMat[Gx][Gy])) * temptotal * 2
        # Outside of summation multiplication of -hbar^2/2
        total *= (-1.0 * 1.0 ** 2) / (2.0)
    elif (approximation == 2):
        t = int(dimensionCounterArray[0])
        j = int(dimensionCounterArray[1])
        u = int(dimensionCounterArray[2])
        k = int(dimensionCounterArray[3])
        v = int(dimensionCounterArray[4])
        l = int(dimensionCounterArray[5])
        # BMatrix calls are backwards
        # So BMatrix[0] would be B1, but it's actually B3
        sums = 0.0
        for p in range(NValue[0]):
            sums += b_matrix_insert[2][j, p] * b_matrix_insert[2][p, t] * GMat[p][k][l][0][0]
        total += -0.5 * sums * delta(k, u) * delta(l, v)

        sums = 0.0
        for p in range(NValue[1]):
            sums += b_matrix_insert[1][k, p] * b_matrix_insert[1][p, u] * GMat[j][p][l][1][1]
        total += -0.5 * sums * delta(j, t) * delta(l, v)

        sums = 0.0
        for p in range(NValue[2]):
            sums += b_matrix_insert[0][l, p] * b_matrix_insert[0][p, v] * GMat[j][k][p][2][2]
        total += -0.5 * sums * delta(j, t) * delta(k, u)

        total += -0.5 * (b_matrix_insert[2][j, t] * b_matrix_insert[1][k, u] * GMat[t][k][l][0][1]) * delta(v, l)
        total += -0.5 * (b_matrix_insert[2][j, t] * b_matrix_insert[0][l, v] * GMat[t][k][l][0][2]) * delta(k, u)
        total += -0.5 * (b_matrix_insert[1][k, u] * b_matrix_insert[2][j, t] * GMat[j][u][l][1][0]) * delta(v, l)
        total += -0.5 * (b_matrix_insert[1][k, u] * b_matrix_insert[0][l, v] * GMat[j][u][l][1][2]) * delta(j, t)
        total += -0.5 * (b_matrix_insert[0][l, v] * b_matrix_insert[2][j, t] * GMat[j][k][v][2][0]) * delta(k, u)
        total += -0.5 * (b_matrix_insert[0][l, v] * b_matrix_insert[1][k, u] * GMat[j][k][v][2][1]) * delta(j, t)



    else:
        print("This current approximation is incorrect or not supported: " + str(approximation))
        exit()

    return (total)
    # return(total*((-1.0*1.0**2)/(2.0*mu)))


def TBlockCalc(dimensions, NValue, LValue, mu, c_matrix, approximation, blockX, blockY, b_matrix, gmatrix):
    # Blocks will be 0 index
    blockHolder = scipy.zeros((NValue[0], NValue[0]), float)
    # The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0 + NValue[0] * blockX, NValue[0] + NValue[0] * blockX):
        for beta in range(0 + NValue[0] * blockY, NValue[0] + NValue[0] * blockY):
            counter = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
            if (approximation > 2):
                counter1 = int(counter[0])
                counter2 = int(counter[2])
                counter3 = int(counter[4])
                blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, LValue, mu, c_matrix, counter,
                                                           approximation, b_matrix,
                                                           gmatrix[counter1][counter2][counter3])
            else:
                blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, LValue, mu, c_matrix, counter,
                                                           approximation, b_matrix, gmatrix)
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder


# The function to calculate a TMatrix using the mol class from input
def TMatrixCalc(dataObject, GMatrix):
    # Establish variables needed
    NValue = []
    LValue = []
    if (int(dataObject.N1) > 0):
        NValue.append(int(dataObject.N1))
        LValue.append(float(dataObject.L1))
    if (int(dataObject.N2) > 0):
        NValue.append(int(dataObject.N2))
        LValue.append(float(dataObject.L2))
    if (int(dataObject.N3) > 0):
        NValue.append(int(dataObject.N3))
        LValue.append(float(dataObject.L3))
    D = len(NValue)
    pes = dataObject.PES
    dimensionCounterArray = scipy.zeros(D * 2, int)
    mu = []
    Tapprox = 2

    # Create the TMatrix and the TFlagMatrix
    # The alpha and beta values are used to create the TMatrix in the correct position
    tmatrix = scipy.zeros((np.prod(NValue), np.prod(NValue)), float)
    tflag = scipy.zeros((np.prod(NValue), np.prod(NValue)), int)
    alpha = 0
    beta = 0

    # Create the C_Matrix
    c_matrix = []
    for x in reversed(range(len(NValue))):
        c_matrix.append(cmatrixgen(NValue[x], LValue[x]))

    # Create the B_Matrix if necessary
    if (Tapprox < 4):
        b_matrix = []
        for x in reversed(range(len(NValue))):
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
            blockCoords.append((x, y))
    if (Tapprox == 4):
        for coords in blockCoords:
            paramz.append((D, NValue, LValue, mu, c_matrix, Tapprox, coords[0], coords[1], None, GMatrix))
    elif (Tapprox < 4):
        for coords in blockCoords:
            paramz.append((D, NValue, LValue, mu, c_matrix, Tapprox, coords[0], coords[1], b_matrix, GMatrix))
    else:
        # Occurs when invalid or unsupported T Approximation is used
        pass
    # Pool and run
    p = mp.Pool(dataObject.cores_amount)
    print("Pool go T")
    blocks = p.starmap(TBlockCalc, paramz)
    print("Pool's done T")
    p.close()

    precalc = 0
    for i in range(len(blockCoords)):
        block = blocks[i]
        x = blockCoords[i][0]
        y = blockCoords[i][1]
        tmatrix[(0 + NValue[precalc] * x):(NValue[precalc] + NValue[precalc] * x),
        (0 + NValue[precalc] * y):(NValue[precalc] + NValue[precalc] * y)] = block

    return tmatrix




