import numpy as np


class ValidationError(Exception):
    pass

def IndexToPoint(N, idx):
    return np.ravel_multi_index(idx, tuple(N))

def PointToIndex(N, pt):
    return list(np.unravel_index(pt, tuple(N)))

'''
The Molecule class.  Defines a chemical molecule.
Nat = number of atoms in the molecule
Q = the molecular charge (int)
Mult = the electronic spin multiplicity (int)
S = a list of length Nat of atomic symbols for each atom (str)
Z = a list of length Nat of atomic numbers for each atom (int)
A = a list of length Nat of mass numbers for each atom (int)
m = a list of length Nat of the masses for each atom (float)
x = a list of length Nat of the x coordinates for each atom (float)
y = a list of length Nat of the y coordinates for each atom (float)
z = a list of length Nat of the z coordinates for each atom (float)
'''

class Molecule:
    def __init__(self):
        self.Nat = 0
        self.Q = 0
        self.Mult = 0
        self.S = None
        self.x = None
        self.y = None
        self.z = None
        self.A = None
        self.Z = None
        self.m = None

    def setNatom(self, Nat):
        self.Nat = Nat
        return

    def getNatom(self):
        return self.Nat

    def setCharge(self, Q):
        self.Q = Q
        return

    def getCharge(self):
        return self.Q

    def setMultiplicity(self, mult):
        self.Mult = mult
        return

    def getMultiplicity(self):
        return self.Mult

    def setSymbol(self,n,s):
        self.S[n] = s
        return

    def setSymbolList(self,S):
        self.S = S
        return

    def getSymbol(self,n):
        return self.S[n]

    def getSymbolList(self):
        return self.S

    def setAtomicNo(self,n,Z):
        self.Z[n] = Z
        return

    def setAtomicNoList(self,Z):
        self.Z = Z
        return

    def getAtomicNo(self,n):
        return self.Z[n]

    def getAtomicNoList(self):
        return self.Z

    def setMassNo(self,n,A):
        self.A[n] = A
        return

    def setMassNoList(self,A):
        self.A = A
        return

    def getMassNo(self,n):
        return self.A[n]

    def getMassNoList(self):
        return self.A

    def setMass(self,n,m):
        self.m[n] = m
        return

    def setMassList(self,m):
        self.m = m
        return

    def getMass(self,n):
        return self.m[n]

    def getMassList(self):
        return self.m

    def setX(self, n, x):
        self.x[n] = x
        return

    def setXList(self,x):
        self.x = x
        return

    def setY(self, n, y):
        self.y[n] = y
        return

    def setYList(self, y):
        self.y = y
        return

    def setZ(self, n, z):
        self.z[n] = z
        return

    def setZList(self, z):
        self.z = z
        return

    def getX(self,n):
        return self.x[n]

    def getY(self,n):
        return self.y[n]

    def getZ(self,n):
        return self.z[n]

    def getXList(self):
        return self.x

    def getYList(self):
        return self.y

    def getZList(self):
        return self.z

    def getMassByCoord(self,n):
        return self.m[n//3]



# A class to define a point on the potential energy surface.
# n = the number of the grid point (indexed from 0)
# q = a list of length 3 to define the values of q for the grid point
# x, y, z = a list of the x,y,z coordinates of the atoms at the point
# en = the value of the potential energy at this point (in atomic units)


class PESpoint:
    def __init__(self,n):
        self.n = n
        self.q = []
        self.mol = Molecule()
        self.en = 0

    def getPointNo(self):
        return self.n

    def setQList(self, q):
        self.q = q
        return

    def getQ(self,n):
        return self.q[n]

    def getQList(self):
        return self.q

    def setMolecule(self,mol):
        self.mol = mol
        return

    def getMolecule(self):
        return(self.mol)

    def setXList(self, x):
        self.getMolecule().setXList(x)
        return

    def getX(self,n):
        return self.getMolecule().getX(n)

    def getXList(self):
        return self.getMolecule().getXList()

    def setYList(self, y):
        self.getMolecule().setYList(y)
        return

    def getY(self,n):
        return self.getMolecule().getY(n)

    def getYList(self):
        return self.getMolecule().getYList()

    def setZList(self, z):
        self.getMolecule().setZList(z)
        return

    def getZ(self,n):
        return self.getMolecule().getZ(n)

    def getZList(self):
        return self.getMolecule().getZList()

    def getCoord(self,c):
        if (c % 3 == 0):
            return self.getMolecule().getX(c // 3)
        elif (c % 3 == 1):
            return self.getMolecule().getY(c // 3)
        elif (c % 3 == 2):
            return self.getMolecule().getZ(c // 3)

    def setEnergy(self, en):
        self.en = en
        return

    def getEnergy(self):
        return self.en

'''
A class to define a potential energy surface.
N = a list of length D containing the number of grid points in each dimension
Npts = number of points in the PES
pts = a list of length Npts of PESpoint objects
'''

class PotentialEnergySurface:
    def __init__(self,N):
        self.N = N
        self.Npts = np.prod(N)
        self.pts = [None]*self.Npts

    def getNpts(self):
        return self.Npts

    def setPESpt(self, pt, pespt):
        self.pts[pt] = pespt
        return

    def getPointByIdx(self, idx):
        pt = IndexToPoint(self.N, idx)
        return self.getPointByPt(pt)

    def getPointByPt(self, pt):
        return self.pts[pt]

# A lookup dictionary connecting each atomic number with its corresponding atomic symbol.

AtomicSymbolLookup = {
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    21: "Sc",
    22: "Ti",
    23: "V",
    24: "Cr",
    25: "Mn",
    26: "Fe",
    27: "Co",
    28: "Ni",
    29: "Cu",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    39: "Y",
    40: "Zr",
    41: "Nb",
    42: "Mo",
    43: "Tc",
    44: "Ru",
    45: "Rh",
    46: "Pd",
    47: "Ag",
    48: "Cd",
    49: "In",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
    54: "Xe",
    55: "Cs",
    56: "Ba",
    57: "La",
    58: "Ce",
    59: "Pr",
    60: "Nd",
    61: "Pm",
    62: "Sm",
    63: "Eu",
    64: "Gd",
    65: "Tb",
    66: "Dy",
    67: "Ho",
    68: "Er",
    69: "Tm",
    70: "Yb",
    71: "Lu",
    72: "Hf",
    73: "Ta",
    74: "W",
    75: "Re",
    76: "Os",
    77: "Ir",
    78: "Pt",
    79: "Au",
    80: "Hg",
    81: "Tl",
    82: "Pb",
    83: "Bi",
    84: "Po",
    85: "At",
    86: "Rn",
    87: "Fr",
    88: "Ra",
    89: "Ac",
    90: "Th",
    91: "Pa",
    92: "U",
    93: "Np",
    94: "Pu",
    95: "Am",
    96: "Cm",
    97: "Bk",
    98: "Cf",
    99: "Es",
    100: "Fm",
    101: "Md",
    102: "No",
    103: "Lr",
    104: "Rf",
    105: "Db",
    106: "Sg",
    107: "Bh",
    108: "Hs",
    109: "Mt",
    110: "Ds",
    111: "Rg",
    112: "Cn",
    113: "Nh",
    114: "Fl",
    115: "Mc",
    116: "Lv",
    117: "Ts",
    118: "Og"
}

# A lookup dictionary connecting each nuclide with its mass (in amu).

MassLookup = {
    "H-1": 1.007825032,
    "H-2": 2.014101778,
    "H-3": 3.016049278,
    "He-3": 3.01602932,
    "He-4": 4.002603254,
    "Li-6": 6.015122887,
    "Li-7": 7.016003437,
    "Be-9": 9.012183065,
    "B-10": 10.01293695,
    "B-11": 11.00930536,
    "C-12": 12.0,
    "C-13": 13.00335484,
    "C-14": 14.00324199,
    "N-14": 14.003074,
    "N-15": 15.0001089,
    "O-16": 15.99491462,
    "O-17": 16.99913176,
    "O-18": 17.99915961,
    "F-19": 18.99840316,
    "Ne-20": 19.99244018,
    "Ne-21": 20.99384669,
    "Ne-22": 21.99138511,
    "Na-23": 22.98976928,
    "Mg-24": 23.9850417,
    "Mg-25": 24.98583698,
    "Mg-26": 25.98259297,
    "Al-27": 26.98153853,
    "Si-28": 27.97692653,
    "Si-29": 28.97649466,
    "Si-30": 29.97377014,
    "P-31": 30.973762,
    "P-32": 31.97207117,
    "P-33": 32.97145891,
    "P-34": 33.967867,
    "P-36": 35.96708071,
    "S-32": 31.97207117,
    "S-33": 32.97145890,
    "S-34": 33.96786701,
    "Cl-35": 34.96885268,
    "Cl-37": 36.9659026,
    "Ar-36": 35.96754511,
    "Ar-38": 37.96273211,
    "Ar-40": 39.96238312,
    "K-39": 38.96370649,
    "K-40": 39.96399817,
    "K-41": 40.96182526,
    "Ca-40": 39.96259086,
    "Ca-42": 41.95861783,
    "Ca-43": 42.95876644,
    "Ca-44": 43.95548156,
    "Ca-46": 45.953689,
    "Ca-48": 47.95252276,
    "Sc-45": 44.95590828,
    "Ti-46": 45.95262772,
    "Ti-47": 46.95175879,
    "Ti-48": 47.94794198,
    "Ti-49": 48.94786568,
    "Ti-50": 49.94478689,
    "V-50": 49.94715601,
    "V-51": 50.94395704,
    "Cr-50": 49.94604183,
    "Cr-52": 51.94050623,
    "Cr-53": 52.94064815,
    "Cr-54": 53.93887916,
    "Mn-55": 54.93804391,
    "Fe-54": 53.93960899,
    "Fe-56": 55.93493633,
    "Fe-57": 56.93539284,
    "Fe-58": 57.93327443,
    "Co-59": 58.93319429,
    "Ni-58": 57.93534241,
    "Ni-60": 59.93078588,
    "Ni-61": 60.93105557,
    "Ni-62": 61.92834537,
    "Ni-64": 63.92796682,
    "Cu-63": 62.92959772,
    "Cu-65": 64.9277897,
    "Zn-64": 63.92914201,
    "Zn-66": 65.92603381,
    "Zn-67": 66.92712775,
    "Zn-68": 67.92484455,
    "Zn-70": 69.9253192,
    "Ga-69": 68.9255735,
    "Ga-71": 70.92470258,
    "Ge-70": 69.92424875,
    "Ge-72": 71.92207583,
    "Ge-73": 72.92345896,
    "Ge-74": 73.92117776,
    "Ge-76": 75.92140273,
    "As-75": 74.92159457,
    "Se-74": 73.92247593,
    "Se-76": 75.9192137,
    "Se-77": 76.91991415,
    "Se-78": 77.91730928,
    "Se-80": 79.9165218,
    "Se-82": 81.9166995,
    "Br-79": 78.9183376,
    "Br-81": 80.9162897,
    "Kr-78": 77.92036494,
    "Kr-80": 79.91637808,
    "Kr-82": 81.91348273,
    "Kr-83": 82.91412716,
    "Kr-84": 83.91149773,
    "Kr-86": 85.91061063,
    "Rb-85": 84.91178974,
    "Rb-87": 86.90918053,
    "Sr-84": 83.9134191,
    "Sr-86": 85.9092606,
    "Sr-87": 86.9088775,
    "Sr-88": 87.9056125,
    "Y-89": 88.9058403,
    "Zr-90": 89.9046977,
    "Zr-91": 90.9056396,
    "Zr-92": 91.9050347,
    "Zr-94": 93.9063108,
    "Zr-96": 95.9082714,
    "Nb-93": 92.906373,
    "Mo-92": 91.90680796,
    "Mo-94": 93.9050849,
    "Mo-95": 94.90583877,
    "Mo-96": 95.90467612,
    "Mo-97": 96.90601812,
    "Mo-98": 97.90540482,
    "Mo-100": 99.9074718,
    "Tc-97": 96.9063667,
    "Tc-98": 97.9072124,
    "Tc-99": 98.9062508,
    "Ru-96": 95.90759025,
    "Ru-98": 97.9052868,
    "Ru-99": 98.9059341,
    "Ru-100": 99.9042143,
    "Ru-101": 100.9055769,
    "Ru-102": 101.9043441,
    "Ru-104": 103.9054275,
    "Rh-103": 102.905498,
    "Pd-102": 101.9056022,
    "Pd-104": 103.9040305,
    "Pd-105": 104.9050796,
    "Pd-106": 105.9034804,
    "Pd-108": 107.9038916,
    "Pd-110": 109.9051722,
    "Ag-107": 106.9050916,
    "Ag-109": 108.9047553,
    "Cd-106": 105.9064599,
    "Cd-108": 107.9041834,
    "Cd-110": 109.9030066,
    "Cd-111": 110.9041829,
    "Cd-112": 111.9027629,
    "Cd-113": 112.9044081,
    "Cd-114": 113.9033651,
    "Cd-116": 115.9047632,
    "In-113": 112.9040618,
    "In-115": 114.9038788,
    "Sn-112": 111.9048239,
    "Sn-114": 113.9027827,
    "Sn-115": 114.9033447,
    "Sn-116": 115.9017428,
    "Sn-117": 116.902954,
    "Sn-118": 117.9016066,
    "Sn-119": 118.9033112,
    "Sn-120": 119.9022016,
    "Sn-122": 121.9034438,
    "Sn-124": 123.9052766,
    "Sb-121": 120.903812,
    "Sb-123": 122.9042132,
    "Te-120": 119.9040593,
    "Te-122": 121.9030435,
    "Te-123": 122.9042698,
    "Te-124": 123.9028171,
    "Te-125": 124.9044299,
    "Te-126": 125.9033109,
    "Te-128": 127.9044613,
    "Te-139": 129.9062227,
    "I-127": 126.9044719,
    "Xe-124": 123.905892,
    "Xe-126": 125.9042983,
    "Xe-128": 127.903531,
    "Xe-129": 128.9047809,
    "Xe-130": 129.9035093,
    "Xe-131": 130.9050841,
    "Xe-132": 131.9041551,
    "Xe-134": 133.9053947,
    "Xe-136": 135.9072145,
    "Cs-133": 132.905452,
    "Ba-130": 129.9063207,
    "Ba-132": 131.9050611,
    "Ba-134": 133.9045082,
    "Ba-135": 134.9056884,
    "Ba-136": 135.9045757,
    "Ba-137": 136.9058271,
    "Ba-138": 137.905247,
    "La-138": 137.9071149,
    "La-139": 138.9063563,
    "Ce-136": 135.9071292,
    "Ce-138": 137.905991,
    "Ce-140": 139.9054431,
    "Ce-142": 141.9092504,
    "Pr-141": 140.9076576,
    "Nd-142": 141.907729,
    "Nd-143": 142.90982,
    "Nd-144": 143.910093,
    "Nd-145": 144.9125793,
    "Nd-146": 145.9131226,
    "Nd-148": 147.9168993,
    "Nd-150": 149.9209022,
    "Pm-145": 144.9127559,
    "Pm-147": 146.915145,
    "Sm-144": 143.9120065,
    "Sm-147": 146.9149044,
    "Sm-148": 147.9148292,
    "Sm-149": 148.9171921,
    "Sm-150": 149.9172829,
    "Sm-152": 151.9197397,
    "Sm-154": 153.9222169,
    "Eu-151": 150.9198578,
    "Eu-153": 152.921238,
    "Gd-152": 151.9197995,
    "Gd-154": 153.9208741,
    "Gd-155": 154.9226305,
    "Gd-156": 155.9221312,
    "Gd-157": 156.9239686,
    "Gd-158": 157.9241123,
    "Gd-160": 159.9270624,
    "Tb-159": 158.9253547,
    "Dy-156": 155.9242847,
    "Dy-158": 157.9244159,
    "Dy-160": 159.9252046,
    "Dy-161": 160.9269405,
    "Dy-162": 161.9268056,
    "Dy-163": 162.9287383,
    "Dy-164": 163.9291819,
    "Ho-165": 164.9303288,
    "Er-162": 161.9287884,
    "Er-164": 163.9292088,
    "Er-166": 165.9302995,
    "Er-167": 166.9320546,
    "Er-168": 167.9323767,
    "Er-170": 169.9354702,
    "Tm-169": 168.9342179,
    "Yb-168": 167.9338896,
    "Yb-170": 169.9347664,
    "Yb-171": 170.9363302,
    "Yb-172": 171.9363859,
    "Yb-173": 172.9382151,
    "Yb-174": 173.9388664,
    "Yb-176": 175.9425764,
    "Lu-175": 174.9407752,
    "Lu-176": 175.9426897,
    "Hf-174": 173.9400461,
    "Hf-176": 175.9414076,
    "Hf-177": 176.9432277,
    "Hf-178": 177.9437058,
    "Hf-179": 178.9458232,
    "Hf-180": 179.946557,
    "Ta-180": 179.9474648,
    "Ta-181": 180.9479958,
    "W-180": 179.9467108,
    "W-182": 181.9482039,
    "W-183": 182.9502228,
    "W-184": 183.9509309,
    "W-186": 185.9543628,
    "Re-185": 184.9529545,
    "Re-187": 186.9557501,
    "Os-184": 183.9524885,
    "Os-186": 185.953835,
    "Os-187": 186.9557474,
    "Os-188": 187.9558352,
    "Os-189": 188.9581442,
    "Os-190": 189.9584437,
    "Os-192": 191.961477,
    "Ir-191": 190.9605893,
    "Ir-193": 192.9629216,
    "Pt-190": 189.9599297,
    "Pt-192": 191.9610387,
    "Pt-194": 193.9626809,
    "Pt-195": 194.9647917,
    "Pt-196": 195.9649521,
    "Pt-198": 197.9678949,
    "Au-197": 196.9665688,
    "Hg-196": 195.9658326,
    "Hg-198": 197.9667686,
    "Hg-199": 198.9682806,
    "Hg-200": 199.9683266,
    "Hg-201": 200.9703028,
    "Hg-202": 201.9706434,
    "Hg-204": 203.973494,
    "Tl-203": 202.9723446,
    "Tl-205": 204.9744278,
    "Pb-204": 203.973044,
    "Pb-206": 205.9744657,
    "Pb-207": 206.9758973,
    "Pb-208": 207.9766525,
    "Bi-209": 208.9803991,
    "Po-209": 208.9824308,
    "Po-210": 209.9828741,
    "At-210": 209.9871479,
    "At-211": 210.9874966,
    "Rn-211": 210.9906011,
    "Rn-220": 220.0113941,
    "Rn-222": 222.0175782,
    "Fr-223": 223.019736,
    "Ra-223": 223.0185023,
    "Ra-224": 224.020212,
    "Ra-226": 226.0254103,
    "Ra-228": 228.0310707,
    "Ac-227": 227.0277523,
    "Th-230": 230.0331341,
    "Th-232": 232.0380558,
    "Pa-231": 231.0358842,
    "U-233": 233.0396355,
    "U-234": 234.0409523,
    "U-235": 235.0439301,
    "U-236": 236.0455682,
    "U-238": 238.0507884,
    "Np-236": 236.04657,
    "Np-237": 237.0481736,
    "Pu-238": 238.0495601,
    "Pu-239": 239.0521636,
    "Pu-240": 240.0538138,
    "Pu-241": 241.0568517,
    "Pu-242": 242.0587428,
    "Pu-244": 244.0642053,
    "Am-241": 241.0568293,
    "Am-243": 243.0613813,
    "Cm-243": 243.0613893,
    "Cm-244": 244.0627528,
    "Cm-245": 245.0654915,
    "Cm-246": 246.0672238,
    "Cm-247": 247.0703541,
    "Cm-248": 248.0723499,
    "Bk-247": 247.0703073,
    "Bk-249": 249.0749877,
    "Cf-249": 249.0748539,
    "Cf-250": 250.0764062,
    "Cf-251": 251.0795886,
    "Cf-252": 252.0816272,
    "Es-252": 252.08298,
    "Fm-257": 257.0951061,
    "Md-258": 258.0984315,
    "Md-260": 260.10365,
    "No-259": 259.10103,
    "Lr-262": 262.10961,
    "Rf-267": 267.12179,
    "Db-268": 268.12567,
    "Sg-271": 271.13393,
    "Bh-272": 272.13826,
    "Hs-270": 270.13429,
    "Mt-276": 276.15159,
    "Ds-281": 281.16451,
    "Rg-280": 280.16514,
    "Cn-285": 285.17712,
    "Nh-284": 284.17873,
    "Fl-289": 289.19042,
    "Mc-288": 288.19274,
    "Lv-293": 293.20449,
    "Ts-292": 292.20746,
    "Og-294": 294.21392

}

