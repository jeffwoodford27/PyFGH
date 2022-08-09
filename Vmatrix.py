#Import the needed modules
import numpy as np
from util import pyfghutil
import multiprocessing as mp

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

            for y in range(self.N-1):
                self.difblocks[y].xboffset = self.xboffset + 0
                self.difblocks[y].yboffset = self.yboffset + 1+int(y * (self.NProd/self.SmallestN))
                self.difblocks[y].difSetup()

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
            blank = 0
            #Nothing
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
def Vab(d, NValue, LValue, deltax, pes, dimensionCounterArray):
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
        total += pes.getPointByN(int(dimensionCounterArray[1]),int(dimensionCounterArray[3]),int(dimensionCounterArray[5])).getEnergy()

    return(total)

def VBlockCalc(dimensions, NValue, LValue, pes, blockX, blockY):
    #Blocks will be 0 index
    blockHolder = np.zeros((NValue[0], NValue[0]), float)
    #The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0+NValue[0]*blockX, NValue[0]+NValue[0]*blockX):
        for beta in range(0+NValue[0]*blockY, NValue[0]+NValue[0]*blockY):
            counter = pyfghutil.AlphaAndBetaToCounter(alpha, beta, dimensions, NValue)
            blockHolder[alpha0start, beta0start] = (Vab(dimensions, NValue, LValue, 0, pes, counter))
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

#The function to calculate a VMatrix using the DataObject class input
def VMatrixCalc(dataObject):
    #Establish variables needed
    NValue = dataObject.getNlist()
    LValue = dataObject.getLlist()

    dimensions = dataObject.getD()
    pes = dataObject.getPES()

    dimensionCounterArray = np.zeros((dimensions*2,1), int)

    #Create the VMatrix
    #The alpha and beta values are used to create the VMatrix in the correct position
    vmatrix = np.zeros((np.prod(NValue), np.prod(NValue)), float)

    #NBlock Class System
    NBlocks = NBlock(dimensions, NValue)
    NBlocks.difSetup()


    #Calculate by blocks:
    #Don't optimize for now. Just calculate blocks as needed.
    blockCoords = []
    optBlockCoords = []
    blocks = []
    paramz = []
    totalwidth = int(np.prod(NValue))
    repeatamount = int(totalwidth // NValue[0])
    for x in range(repeatamount):
        for y in range(repeatamount):
            blockCoords.append((x,y))
    optBlockCoords = NBlocks.coordGen()
    for coords in optBlockCoords:
        paramz.append((dimensions, NValue, LValue, pes, coords[0], coords[1]))

    #Pool and run
    p = mp.Pool(dataObject.cores_amount)
    #print("Pool go V")
    blocks = p.starmap(VBlockCalc, paramz)
    #print("Pool's done V")
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

    return vmatrix
