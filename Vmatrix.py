#Import the needed modules
import numpy as np
from util import pyfghutil
import math


class HarmonicOscillatorModel:
    def __init__(self,k):
        self.k = k

class MorseOscillatorModel:
    def __init__(self,De,a):
        self.De = De
        self.a = a

class Molecule:
    def __init__(self, D, N, L, mu, Vtype, Vmodel):
        self.N = N
        self.L = L
        self.mu = mu
        self.Vtype = Vtype
        self.Vmodel = Vmodel




#A function to calculate the invidivdual values for the VMatrix
def Vab(d, NValue, LValue, VModel, VType, deltax, dimensionCounterArray):
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
            realdeltax = (float(LValue[(d-1)-counter])/float(NValue[(d-1)-counter]))
            if(VType[counter] == 0):
                xj = ((dimensionCounterArray[(counter*2)+1])*realdeltax)+(realdeltax/2.0)
                total += 0.5*VModel[(d-1)-counter].k*(xj-(LValue[(d-1)-counter]*0.5))**2
            elif(VType[counter] == 1):
                xj = ((dimensionCounterArray[(counter*2)+1])*realdeltax)+(realdeltax/2.0)
                #total += De*(1-math.exp(-a*xj))**2
                total += (VModel[(d-1)-counter].De)*((1.0-math.exp(-(VModel[(d-1)-counter].a)*(xj-(LValue[(d-1)-counter]*0.5))))**2.0)
            else:
                pass
                #This should never happen
    return(total)        

#The function to calculate a VMatrix using the mol class from input
def VMatrixCalc(mol, D):
    #Establish variables needed
    dimensions = D
    NValue = mol.N
    LValue = mol.L
    VModel = mol.Vmodel
    VType = mol.Vtype
    #Reference a mol.Vmodel[0].k
    mu = mol.mu
    #deltax = (float(LValue)/float(NValue))
    #Create the array for the x dimensional counters
    dimensionCounterArray = np.zeros((dimensions*2,1), int)

    #Create the VMatrix
    #The alpha and beta values are used to create the VMatrix in the correct position
    vmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)

    #Calculate the VMatrix
    for i in range((np.prod(NValue))*(np.prod(NValue))):
        alpha = pyfghutil.AlphaCalc(dimensions, dimensionCounterArray, NValue)
        beta = pyfghutil.BetaCalc(dimensions, dimensionCounterArray, NValue)  

        vmatrix[alpha, beta] = (Vab(dimensions, NValue, LValue, VModel, VType, 0, dimensionCounterArray))

        #Adds +1 to the last dimension's X/Y value and checks to see if values need to add 1 to the next dimension counter / sets the current value to 0
        dimensionCounterArray = pyfghutil.DCAAdvance(dimensions, dimensionCounterArray, NValue)
    return vmatrix




D = 1
N = [5]
L = [3]
mu = [919]
Vtype = [0]
Vmodel = [HarmonicOscillatorModel(0.37)]

mol = Molecule(D, N, L, mu, Vtype, Vmodel)
print(VMatrixCalc(mol,D))