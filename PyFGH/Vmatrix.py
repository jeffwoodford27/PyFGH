# Import the needed modules
import numpy as np
from PyFGH.util import pyfghutil as pyfghutil
import multiprocessing as mp
from scipy.sparse import lil_matrix


class NBlock:
    def __init__(self, D, NValues):
        self.D = D
        self.N = NValues[D - 1]
        self.SmallestN = NValues[0]
        self.NProd = np.prod(NValues[:D - 1])
        self.diagblocks = []
        self.difblocks = []
        self.xboffset = 0
        self.yboffset = 0
        if (self.D > 1):
            self.diagblocks = [None] * self.N
            self.difblocks = [None] * (self.N - 1)
            for x in range(self.N):
                self.diagblocks[x] = NBlock(D - 1, NValues)

            for y in range(self.N - 1):
                self.difblocks[y] = NBlock(D - 1, NValues)

        else:
            self.difblocks = np.zeros((self.N, self.N), float)

    def difSetup(self):
        if (self.D > 1):
            for x in range(self.N):
                self.diagblocks[x].xboffset = self.xboffset + int(x * (self.NProd / self.SmallestN))
                self.diagblocks[x].yboffset = self.yboffset + int(x * (self.NProd / self.SmallestN))
                self.diagblocks[x].difSetup()

            for y in range(self.N - 1):
                self.difblocks[y].xboffset = self.xboffset + 0
                self.difblocks[y].yboffset = self.yboffset + 1 + int(y * (self.NProd / self.SmallestN))
                self.difblocks[y].difSetup()

    def coordGen(self):
        if (self.D > 1):
            coords = []
            for x in range(len(self.diagblocks)):
                coords += self.diagblocks[x].coordGen()
            for y in range(len(self.difblocks)):
                coords += self.difblocks[y].coordGen()
            return (coords)
        elif (self.D == 1):
            return ([(self.xboffset, self.yboffset)])

    def print1x1(self):
        if (self.D != 1):
            blank = 0
            # Nothing
        else:
            pass

    def accessPoint(self, alpha, beta):
        if (self.D > 1):
            return (
                self.blocks[beta // self.NProd, alpha // self.NProd].accessPoint(beta % self.NProd, alpha % self.NProd))
        else:
            return (self.blocks[alpha, beta])

    def setBlock(self, N1BlockX, N1BlockY, blockData, startFlag=True):
        if (startFlag):
            if (self.D > 1):
                xb = (N1BlockX * self.SmallestN) // self.NProd
                yb = (N1BlockY * self.SmallestN) // self.NProd
                # print("Set block (D,xb,yb): "+str(self.D)+", "+str(xb)+", "+str(yb))
                if (xb == yb):
                    self.diagblocks[xb].setBlock((N1BlockX * self.SmallestN) % self.NProd,
                                                 (N1BlockY * self.SmallestN) % self.NProd, blockData, False)
                else:
                    xydif = abs(xb - yb)
                    self.difblocks[xydif - 1].setBlock((N1BlockX * self.SmallestN) % self.NProd,
                                                       (N1BlockY * self.SmallestN) % self.NProd, blockData, False)
            else:
                self.difblocks = blockData
        else:
            if (self.D > 1):
                xb = N1BlockX // self.NProd
                yb = N1BlockY // self.NProd
                if (xb == yb):
                    self.diagblocks[xb].setBlock(N1BlockX % self.NProd, N1BlockY % self.NProd, blockData, False)
                else:
                    xydif = abs(xb - yb)
                    self.difblocks[xydif - 1].setBlock(N1BlockX % self.NProd, N1BlockY % self.NProd, blockData, False)
            else:
                self.difblocks = blockData

    def readBlock(self, N1BlockX, N1BlockY, startFlag=True):
        if (startFlag):
            if (self.D > 1):
                xb = (N1BlockX * self.SmallestN) // self.NProd
                yb = (N1BlockY * self.SmallestN) // self.NProd
                if (xb == yb):
                    return (self.diagblocks[xb].readBlock((N1BlockX * self.SmallestN) % self.NProd,
                                                          (N1BlockY * self.SmallestN) % self.NProd, False))
                else:
                    xydif = abs(xb - yb)
                    return (self.difblocks[xydif - 1].readBlock((N1BlockX * self.SmallestN) % self.NProd,
                                                                (N1BlockY * self.SmallestN) % self.NProd, False))
            else:
                return (self.difblocks)
        else:
            if (self.D > 1):
                xb = N1BlockX // self.NProd
                yb = N1BlockY // self.NProd
                if (xb == yb):
                    return (self.diagblocks[xb].readBlock(N1BlockX % self.NProd, N1BlockY % self.NProd, False))
                else:
                    xydif = abs(xb - yb)
                    return (self.difblocks[xydif - 1].readBlock(N1BlockX % self.NProd, N1BlockY % self.NProd, False))
            else:
                return (self.difblocks)


def calcPESfromPsi4(D, N, equil, pes, cores, psi4method):
    import psi4

    psi4.core.be_quiet()
    Npts = np.prod(N)
    if (D == 1):
        mol_geom = """
        {q} {mult}
        {s1} {x1} {y1} {z1}
        {s2} {x2} {y2} {z2}
        """

        S = equil.getSymbolList()
        z = equil.getZList()
        Q = equil.getCharge()
        Mult = equil.getMultiplicity()
        psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                               s1=S[0], x1=0, y1=0, z1=z[0],
                                               s2=S[1], x2=0, y2=0, z2=z[1]))
        try:
            emin = psi4.energy(psi4method, molecule=psimol)
        except:
            print("Error: Unknown/unsupported method " + psi4method + " or other Psi4 error.")
            raise

        for pt in range(Npts):
            mol = pes.getPointByPt[pt].getMolecule()
            z = mol.getZList()
            psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                                   s1=S[0], x1=0, y1=0, z1=z[0],
                                                   s2=S[1], x2=0, y2=0, z2=z[1]))
            try:
                en = psi4.energy(psi4method, molecule=psimol)
            except:
                print("Error: Unknown/unsupported method " + psi4method + " or other Psi4 error.")
                raise
            pes.getPointByPt[pt].setEnergy(en - emin)
    elif (D == 3):
        mol_geom = """
        {q} {mult}
        {s1} {x1} {y1} {z1}
        {s2} {x2} {y2} {z2}
        {s3} {x3} {y3} {z3}
        """

        S = equil.getSymbolList()
        x = equil.getXList()
        y = equil.getYList()
        Q = equil.getCharge()
        Mult = equil.getMultiplicity()
        psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                               s1=S[0], x1=x[0], y1=y[0], z1=0,
                                               s2=S[1], x2=x[1], y2=y[1], z2=0,
                                               s3=S[2], x3=x[2], y3=y[2], z3=0))
        try:
            emin = psi4.energy(psi4method, molecule=psimol)
        except:
            print("Error: Unknown/unsupported method " + psi4method + " or other Psi4 error.")
            raise

        for pt in range(Npts):
            mol = pes.getPointByPt[pt].getMolecule()
            x = mol.getXList()
            y = mol.getYList()
            psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                                   s1=S[0], x1=x[0], y1=y[0], z1=0,
                                                   s2=S[1], x2=x[1], y2=y[1], z2=0,
                                                   s3=S[2], x3=x[2], y3=y[2], z3=0))
            try:
                en = psi4.energy(psi4method, molecule=psimol)
            except:
                print("Error: Unknown/unsupported method " + psi4method + " or other Psi4 error.")
                raise
            pes.getPointByPt[pt].setEnergy(en - emin)
        else:
            raise ("Invalid call to Psi4 driver")
    return


def Vab(D, N, pes, alpha, beta):
    if (alpha == beta):
        return pes.getPointByPt(alpha).getEnergy()

    idx_a = pyfghutil.PointToIndex(N, alpha)
    idx_b = pyfghutil.PointToIndex(N, beta)

    deltacounter = True
    j = 0
    while (deltacounter and (j < D)):
        if (idx_a[j] != idx_b[j]):
            deltacounter = False
        j = j + 1

    if (deltacounter):
        return pes.getPointByIdx(idx_a).getEnergy()
    else:
        return 0.0


def VBlockCalc(dimensions, NValue, pes, blockX, blockY):
    # Blocks will be 0 index
    blockHolder = np.zeros((NValue[0], NValue[0]), float)
    # The 0Start variables will always be 0 at the beginning to act as loop variables that correspond to the blockHolder size
    alpha0start = 0
    beta0start = 0
    for alpha in range(0 + NValue[0] * blockX, NValue[0] + NValue[0] * blockX):
        for beta in range(0 + NValue[0] * blockY, NValue[0] + NValue[0] * blockY):
            blockHolder[alpha0start, beta0start] = (Vab(dimensions, NValue, pes, alpha, beta))
            beta0start += 1
        alpha0start += 1
        beta0start = 0
    return blockHolder


# The function to calculate a VMatrix using the DataObject class input
def VMatrixCalc(dimensions, NValue, Vmethod, equil, pes, psi4method, cores):
    # Create the VMatrix
    # The alpha and beta values are used to create the VMatrix in the correct position
    Npts = np.prod(NValue)
    vmatrix = lil_matrix((Npts, Npts), dtype=float)

    if (Vmethod == "Calculate with Psi4"):
        calcPESfromPsi4(dimensions, N, equil, pes, psi4method, cores)

    # NBlock Class System
    NBlocks = NBlock(dimensions, NValue)
    NBlocks.difSetup()

    # Calculate by blocks:
    # Don't optimize for now. Just calculate blocks as needed.
    blockCoords = []
    optBlockCoords = []
    blocks = []
    paramz = []
    totalwidth = int(np.prod(NValue))
    repeatamount = int(totalwidth // NValue[0])
    for x in range(repeatamount):
        for y in range(repeatamount):
            blockCoords.append((x, y))
    optBlockCoords = NBlocks.coordGen()
    for coords in optBlockCoords:
        paramz.append((dimensions, NValue, pes, coords[0], coords[1]))

    # Pool and run
    p = mp.Pool(cores)
    # print("Pool go V")
    blocks = p.starmap(VBlockCalc, paramz)
    # print("Pool's done V")
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
        vmatrix[(0 + NValue[precalc] * x):(NValue[precalc] + NValue[precalc] * x),
        (0 + NValue[precalc] * y):(NValue[precalc] + NValue[precalc] * y)] = NBlocks.readBlock(x, y)

    return vmatrix
