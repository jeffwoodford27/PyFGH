import pyfghutil
import numpy as np
import math

def bmatrixgen(NValue, LValue):
    #Generate the BMatrix
    b_matrix = np.zeros((NValue, NValue), float)
    #Generate the difference matrix for the value calculations
    difb_matrix = np.zeros((NValue, 1), float)
    scroll = 0
    for a in difb_matrix:
        for b in range(int((NValue-1)/2)):
            difb_matrix[scroll] += ((b+1)*math.sin(( (b+1)*2*math.pi*scroll)/ NValue))
        scroll +=1
    #Use the dif_bmatrix to set the values of the BMatrix
    for y in range(NValue):
        for x in range(NValue):
            if (x-y) > 0:
                b_matrix[x, y] = (-1*difb_matrix[abs(x-y)])
            if (x-y) <= 0:
                b_matrix[x, y] = difb_matrix[abs(x-y)]
            b_matrix[x,y] = b_matrix[x,y] * (4.0*math.pi)/(float(NValue)*LValue)
    return(b_matrix)

def cmatrixgen(NValue, LValue):
    #Generate the CMatrix
    c_matrix_local = np.zeros((NValue, NValue), float)
    #Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = np.zeros((NValue, 1), float)
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

def Tab(d, mu, GMatrix, c_matrix_insert, dimensionCounterArray):
    # Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    # Total is return value
    total = 0.0
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
                total += (-1.0/2.0)*(GMatrix[T][T])*(c_matrix_insert[T][dimensionCounterArray[(T * 2) + 1], dimensionCounterArray[T * 2]])
            except:
                print("Trying to access: " + str(dimensionCounterArray[(T * 2) + 1]) + ", " + str(dimensionCounterArray[T * 2]))
                print(c_matrix_insert[T])
                print("TAB error")

    return (total)
    # return(total*((-1.0*1.0**2)/(2.0*mu)))

# The function to calculate a TMatrix using the mol class from input
def TMatrixCalc(params, D):
    # Establish variables needed
    dimensions = D
    NValue = params.N
    LValue = params.L

    if(params.Vtype == "Model"):
        mu = np.zeros(D,float)
        for i in range(D):
            mu[i] = params.Vmodel[i].getMu()
    else:
        mu = None

    if(params.Vtype == "File"):
        GMatrix = params.GMatrix
    else:
        GMatrix = None

    # Move deltax to functions that need it
    # deltax = (float(LValue)/float(NValue))
    # Create the array for the x dimensional counters
    dimensionCounterArray = np.zeros((dimensions * 2, 1), int)

    # Create the TMatrix and the TFlagMatrix
    # The alpha and beta values are used to create the TMatrix in the correct position
    tmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)
    tflag = np.zeros((np.prod(NValue), np.prod(NValue)), int)

    # Create the C_Matrix
    c_matrix = []
    for x in reversed(range(len(NValue))):
        # c_matrix.append(cmatrixgen(NValue[(dimensions-1)-x], LValue[(dimensions-1)-x]))
        c_matrix.append(cmatrixgen(NValue[x], LValue[x]))

    if (params.Tapprox < 4):
        # Create the B Matrix
        b_matrix = []
        for x in reversed(range(len(NValue))):
            b_matrix.append(bmatrixgen(NValue[x], LValue[x]))
    else:
        b_matrix = None

    # Calculate the TMatrix
    for i in range((np.prod(NValue)) * (np.prod(NValue))):
        # Counts X componenets of counterarray and multiplies it times N^(current dimension being used - 1) for alpha
        alpha = pyfghutil.AlphaCalc(dimensions, dimensionCounterArray, NValue)
        beta = pyfghutil.BetaCalc(dimensions, dimensionCounterArray, NValue)

        #print("Alpha: "+str(alpha)+" Beta:"+str(beta))
        #print(dimensionCounterArray)
        # Set the t matrix if the flag hasn't been set
        if tflag[alpha, beta] == 0:
            tmatrix[alpha, beta] = (Tab(dimensions, mu, GMatrix[alpha[0]], c_matrix, dimensionCounterArray))
            tflag[alpha, beta] = 1
        if tflag[beta, alpha] == 0:
            tmatrix[beta, alpha] = (Tab(dimensions, mu, GMatrix[alpha[0]], c_matrix, dimensionCounterArray))
            tflag[beta, alpha] = 1

            # Adds +1 to the last dimension's X/Y value and checks to see if values need to add 1 to the next dimension counter / sets the current value to 0
        dimensionCounterArray = pyfghutil.DCAAdvance(dimensions, dimensionCounterArray, NValue)

    return tmatrix
