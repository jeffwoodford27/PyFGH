import pyfghutil
import numpy as np

def Vab(d, NValue, LValue, VType, VModel, pes, dimensionCounterArray):
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
        if (VType == "Model"):
            for counter in range(d):
                realdeltax = (float(LValue[(d-1)-counter])/float(NValue[(d-1)-counter]))
                xj = ((dimensionCounterArray[(counter*2)+1])*realdeltax)+(realdeltax/2.0)
                xj = xj - (LValue[(d-1)-counter])/2.0
                total += VModel[(d-1)-counter].calcPotentialEnergy(xj)
        if (VType == "File"):
            total += pes.getPointByN(dimensionCounterArray[1][0],dimensionCounterArray[3][0],dimensionCounterArray[5][0]).getEnergy()
    return(total)

def VMatrixCalc(params, D):
    #Establish variables needed
    dimensions = D
    NValue = params.N
    LValue = params.L
    VType = params.Vtype
    VModel = params.Vmodel
    pes = params.PES


    #Create the array for the x dimensional counters
    dimensionCounterArray = np.zeros((dimensions*2,1), int)

    #Create the VMatrix
    #The alpha and beta values are used to create the VMatrix in the correct position
    vmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)

    #Calculate the VMatrix
    for i in range((np.prod(NValue))*(np.prod(NValue))):
        alpha = pyfghutil.AlphaCalc(dimensions, dimensionCounterArray, NValue)
        beta = pyfghutil.BetaCalc(dimensions, dimensionCounterArray, NValue)

        vmatrix[alpha, beta] = (Vab(dimensions, NValue, LValue, VType, VModel, pes, dimensionCounterArray))

        #Adds +1 to the last dimension's X/Y value and checks to see if values need to add 1 to the next dimension counter / sets the current value to 0
        dimensionCounterArray = pyfghutil.DCAAdvance(dimensions, dimensionCounterArray, NValue)
    return vmatrix
