#Import the needed modules
import numpy as np
import scipy as scipy
import scipy.linalg
import pyfghutil
import math
import multiprocessing as mp
import sys



#A function to calculate the BMatrix
def bmatrixgen(NValue, LValue):
    '''
    #Generate the BMatrix
    b_matrix = np.zeros((NValue, NValue), float)
    #Generate the difference matrix for the value calculations
    difb_matrix = np.zeros((NValue, 1), float)
    for a in difb_matrix:
        for b in range(int((NValue-1)/2)):
            difb_matrix[int(a)] += ((b+1)*math.sin(( (b+1)*2.0*math.pi*int(a))/ NValue))
        difb_matrix[int(a)] *= (4.0*math.pi)/(LValue*NValue)
    #Use the dif_bmatrix to set the values of the BMatrix

    for y in range(NValue):
        for x in range(NValue):
            if (x-y) > 0:
                b_matrix[x, y] = (-1*difb_matrix[abs(x-y)])
            if (x-y) <= 0:
                b_matrix[x, y] = difb_matrix[abs(x-y)]
    '''
    n = int((NValue - 1)/2)
    b_matrix = np.zeros((NValue, NValue), float)
    for j in range(NValue):
        for l in range(NValue):
            for p in range(1, n+1):
                b_matrix[j][l] += float(p)*math.sin(2*math.pi*float(p)*float(l-j)/float(NValue))
            b_matrix[j][l] *= (4.0*math.pi)/(LValue*float(NValue))
    
    return(b_matrix)

#A function to calculate the CMatrix
def cmatrixgen(NValue, LValue):
    #Generate the CMatrix
    c_matrix_local = scipy.zeros((NValue, NValue), float)
    #Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = scipy.zeros((NValue, 1), float)
    for a in range(NValue):
        for b in range(int((NValue-1)/2)):
            difc_matrix[a] += (((b+1)*(b+1))*math.cos(((b+1)*2*math.pi*a)/ NValue))
        difc_matrix[a] *= (-8.0*(math.pi*math.pi)/(float(NValue)*(float(LValue)*float(LValue))))
    #Push the difc_matrix values to their respective c_matrix spots
    for y in range(NValue):
        for x in range(NValue):
            c_matrix_local[x, y] = (difc_matrix[abs(x-y)])
    #Return the matrix
    return c_matrix_local

#A function to calculate the individual values for the TMatrix
def Tab(d, NValue, LValue, mu, c_matrix_insert, dimensionCounterArray, approximation, b_matrix_insert = None, GMat = None):
    #Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0
    #Total is return value
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
                #print("Accessed GMat point "+str(C)+", "+str(C)+" with dimension counter array: "+str(dimensionCounterArray))
        #Perform all of the "B" calculations second
        for B in range(d):
            if(dimensionCounterArray[B*2] == dimensionCounterArray[(B*2)+1]):
                temptotal = 1.0
                for BSecond in range(d):
                    if(BSecond != B):
                        temptotal *= b_matrix_insert[BSecond][dimensionCounterArray[(BSecond*2)+1], dimensionCounterArray[BSecond*2]]
                        #print("BMatrix access: "+str(b_matrix_insert[BSecond][dimensionCounterArray[(BSecond*2)+1], dimensionCounterArray[BSecond*2]]))
                #This will be the first set of numbers and then the flipped ones
                GRange = [*range(d)]
                GRange.remove(B)
                Gx = min(GRange)
                Gy = max(GRange)
                total +=  float((GMat[Gx][Gy])) * temptotal * 2
                #print("Accessed GMat point "+str(Gx)+", "+str(Gy)+" with dimension counter array: "+str(dimensionCounterArray))
        #Outside of summation multiplication of -hbar^2/2
        total *= (-1.0*1.0**2)/(2.0)
    elif(approximation == 2):
        #Perform all of the "C" calcuations first
        for C in range(d):
            Deltacounter = 0
            for Ccounter in range(d):
                if(Ccounter != C):
                    if(dimensionCounterArray[Ccounter*2] == dimensionCounterArray[(Ccounter*2)+1]):
                        Deltacounter += 1
            if(Deltacounter == d-1):
                #print("This is what GMat lookup found at point "+str(dimensionCounterArray[1])+", "+str(dimensionCounterArray[3])+", "+str(dimensionCounterArray[5])+": "+str(GMat.getPoint(dimensionCounterArray[1],dimensionCounterArray[3],dimensionCounterArray[5])))
                point = float((GMat[C][C]))
                total += point * (c_matrix_insert[C][dimensionCounterArray[(C*2)+1], dimensionCounterArray[C*2]]) 
        #Perform all of the "B" calculations second
        for B in range(d):
            if(dimensionCounterArray[B*2] == dimensionCounterArray[(B*2)+1]):
                temptotal = 1.0
                for BSecond in range(d):
                    if(BSecond != B):
                        #DeltaConstant currently fills the deltaG / deltaq constant
                        deltaConst = 1  
                        temptotal *= b_matrix_insert[BSecond][dimensionCounterArray[(BSecond*2)+1], dimensionCounterArray[BSecond*2]] * deltaConst
                #This will be the first set of numbers and then the flipped ones     
                total +=  0 * temptotal * 2
        total *= (-1.0*1.0**2)/(2.0)




    else:
        print("This current approximation is incorrect or not supported: "+str(approximation))
        exit()                

    return(total)        
    #return(total*((-1.0*1.0**2)/(2.0*mu)))        

def TBlockCalc(dimensions, NValue, LValue, mu, c_matrix, approximation, blockX, blockY, b_matrix=None, gmatrix=None):
    #Blocks will be 0 index
    blockHolder = scipy.zeros((NValue[0], NValue[0]), float)
    #The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0+NValue[0]*blockX, NValue[0]+NValue[0]*blockX):
        for beta in range(0+NValue[0]*blockY, NValue[0]+NValue[0]*blockY):
            counter = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
            blockHolder[alpha0start, beta0start] = Tab(dimensions, NValue, LValue, mu, c_matrix, counter, approximation, b_matrix, gmatrix[alpha])
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

#The function to calculate a TMatrix using the mol class from input
def TMatrixCalc(params, D):
    dimensionCounterArray = scipy.zeros((D*2,1), int)
    NValue = params.N
    LValue = params.L
    if(params.Vtype == "Model"):
        mu = []
        for i in range(D):
            mu.append(params.Vmodel[i].getMu())
    else:
        mu = None
    Tapprox = params.Tapprox

    #Create the TMatrix and the TFlagMatrix
    #The alpha and beta values are used to create the TMatrix in the correct position
    tmatrix = scipy.zeros((np.prod(NValue), np.prod(NValue)), float)
    tflag = scipy.zeros((np.prod(NValue), np.prod(NValue)), int)
    alpha = 0
    beta = 0
    
    #Create the C_Matrix
    c_matrix = []
    for x in reversed(range(len(NValue))):
        c_matrix.append(cmatrixgen(NValue[x], LValue[x]))

    #Create the B_Matrix if necessary
    if(Tapprox < 4):
        b_matrix = []
        for x in reversed(range(len(NValue))):
            b_matrix.append(bmatrixgen(NValue[x], LValue[x]))
    else:
        b_matrix = None

    GMatrix = params.GMatrix

    blockCoords = []
    blocks = []
    paramz = []
    totalwidth = int(np.prod(NValue))
    repeatamount = int(totalwidth // NValue[0])
    #print(repeatamount)
    #print(NValue)
    #Don't optimize for now. Just calculate blocks as needed.
    for x in range(repeatamount):
        for y in range(repeatamount):
            blockCoords.append((x,y))
    if(Tapprox == 4):
        for coords in blockCoords:
            paramz.append((D, NValue, LValue, mu, c_matrix, Tapprox, coords[0], coords[1], None, GMatrix))
    elif(Tapprox < 4):
        for coords in blockCoords:
            paramz.append((D, NValue, LValue, mu, c_matrix, Tapprox, coords[0], coords[1], b_matrix, GMatrix))
    else:
        #Occurs when invalid or unsupported T Approximation is used
        pass 

    #Disable multi to find the error
    p = mp.Pool(16)
    print("Pool go T")
    blocks = p.starmap(TBlockCalc, paramz)
    print("Pool's done T")
    p.close()

    
    precalc = 0
    for i in range(len(blockCoords)):
        block = blocks[i]
        x = blockCoords[i][0]
        y = blockCoords[i][1]
        tmatrix[(0+NValue[precalc]*x):(NValue[precalc]+NValue[precalc]*x), (0+NValue[precalc]*y):(NValue[precalc]+NValue[precalc]*y)] = block
    
    
    return tmatrix
    


