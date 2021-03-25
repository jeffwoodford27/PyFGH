#Import the needed modules
import numpy as np
import scipy as scipy
import scipy.linalg
import math
import sys

#Remove the numpy print limits
np.set_printoptions(threshold=sys.maxsize)

#A function to calculate the BMatrix
def bmatrixgen(NValue, LValue):
    #Generate the BMatrix
    b_matrix_local = scipy.zeros((NValue, NValue), float)
    #Generate the difference matrix for the value calculations
    difb_matrix = scipy.zeros((NValue, 1), float)   
    scroll = 0
    for a in difb_matrix:
        for b in range((NValue-1)/2):
            difb_matrix[scroll] += ((b+1)*math.sin(( (b+1)*2*math.pi*scroll)/ NValue))
        scroll +=1
    #Use the dif_bmatrix to set the values of the BMatrix
    for y in range(NValue):
        for x in range(NValue):
            if (x-y) > 0:
                b_matrix[x, y] = (-1*difb_matrix[abs(x-y)])
            if (x-y) <= 0:
                b_matrix[x, y] = difb_matrix[abs(x-y)]
    return(b_matrix)

#A function to calculate the CMatrix
def cmatrixgen(NValue, LValue):
    #Generate the CMatrix
    c_matrix_local = scipy.zeros((NValue, NValue), float)
    #Calculate the similar values shared between x,y differences to improve efficiency
    difc_matrix = scipy.zeros((NValue, 1), float)
    for a in range(NValue):
        for b in range((NValue-1)/2):
            difc_matrix[a] += (((b+1)*(b+1))*math.cos(((b+1)*2*math.pi*a)/ NValue))
        difc_matrix[a] *= (-8.0*(math.pi*math.pi)/(float(NValue)*(float(LValue)*float(LValue))))
    #Push the difc_matrix values to their respective c_matrix spots
    for y in range(NValue):
        for x in range(NValue):
            c_matrix_local[x, y] = (difc_matrix[abs(x-y)])
    #Return the matrix
    return c_matrix_local


#A function to calculate the invidivdual values for the VMatrix
def Vab(d, NValue, LValue, KValue, deltax, dimensionCounterArray):
    #Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0
    #Total is the value returned for the calculation
    total = 0.0
    for Vcounter in range(d):
        #Add 1 to deltacounter if the corrosponding x and y values for the dimension equals each other
        if(dimensionCounterArray[Vcounter*2] == dimensionCounterArray[(Vcounter*2)+1]):
            Deltacounter += 1
        Vcounter += 1
    #If the deltacounter amount equals the amount of dimensions, perform a summation for the formula
    #Otherwise, the total will remain 0.0
    if (Deltacounter == d):
        for counter in range(d):
            xj = ((dimensionCounterArray[(counter*2)+1])*deltax)+(deltax/2.0)
            total += 0.5*KValue*(xj-(LValue*0.5))**2
    return(total)        

#A function to calculate the individual values for the TMatrix
def Tab(d, NValue, LValue, mu, c_matrix_insert, dimensionCounterArray):
    #Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0
    #Total is return value
    total = 0.0
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
                total += c_matrix_insert[dimensionCounterArray[(T*2)+1], dimensionCounterArray[T*2]]    
    return(total*((-1.0*1.0**2)/(2.0*mu)))        

#The function to calculate a TMatrix using the mol class from input
def TMatrixCalc(mol, D, VType):
    #Establish variables needed
    dimensions = D
    NValue = mol.N[0]
    LValue = mol.L[0]
    mu = mol.mu[0]
    deltax = (float(LValue)/float(NValue))
    #Create the array for the x dimensional counters
    dimensionCounterArray = scipy.zeros((dimensions*2,1), int)

    #Create the TMatrix and the TFlagMatrix
    #The alpha and beta values are used to create the TMatrix in the correct position
    tmatrix = scipy.zeros((NValue**dimensions, NValue**dimensions), float)
    tflag = scipy.zeros((NValue**dimensions, NValue**dimensions), int)
    alpha = 0
    beta = 0
    
    #Create the C_Matrix
    c_matrix = cmatrixgen(NValue, LValue)

    #Calculate the TMatrix
    for i in range((NValue**dimensions)*(NValue**dimensions)):
        #Counts X componenets of counterarray and multiplies it times N^(current dimension being used - 1) for alpha
        alpha = 0
        for a in reversed(range(len(dimensionCounterArray)/2)):
            alpha += dimensionCounterArray[(a*2)+1]*(NValue**(dimensions-(a+1)))
        #Counts Y componenets of counterarray and multiplies it times N^(current dimension being used - 1) for beta
        beta = 0
        for b in reversed(range(len(dimensionCounterArray)/2)):
            beta += dimensionCounterArray[(b*2)]*(NValue**(dimensions-(b+1)))    

        #Set the t matrix if the flag hasn't been set
        if tflag[alpha, beta] == 0:
            tmatrix[alpha, beta] = (Tab(dimensions, NValue, LValue, mu, c_matrix, dimensionCounterArray))
            tflag[alpha,beta] = 1
        if tflag[beta, alpha] == 0:
            tmatrix[beta, alpha] = (Tab(dimensions, NValue, LValue, mu, c_matrix, dimensionCounterArray))
            tflag[beta, alpha] = 1  

        #Adds +1 to the last dimension's X/Y value and checks to see if values need to add 1 to the next dimension counter / sets the current value to 0
        dimensionCounterArray[(dimensions*2)-1,0] += 1
        for c in reversed(range(len(dimensionCounterArray))):
            if (dimensionCounterArray[c]>= NValue):
                dimensionCounterArray[c] = 0
                dimensionCounterArray[c-1] += 1

    return tmatrix

#The function to calculate a VMatrix using the mol class from input
def VMatrixCalc(mol, D, VType):
    #Establish variables needed
    dimensions = D
    NValue = mol.N[0]
    LValue = mol.L[0]
    KValue = mol.Vmodel[0].k
    mu = mol.mu[0]
    deltax = (float(LValue)/float(NValue))
    #Create the array for the x dimensional counters
    dimensionCounterArray = scipy.zeros((dimensions*2,1), int)

    #Create the VMatrix
    #The alpha and beta values are used to create the VMatrix in the correct position
    vmatrix = scipy.zeros((NValue**dimensions, NValue**dimensions), float)
    alpha = 0
    beta = 0

    #Calculate the VMatrix
    for i in range((NValue**dimensions)*(NValue**dimensions)):
        #Counts X componenets of counterarray and multiplies it times N^(current dimension being used - 1) for alpha
        alpha = 0
        for a in reversed(range(len(dimensionCounterArray)/2)):
            alpha += dimensionCounterArray[(a*2)+1]*(NValue**(dimensions-(a+1)))
        #Counts Y componenets of counterarray and multiplies it times N^(current dimension being used - 1) for beta
        beta = 0
        for b in reversed(range(len(dimensionCounterArray)/2)):
            beta += dimensionCounterArray[(b*2)]*(NValue**(dimensions-(b+1)))    

        vmatrix[alpha, beta] =  (Vab(dimensions, NValue, LValue, KValue, deltax, dimensionCounterArray))

        #Adds +1 to the last dimension's X/Y value and checks to see if values need to add 1 to the next dimension counter / sets the current value to 0
        dimensionCounterArray[(dimensions*2)-1,0] += 1
        for c in reversed(range(len(dimensionCounterArray))):
            if (dimensionCounterArray[c]>= NValue):
                dimensionCounterArray[c] = 0
                dimensionCounterArray[c-1] += 1
    return vmatrix
