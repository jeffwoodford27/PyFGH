#Import the needed modules
import numpy as np
from util import pyfghutil
import math
import multiprocessing as mp
import sys
import pandas


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

class NBlock:
    def __init__(self, D, NValues):
        self.D = D
        self.N = NValues[D-1]
        self.SmallestN = NValues[0]
        self.NProd = np.prod(NValues[:D-1])
        self.diagblocks = []
        self.difblocks = []
        self.xboffset = 0
        self.yboffset = 0
        #print(NValues)
        #print("D and NProd"+str(self.D)+" "+str(self.NProd))
        #print("Smallest N:"+str(self.SmallestN))
        #We assume that blocks is an (Nx+1)^2 grid for blocks below it
        #Shape is (y, x) of the array
        #NDarray uses [y,x] accessing
        #NProd will be the amount of items in alpha/beta it encompases for a block
        if(self.D > 1):
            self.diagblocks = [None]*self.N
            self.difblocks = [None]*(self.N-1)
            for x in range(self.N):
                self.diagblocks[x] = NBlock(D-1, NValues)
                    
            for y in range(self.N-1):
                self.difblocks[y] = NBlock(D-1, NValues)
                
        else:
            self.difblocks = np.zeros((self.N, self.N), float)
    def difSetup(self):
        if(self.D>1):
            for x in range(self.N):
                self.diagblocks[x].xboffset = self.xboffset + int(x * (self.NProd/self.SmallestN))
                self.diagblocks[x].yboffset = self.yboffset + int(x * (self.NProd/self.SmallestN))
                self.diagblocks[x].difSetup()
                #print("Setting diag block: "+str(self.D-1)+" with xboffset "+str(self.xboffset + int(x * (self.NProd/self.SmallestN))))
                #print("Setting diag block: "+str(self.D-1)+" with yboffset "+str(self.yboffset + int(x * (self.NProd/self.SmallestN))))
                        
            for y in range(self.N-1):
                self.difblocks[y].xboffset = self.xboffset + 0
                self.difblocks[y].yboffset = self.yboffset + 1+int(y * (self.NProd/self.SmallestN))
                self.difblocks[y].difSetup()
                #print("Setting diag block: "+str(self.D-1)+" with xboffset "+str(self.xboffset))
                #print("Setting diag block: "+str(self.D-1)+" with yboffset "+str(self.yboffset + 1+int(y * (self.NProd/self.SmallestN))))
                
    def coordGen(self):
        if(self.D>1):
            coords = []
            for x in range(len(self.diagblocks)):
                coords += self.diagblocks[x].coordGen()
            for y in range(len(self.difblocks)):
                coords += self.difblocks[y].coordGen()
            return(coords)
        elif(self.D == 1):
            return([(self.xboffset, self.yboffset)])
            
    def print1x1(self):
        if(self.D != 1):
            '''
            print("Print dimension class "+str(self.D-1)+" with N "+str(self.blocks[0,0].N)+"and with nprod "+str(self.blocks[0,0].NProd))
            print(self.blocks[0,0].blocks)
            self.blocks[0,0].print1x1()
            '''
        else:
            pass
    def accessPoint(self, alpha, beta):
        if(self.D > 1):
            return(self.blocks[beta//self.NProd, alpha//self.NProd].accessPoint(beta%self.NProd, alpha%self.NProd))
        else:
            return(self.blocks[alpha, beta])
    def setBlock(self, N1BlockX, N1BlockY, blockData, startFlag=True):
        if(startFlag):
            if(self.D > 1):
                xb = (N1BlockX*self.SmallestN)//self.NProd
                yb = (N1BlockY*self.SmallestN)//self.NProd
                #print("Set block (D,xb,yb): "+str(self.D)+", "+str(xb)+", "+str(yb))
                if(xb == yb):
                    self.diagblocks[xb].setBlock((N1BlockX*self.SmallestN)%self.NProd, (N1BlockY*self.SmallestN)%self.NProd, blockData, False)
                else:
                    xydif = abs(xb-yb)
                    self.difblocks[xydif-1].setBlock((N1BlockX*self.SmallestN)%self.NProd, (N1BlockY*self.SmallestN)%self.NProd, blockData, False)
            else:
                self.difblocks = blockData
        else:
            if(self.D > 1):
                xb = N1BlockX//self.NProd
                yb = N1BlockY//self.NProd
                #print("Set block (D,xb,yb): "+str(self.D)+", "+str(xb)+", "+str(yb))
                if(xb == yb):
                    self.diagblocks[xb].setBlock(N1BlockX%self.NProd, N1BlockY%self.NProd, blockData, False)
                else:
                    xydif = abs(xb-yb)
                    self.difblocks[xydif-1].setBlock(N1BlockX%self.NProd, N1BlockY%self.NProd, blockData, False)
            else:
                self.difblocks = blockData
    def readBlock(self, N1BlockX, N1BlockY, startFlag=True):
        if(startFlag):
            if(self.D > 1):
                xb = (N1BlockX*self.SmallestN)//self.NProd
                yb = (N1BlockY*self.SmallestN)//self.NProd
                if(xb == yb):
                    return(self.diagblocks[xb].readBlock((N1BlockX*self.SmallestN)%self.NProd, (N1BlockY*self.SmallestN)%self.NProd, False))
                else:
                    xydif = abs(xb-yb)
                    return(self.difblocks[xydif-1].readBlock((N1BlockX*self.SmallestN)%self.NProd, (N1BlockY*self.SmallestN)%self.NProd, False))
            else:
                return(self.difblocks)
        else:
            if(self.D > 1):
                xb = N1BlockX//self.NProd
                yb = N1BlockY//self.NProd
                if(xb == yb):
                    return(self.diagblocks[xb].readBlock(N1BlockX%self.NProd, N1BlockY%self.NProd, False))
                else:
                    xydif = abs(xb-yb)
                    return(self.difblocks[xydif-1].readBlock(N1BlockX%self.NProd, N1BlockY%self.NProd, False))
            else:
                return(self.difblocks)




#A function to calculate the invidivdual values for the VMatrix
def Vab(d, NValue, LValue, VType, VModel, deltax, dimensionCounterArray):
    #Deltacounter is used to makes sure that the value being calculated is in the diagonal of the matrix
    Deltacounter = 0
    #Total is the value returned for the calculation
    total = 0.0
    for Vcounter in range(d):
        #Add 1 to deltacounter if the corrosponding x and y values for the dimension equals each other
        if(dimensionCounterArray[Vcounter*2] == dimensionCounterArray[(Vcounter*2)+1]):
            Deltacounter += 1
    #If the deltacounter amount equals the amount of dimensions, perform a summation for the formula
    #Otherwise, the total will remain 0.0 
    if (Deltacounter == d):
        for counter in range(d):
            realdeltax = (float(LValue[(d-1)-counter])/float(NValue[(d-1)-counter]))
            if(VType[counter] == 0):
                xj = ((dimensionCounterArray[(counter*2)+1])*realdeltax)+(realdeltax/2.0)
                total += 0.5*VModel[(d-1)-counter][1]*(xj-(LValue[(d-1)-counter]*0.5))**2
            elif(VType[counter] == 1):
                xj = ((dimensionCounterArray[(counter*2)+1])*realdeltax)+(realdeltax/2.0)
                #total += De*(1-math.exp(-a*xj))**2
                total += (VModel[(d-1)-counter][1])*((1.0-math.exp(-(VModel[(d-1)-counter][2])*(xj-(LValue[(d-1)-counter]*0.5))))**2.0)
            else:
                pass
                #This should never happen
        
    return(total)        

def VBlockCalc(dimensions, NValue, LValue, VType, VModel, blockX, blockY):
    #Blocks will be 0 index
    blockHolder = np.zeros((NValue[0], NValue[0]), float)
    #The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0+NValue[0]*blockX, NValue[0]+NValue[0]*blockX):
        for beta in range(0+NValue[0]*blockY, NValue[0]+NValue[0]*blockY):
            counter = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
            blockHolder[alpha0start, beta0start] = (Vab(dimensions, NValue, LValue, VType, VModel, 0, counter))
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

#The function to calculate a VMatrix using the DataObject class input
def VMatrixCalc(dataObj):
    #Establish variables needed
    NValue = []
    LValue = []
    #Create the NValue and LValue list from scratch:
    if int(dataObj.holdData.N1) > 0:
        NValue.append(int(dataObj.holdData.N1))
        LValue.append(float(dataObj.holdData.L1))
    if int(dataObj.holdData.N2) > 0:
        NValue.append(int(dataObj.holdData.N2))
        LValue.append(float(dataObj.holdData.L2))
    if int(dataObj.holdData.N3) > 0:
        NValue.append(int(dataObj.holdData.N3))
        LValue.append(float(dataObj.holdData.L3))
    
    dimensions = len(NValue)
    VType = []
    VModel = []
    for VModelClass in dataObj.holdData.model_data:
        VType.append(VModelClass.type)
        VModel.append(VModelClass.param)

    '''
    VType = []
    for VTypeString in dataObj.holdData.v:
        if (VTypeString == "Harmonic Oscillator"):
            VType.append(0)
        elif (VTypeString == "Morse Oscillator"):
            VType.append(1)
        else:
            VType.append(2)
    
    VType = mol.Vtype
    '''
    #Create the array for the x dimensional counters

    #This will be configured to work with 2D only at the moment
    
    dimensionCounterArray = np.zeros((dimensions*2,1), int)

    #Create the VMatrix
    #The alpha and beta values are used to create the VMatrix in the correct position
    vmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)

    #NBlock Class System
    NBlocks = NBlock(dimensions, NValue)
    NBlocks.difSetup()
    print(NBlocks.D)
    print(NBlocks.N)
    print(NBlocks.diagblocks)
    print(NBlocks.difblocks)
    print(NBlocks.NProd)
    '''
    NBlocks.print1x1()
    
    print("Try to access")
    print(NBlocks.accessPoint(37, 20))
    '''

    #If using model or file
    if(False):
        #Calculate by blocks:
        #Don't optimize for now. Just calculate blocks as needed.
        blockCoords = []
        optBlockCoords = []
        blocks = []
        paramz = []
        totalwidth = int(np.prod(NValue))
        repeatamount = int(totalwidth // NValue[0])
        #print(NValue)
        for x in range(repeatamount):
            for y in range(repeatamount):
                blockCoords.append((x,y))
        optBlockCoords = NBlocks.coordGen()
        #print(optBlockCoords)
        for coords in optBlockCoords:
            paramz.append((dimensions, NValue, LValue, VType, VModel, coords[0], coords[1]))
        
        p = mp.Pool(16)
        print("Pool go V")
        blocks = p.starmap(VBlockCalc, paramz)
        print("Pool's done V")
        p.close()
    
        precalc = 0
        for i in range(len(optBlockCoords)):
            block = blocks[i]
            x = optBlockCoords[i][0]
            y = optBlockCoords[i][1]
            NBlocks.setBlock(x, y, block)
        for i in range(len(blockCoords)):
            x = blockCoords[i][0]
            y = blockCoords[i][1]
            vmatrix[(0+NValue[precalc]*x):(NValue[precalc]+NValue[precalc]*x), (0+NValue[precalc]*y):(NValue[precalc]+NValue[precalc]*y)] = NBlocks.readBlock(x,y)
    else:
        #Using file
        potentialfile = pandas.read_csv("waterpot-data.csv", names=['q1', 'q2', 'q3', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'v'])
        countamount = int(np.prod(NValue))
        potentialfilepreview = np.zeros((countamount, countamount), float)
        for alpha in range(countamount):
            for beta in range(countamount):
                counterArray = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
                deltas = 0
                for coordPair in range(dimensions):
                    if(counterArray[coordPair*2] == counterArray[coordPair*2 + 1]):
                        deltas += 1
                if(deltas == dimensions):
                    vmatrix[alpha][beta] = potentialfile['v'][alpha]
                    potentialfilepreview[alpha][beta] = potentialfile['v'][alpha]
                #print("\n\n"+str(counterArray)+" alpha value "+str(alpha)+" beta value "+str(beta)+ " and value "+ str(potentialfile['v'][alpha]))
        pandas.DataFrame(potentialfilepreview).to_csv("alphabetapreview.csv")
    
    return vmatrix

    
    #Calculate the VMatrix for alpha and beta loop test
    '''
    for alpha in range(np.prod(NValue)):
        for beta in range(np.prod(NValue)):
            dimensionCounterArray = pyfghutil.AlphaAndBetaToCounter(alpha, beta, D, NValue)
            vmatrix[alpha, beta] = (Vab(dimensions, NValue, LValue, VModel, VType, 0, dimensionCounterArray))
    return vmatrix
    '''
    



'''
D = 1
N = [5]
L = [3]
mu = [919]
Vtype = [0]
Vmodel = [HarmonicOscillatorModel(0.37)]

mol = Molecule(D, N, L, mu, Vtype, Vmodel)
print(VMatrixCalc(mol,D))
'''
