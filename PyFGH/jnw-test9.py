#Import the needed modules
import numpy as np
from util import pyfghutil
from util import DataObject
import multiprocessing as mp
import csv

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
            if (blockX == 0 and blockY == 10):
                print(counter)
            blockHolder[alpha0start, beta0start] = (Vab(dimensions, NValue, LValue, 0, pes, counter))
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder

#The function to calculate a VMatrix using the DataObject class input
def VMatrixCalc(dataObject):
    #Establish variables needed
    NValue = []
    LValue = []
    if(int(dataObject.N1) > 0):
        NValue.append(int(dataObject.N1))
        LValue.append(float(dataObject.L1))
    if(int(dataObject.N2) > 0):
        NValue.append(int(dataObject.N2))
        LValue.append(float(dataObject.L2))
    if(int(dataObject.N3) > 0):
        NValue.append(int(dataObject.N3))
        LValue.append(float(dataObject.L3))

    dimensions = len(NValue)
    pes = dataObject.PES

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

            if (x == 0 and y == 10):
                print(pyfghutil.PointToIndex(dimensions, NValue, x))
                print(pyfghutil.PointToIndex(dimensions, NValue, y))

    optBlockCoords = NBlocks.coordGen()
    print(optBlockCoords)
    print(len(optBlockCoords))
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

if __name__ == '__main__':
    D = 3
    inp = DataObject.InputData()
    inp.setN1(11)
    inp.setN2(11)
    inp.setN3(11)
    inp.setL1(1.1)
    inp.setL2(1.1)
    inp.setL3(1.65)
    inp.setequilibrium_file("./testing files/water-equil.csv")
    inp.setpotential_energy("./testing files/water-potential.csv")

    Nat = 3
    equil = pyfghutil.Molecule()
    with open(inp.equilibrium_file, newline='') as csvfile:
        eqfile = csv.reader(csvfile)
        A = np.empty(Nat, dtype=int)
        Z = np.empty(Nat, dtype=int)
        x = np.empty(Nat, dtype=float)
        y = np.empty(Nat, dtype=float)
        z = np.empty(Nat, dtype=float)
        m = np.empty(Nat, dtype=float)
        n = 0
        for row in eqfile:
            for key, value in pyfghutil.AtomicSymbolLookup.items():
                if (value == row[0]):
                    Z[n] = key
                    break
            A[n] = int(row[1])
            x[n] = float(row[2])
            y[n] = float(row[3])
            z[n] = float(row[4])
            nucl = row[0] + "-" + row[1]
            m[n] = pyfghutil.MassLookup.get(nucl) * 1822.89
            n = n + 1

    equil.setXList(x)
    equil.setYList(y)
    equil.setZList(z)
    equil.setAtomicNoList(Z)
    equil.setMassNoList(A)
    equil.setMassList(m)

    N = np.zeros(D,dtype=int)
    N[0] = inp.getN1()
    N[1] = inp.getN2()
    N[2] = inp.getN3()
    Npts = np.prod(N)

    pes = pyfghutil.PotentialEnergySurface()
    pes.setN(N)
    with open(inp.potential_energy_file, newline='') as csvfile:
        pesfile = csv.reader(csvfile)

        n = 0
        for row in pesfile:
            pespt = pyfghutil.PESpoint()
            pespt.setN(n)

            q = np.zeros(D, dtype=float)
            q[0] = float(row[0])
            q[1] = float(row[1])
            q[2] = float(row[2])
            pespt.setQList(q)

            x = np.zeros(Nat, dtype=float)
            y = np.zeros(Nat, dtype=float)
            z = np.zeros(Nat, dtype=float)

            x[0] = float(row[3])
            y[0] = float(row[4])
            x[1] = float(row[5])
            y[1] = float(row[6])
            x[2] = float(row[7])
            y[2] = float(row[8])
            pespt.setXList(x)
            pespt.setYList(y)
            pespt.setZList(z)

            pespt.setEnergy(float(row[9]))

            pes.appendPESpt(pespt)
            n = n + 1

    pes.setNpts(n)
    inp.setPES(pes)

for p in range(pes.getNpts()):
    print(p)
    idx = pyfghutil.PointToIndex(D, N, p)
    print(idx)
    print(pes.getPointByPt(p).getN())
    print(pes.getPointByIdx(idx).getN())
    print(pes.getPointByPt(p).getQList())


#    V = VMatrixCalc(inp)
#    print(V)
