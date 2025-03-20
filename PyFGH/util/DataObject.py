import numpy as np
import csv
from PyFGH import Constants as co
from PyFGH.util import pyfghutil
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import ma
import os
import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.logfile = open(self.filename, 'w', encoding='utf-8')
        if self.logfile.writable():
            self.writable = True
            self.logfile.write("{0}: PyFGH invoked\n".format(datetime.datetime.now()))
            self.logfile.close()
        else:
            self.writable = False

    def write(self, txt):
        if self.writable:
            self.logfile = open(self.filename, 'a', encoding='utf-8')
            self.logfile.write("{0}: {1}\n".format(datetime.datetime.now(),txt))
            self.logfile.close()
        return

    def close(self):
        if self.writable:
            self.logfile = open(self.filename, 'a', encoding='utf-8')
            self.logfile.write("{0}: PyFGH terminated\n".format(datetime.datetime.now()))
            self.logfile.close()
        return

"""
DataObject is a place to hold data. All values in these classes are first assigned to zero. In GUI_old.py these values get 
reassigned new values based on the input of the GUI. When the GUI is terminated, these values change from zero to the 
values from the input. After the GUI is terminated, these new values can be called from any file in this project.
"""

class ValidationError(Exception):
    def __init__(self,p,msg):
        self.param = p
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return ("Validation Error for {0}: {1}".format(self.param,self.message))

class Parameter:
    def __init__(self,label,value=None,state=False,stateDependency=[]):
        self.label = label
        self.value = value
        self.state = state
        self.stateDependency = stateDependency

    def getStateDependency(self):
        return self.stateDependency

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        return

    def get(self):
        return self.value

    def set(self, value,state=None):
        self.value = value
        if state is not None:
            self.setState(state)
        return

defaultdict = {
    "D":Parameter("D",3,True),
    "N":Parameter("N",[11,11,11],True,["D"]),
    "L":Parameter("L",[1.1,1.1,1.65],True,["D"]),
    "NCores":Parameter("NCores",1,True),
    "EqFile":Parameter("EqFile"),
    "PEFile":Parameter("PEFile",None,False,["PEMethod"]),
    "NEigen":Parameter("NEigen",10,True),
    "EigenMethod":Parameter("EigenMethod",co.FMAT,True),
    "PEMethod":Parameter("PEMethod",co.READ,True),
    "Psi4Method":Parameter("Psi4Method",co.PSI4M[0],True,["PEMethod"])
}

config_file = "testingfiles/test.json"

class InputData:
    def __init__(self):
        self.nparam = 12
        self.paramdict = defaultdict.copy()
        self.paramdict["EqMol"] = Parameter("EqMol", None, False, ["EqFile"])
        self.paramdict["PES"] = Parameter("PES", None, False, ["D", "N", "L", "EqMol", "PEMethod"])
        self.logfile = Logger("testingfiles/PyFGH.log")
        self.gui = False
        self.debug = False

        self.validate_func = {
            "D": self.checkD,
            "N": self.checkN,
            "L": self.checkL,
            "NEigen": self.checkNEigen,
            "NCores": self.checkNCores,
            "PEMethod": self.checkPEMethod,
            "Psi4Method": self.checkPsi4Method,
            "EigenMethod": self.checkEigenMethod,
            "EqFile": self.checkEqFile,
            "PEFile": self.checkPEFile,
            "EqMol": self.checkEqMol,
            "PES": self.checkPES
        }

        self.validate_msg = None

    """
    The following methods are setters and getters.
    """

    def setgui(self,val):
        self.gui = val
        return

    def getgui(self):
        return self.gui

    def setdebug(self,val):
        self.debug = val
        return

    def getStateDependency(self, param):
        try:
            val = self.paramdict[param].getStateDependency()
        except KeyError:
            print("error: trying to get state dependency of unknown parameter {0}".format(param))
            raise
        return val

    def getState(self, param):
        try:
            val = self.paramdict[param].getState()
        except KeyError:
            print("error: trying to get state of unknown parameter {0}".format(param))
            raise
        return val

    def setState(self, param, state):
        try:
            self.paramdict[param].setState(state)
        except KeyError:
            print("error: trying to set state for unknown parameter {0}".format(param))
            raise
        return

    def printAllState(self):
        for p in self.paramdict.keys():
            print(p, self.getState(p))
        return

    def get(self, param):
        try:
            val = self.paramdict[param].get()
        except KeyError:
            print("error: trying to get unknown parameter {0}".format(param))
            raise
        return val

    def set(self, param, value):
        try:
            self.paramdict[param].set(value)
        except KeyError:
            print("error: trying to set value for unknown parameter {0}".format(param))
            raise
        for p in self.paramdict.keys():
            for dep in self.getStateDependency(p):
                if param == dep:
                    self.setState(dep, False)
        return

    def validate(self,param):
        self.logfile.write("working on validation parameter "+param)
        deps = self.getStateDependency(param)
        for dep in deps:
            if self.getState(dep):
                self.logfile.write("don't need to validate "+dep+", already validated")
            elif not self.validate(param=dep):
                return False
        try:
            return self.validate_func[param]()
        except KeyError:
            raise ValidationError(param,"error: missing validation function for {0}".format(param))

    def validate_all(self):
        self.logfile.write("Begin all parameter validation method")
        paramlist = self.paramdict.keys()
        for p in paramlist:
            self.setState(p,False)
        for p in paramlist:
            res = self.validate(p)
            if not res:
                raise ValidationError(p,self.validate_msg)
        self.logfile.write("All parameters successfully validated")
        return True

    # The following are the individual checks used in validate
    def checkD(self):
        self.setState("D",False)
        D = self.get("D")
        if not isinstance(D,int):
            self.validate_msg = "D is not an integer"
            return False
        if D > co.MAXDIM:
            self.validate_msg = "D must be {0} or less".format(co.MAXDIM)
            return False
        self.setState("D",True)
        self.logfile.write("validated D")
        return True

    def checkN(self):
        self.setState("N", False)
        D = self.get("D")
        N = self.get("N")

        if not isinstance(N, np.ndarray):
            try:
                N = np.array(N,dtype=int)
            except ValueError:
                self.validate_msg = "N values are not integers"
                return False
            self.set("N",N)
        if len(N) != D:
            self.validate_msg = "length of N is not equal to D"
            return False
        for i in range(D):
            if pyfghutil.isEven(N[i]):
                self.validate_msg = "N values must be odd"
                return False
            if N[i] < 5:
                self.validate_msg = "N values are less than 5"
                return False
        self.setState("N", True)
        self.logfile.write("validated N")
        return True

    def checkL(self):
        self.setState("L",False)
        D = self.get("D")
        L = self.get("L")

        if not isinstance(L, np.ndarray):
            try:
                L = np.array(L,dtype=float)
            except ValueError:
                self.validate_msg = "L values are not floats"
                return False
            self.set("L",L)
        if len(L) != D:
            self.validate_msg = "length of L is not equal to D"
            return False
        for i in range(D):
            if (L[i] <= 0):
                self.validate_msg = "L values are not positive"
                return False
        self.setState("L", True)
        self.logfile.write("validated L")
        return True

    def checkNEigen(self):
        self.setState("NEigen",False)
        NEigen = self.get("NEigen")
        if not isinstance(NEigen,int):
            self.validate_msg = "error: number of eigenvalues must be an integer"
            return False
        if (NEigen < 1) or (NEigen > co.MAXEIG):
            self.validate_msg = "error: number of eigenvalues must be between 1 and {0}".format(co.MAXEIG)
            return False
        self.setState("NEigen",True)
        self.logfile.write("validated NEigen")
        return True

    def checkNCores(self):
        self.setState("NCores",False)
        NCores = self.get("NCores")
        if not isinstance(NCores,int):
            self.validate_msg = "error: number of cores must be an integer"
            return False
        if NCores < 1:
            self.validate_msg = "error: number of cores must be a positive integer"
            return False
        self.setState("NCores",True)
        self.logfile.write("validated NCores")
        return True

    def checkPEMethod(self):
        self.setState("PEMethod",False)
        if self.get("PEMethod") not in co.CMETHOD:
            self.validate_msg = "error: Potential Energy method must be one of the following: {0}".format(co.PSI4M)
            return False
        self.setState("PEMethod",True)
        self.logfile.write("validated PEMethod")
        return True

    def checkPsi4Method(self):
        self.setState("Psi4Method",False)
        PEMethod = self.get("PEMethod")
        if PEMethod == co.CPSI:
            psi4method = self.get("Psi4Method")
            if psi4method not in co.PSI4M:
                self.validate_msg = "error: unsupported Psi4 method {0}".format(psi4method)
                return False
            self.setState("Psi4Method",True)
            self.logfile.write("validated Psi4Method")
            return True
        else:
            self.setState("Psi4Method",True)
            self.logfile.write("Since Psi4 potential energies were not chosen, Psi4Method parameter was ignored.")
            return True

    def checkEigenMethod(self):
        self.setState("EigenMethod",False)
        eigenmethod = self.get("EigenMethod")
        if eigenmethod not in co.MATRIX:
            self.validate_msg = "error: unrecognized eigenvalue method {0}".format(eigenmethod)
        self.setState("EigenMethod",True)
        self.logfile.write("validated EigenMethod")
        return True

    def checkEqFile(self):
        self.setState("EqFile",False)
        eqfile = self.get("EqFile")
        try:
            if os.path.isfile(eqfile) and os.access(eqfile, os.R_OK):
                self.setState("EqFile",True)
                self.logfile.write("validated EqFile")
                return True
            else:
                self.validate_msg = "file {0} either does not exist or is not readable".format(eqfile)
                return False
        except TypeError:
            self.validate_msg = "invalid input for equilibrium filename"
            return False

    def checkPEFile(self):
        self.setState("PEFile",False)
        if self.get("PEMethod") == co.READ:
            pefile = self.get("PEFile")
            try:
                if os.path.isfile(pefile) and os.access(pefile, os.R_OK):
                    self.setState("PEFile",True)
                    self.logfile.write("validated PEFile")
                    return True
                else:
                    self.validate_msg = "error: file {0} either does not exist or is not readable".format(pefile)
                    return False
            except TypeError:
                self.validate_msg = "error: invalid input for PES filename"
                return False
        else:
            self.setState("PEFile",True)
            self.logfile.write("Since reading PE from file was not selected, PEFile parameter was ignored.")
            return True

    def checkEqMol(self):
        self.setState("EqMol",False)
        if self.readEqFile():
            self.setState("EqMol",True)
            self.logfile.write("validated EqMol")
            return True
        else:
            self.set("EqMol",None)
            self.setState("EqMol",False)
            return False

    def checkPES(self):
        self.setState("PES",False)
        PEMethod = self.get("PEMethod")
        if (PEMethod == co.READ):
            if self.readPESfile():
                self.setState("PES",True)
                self.logfile.write("validated PES for READ")
                return True
        if (PEMethod == co.CPSI):
            if self.generatePESCoordinates_Psi4():
                self.setState("PES",True)
                self.logfile.write("validated PES for CPSI")
                return True
        self.set("PES",None)
        self.setState("PES",False)
        return False

    def readEqFile(self):
        eqfile = self.get("EqFile")
        S = []
        A = []
        Z = []
        x = []
        y = []
        z = []
        m = []
        with open(eqfile, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            row = next(reader)
            try:
                Q = int(row[0])
                Mult = int(row[1])
            except (IndexError, ValueError):
                self.validate_msg = 'In Equilibrium File: First Line Should Contain Charge and Multiplicity'
                return False
            if (Mult < 1):
                self.validate_msg = 'Read Multiplicity of {0}, Should Be A Positive Integer'.format(Mult)
                return False

            self.logfile.write("Charge is {0}, Multiplicity is {1}".format(Q, Mult))

            Nat = 0
            for row in reader:
                try:
                    S.append(row[0])
                    A.append(int(row[1]))
                    x.append(float(row[2]) / 0.529177249)
                    y.append(float(row[3]) / 0.529177249)
                    z.append(float(row[4]) / 0.529177249)
                except (IndexError, ValueError):
                    self.validate_msg = 'In Equilibrium File: Missing Data or Wrong Format Found on Line {0}'.format(Nat + 2)
                    return False
                Nat = Nat + 1

        self.logfile.write("Read {0} Atoms from Equilibrium File".format(Nat))

        for n in range(Nat):
            symbolFound = False
            for key, value in pyfghutil.AtomicSymbolLookup.items():
                if (value == S[n]):
                    Z.append(key)
                    symbolFound = True
                    break
            if (not symbolFound):
                self.validate_msg = 'Atom {0} Symbol {1} Not Found In Dictionary'.format(n + 1, S[n])
                return False

        Nel = np.sum(Z) - Q
        if ((Nel % 2) == (Mult % 2)):
            self.validate_msg = 'Charge {0} And Multiplicity {1} Are Inconsistent'.format(Q, Mult)
            return False

        for n in range(Nat):
            nucl = S[n] + "-" + str(A[n])
            m.append(pyfghutil.MassLookup.get(nucl))
            if (m[n] == None):
                self.validate_msg = 'Atom {0} Nuclide {1} Not Found In Dictionary'.format(n + 1, nucl)
                return False
            else:
                m[n] = float(m[n]) * 1822.89

        eqmol = pyfghutil.Molecule()
        eqmol.setNatom(Nat)
        eqmol.setCharge(Q)
        eqmol.setMultiplicity(Mult)
        eqmol.setSymbolList(S)
        eqmol.setMassNoList(np.array(A))
        eqmol.setXList(np.array(x))
        eqmol.setYList(np.array(y))
        eqmol.setZList(np.array(z))
        eqmol.setAtomicNoList(np.array(Z))
        eqmol.setMassList(np.array(m))

        if not pyfghutil.closeContactTest(eqmol):
            self.validate_msg = "error: in equilibrium structure, atoms are too close together"
            return False
        self.set("EqMol",eqmol)
        self.logfile.write("Equilibrium molecule successfully read and validated")
        return True

    def readPESfile(self):
        self.set("PES",None)
        self.setState("PES",False)
        PEFile = self.get("PEFile")
        D = self.get("D")
        N = self.get("N")
        Npts = np.prod(N)
        L = self.get("L")
        EqMol = self.get("EqMol")
        Nat = EqMol.getNatom()

        pes = pyfghutil.PotentialEnergySurface(N)
        with open(PEFile, newline='') as f:
            reader = csv.reader(f)

            n = 0
            for row in reader:
                try:
                    q = np.zeros(D, dtype=float)
                    for i in range(D):
                        q[i] = float(row[i])

                    x = np.zeros(Nat, dtype=float)
                    y = np.zeros(Nat, dtype=float)
                    z = np.zeros(Nat, dtype=float)
                    for i in range(Nat):
                        x[i] = float(row[D + 3 * i])
                        y[i] = float(row[D + 3 * i + 1])
                        z[i] = float(row[D + 3 * i + 2])

                    en = float(row[D + 3 * Nat])
                except (IndexError, ValueError):
                    self.validate_msg = "In PES file: Missing data or wrong format found on line {0}".format(n + 1)
                    return False

                pespt = pyfghutil.PESpoint(n)
                pespt.setQList(q)
                pespt.setXList(x)
                pespt.setYList(y)
                pespt.setZList(z)
                pespt.getMolecule().setNatom(Nat)
                pespt.getMolecule().setCharge(EqMol.getCharge())
                pespt.getMolecule().setMultiplicity(EqMol.getMultiplicity())
                pespt.getMolecule().setSymbolList(EqMol.getSymbolList())
                pespt.getMolecule().setAtomicNoList(EqMol.getAtomicNoList())
                pespt.getMolecule().setMassNoList(EqMol.getMassNoList())
                pespt.getMolecule().setMassList(EqMol.getMassList())
                pespt.setEnergy(en)

                if not pyfghutil.closeContactTest(pespt):
                    self.validate_msg = "error: in PES point {0}, atoms are too close together".format(n)
                    return False

                pes.setPESpt(n, pespt)
                n = n + 1

        if (Npts != n):
            self.validate_msg = "Error: Expecting {0} lines in PES file, read {1}".format(Npts, n)
            return False

        self.logfile.write("Read {0} lines from potential energy file".format(n))
        self.set("PES",pes)
        return True

    '''
    Function generatePESCoordinates_Psi4 generates a PES object if the user chooses "Compute With Psi4".  It fills the PES object
    with molecular structures corresponding to the input D, N, L values but with energy values of zero.  The energy values are computed in Vmatrix.
    Input: 
    D: number of dimensions (int)
    N: numpy array of length D of number of points in each dimension (int)
    L: numpy array of length D of the length of each grid, in bohr (float)
    equil: Molecule object with the equilibrium molecular structure
    Output:
    PotentialEnergySurface object
    '''

    def generatePESCoordinates_Psi4(self):
        self.set("PES",None)
        self.setState("PES",False)
        EqMol = self.get("EqMol")
        D = self.get("D")
        N = self.get("N")
        L = self.get("L")
        Nat = EqMol.getNatom()

        if not (((D == 1) and (Nat == 2)) or ((D == 3) and (Nat == 3))):
            self.validate_msg = "Psi4 Calculation Method only implemented for diatomic and nonlinear triatomic molecules."
            return False

        Npts = np.prod(N)
        xeq = EqMol.getXList()
        yeq = EqMol.getYList()
        zeq = EqMol.getZList()
        Z = EqMol.getAtomicNoList()
        A = EqMol.getMassNoList()
        m = EqMol.getMassList()

        pes = pyfghutil.PotentialEnergySurface(N)

        if (D == 1):
            Req = np.linalg.norm(np.array([xeq[1] - xeq[0], yeq[1] - yeq[0], zeq[1] - zeq[0]]))

            xeq[0] = xeq[1] = yeq[0] = yeq[1] = 0
            zeq[0] = -Req / 2
            zeq[1] = Req / 2

            EqMol.setXList(xeq)
            EqMol.setYList(yeq)
            EqMol.setZList(zeq)

            for pt in Npts:
                pespt = pyfghutil.PESpoint(pt)
                idx = pyfghutil.PointToIndex(N, pt)
                q = np.zeros(D, dtype=float)
                for d in range(D):
                    dq = L[d] / N[d]
                    q[d] = idx[d] * dq - L[d] / 2 + dq / 2

                x = np.zeros(Nat, dtype=float)
                y = np.zeros(Nat, dtype=float)
                z = np.zeros(Nat, dtype=float)

                z[0] = -(Req + q[0]) / 2
                z[1] = (Req + q[0]) / 2

                pespt.setQList(q)
                pespt.setXList(x)
                pespt.setYList(y)
                pespt.setZList(z)
                pespt.getMolecule().setNatom(Nat)
                pespt.getMolecule().setCharge(EqMol.getCharge())
                pespt.getMolecule().setMultiplicity(EqMol.getMultiplicity())
                pespt.getMolecule().setSymbolList(EqMol.getSymbolList())
                pespt.getMolecule().setAtomicNoList(Z)
                pespt.getMolecule().setMassNoList(A)
                pespt.getMolecule().setMassList(m)
                pespt.setEnergy(0)
                pes.setPESpt(pt, pespt)

        elif (D == 3):
            R1eq = np.array([xeq[1] - xeq[0], yeq[1] - yeq[0], zeq[1] - zeq[0]])
            R1eqlen = np.linalg.norm(R1eq)
            R2eq = np.array([xeq[2] - xeq[0], yeq[2] - yeq[0], zeq[2] - zeq[0]])
            R2eqlen = np.linalg.norm(R2eq)
            theta_eq = np.arccos((np.dot(R1eq, R2eq)) / (R1eqlen * R2eqlen))

            m1 = m[0]
            m2 = m[1]
            m3 = m[2]
            M = m1 + m2 + m3

            xeq[0] = (m2 * R1eqlen - m3 * R2eqlen) * np.sin(theta_eq / 2.0) / M
            yeq[0] = -(m3 * R2eqlen + m2 * R1eqlen) * np.cos(theta_eq / 2.0) / M
            xeq[1] = xeq[0] - R1eqlen * np.sin(theta_eq / 2.0)
            yeq[1] = yeq[0] + R1eqlen * np.cos(theta_eq / 2.0)
            xeq[2] = xeq[0] + R2eqlen * np.sin(theta_eq / 2.0)
            yeq[2] = yeq[0] + R2eqlen * np.cos(theta_eq / 2.0)
            zeq[0] = zeq[1] = zeq[2] = 0

            EqMol.setXList(xeq)
            EqMol.setYList(yeq)
            EqMol.setZList(zeq)

            for pt in range(Npts):
                pespt = pyfghutil.PESpoint(pt)
                idx = pyfghutil.PointToIndex(N, pt)
                q = np.zeros(D, dtype=float)
                for d in range(D):
                    dq = L[d] / N[d]
                    q[d] = idx[d] * dq - L[d] / 2 + dq / 2

                x = np.zeros(Nat, dtype=float)
                y = np.zeros(Nat, dtype=float)
                z = np.zeros(Nat, dtype=float)

                if (A[1] == A[2]) and (Z[1] == Z[2]):
                    R1 = R1eqlen + q[0] + q[1]
                    R2 = R1eqlen + q[1] - q[0]
                else:
                    R1 = R1eqlen + q[0]
                    R2 = R2eqlen + q[1]

                theta = theta_eq + q[2]

                x[0] = (m2 * R1 - m3 * R2) * np.sin(theta / 2.0) / M
                y[0] = -(m3 * R2 + m2 * R1) * np.cos(theta / 2.0) / M
                x[1] = x[0] - R1 * np.sin(theta / 2.0)
                y[1] = y[0] + R1 * np.cos(theta / 2.0)
                x[2] = x[0] + R2 * np.sin(theta / 2.0)
                y[2] = y[0] + R2 * np.cos(theta / 2.0)

                pespt.setQList(q)
                pespt.setXList(x)
                pespt.setYList(y)
                pespt.setZList(z)
                pespt.getMolecule().setNatom(Nat)
                pespt.getMolecule().setCharge(EqMol.getCharge())
                pespt.getMolecule().setMultiplicity(EqMol.getMultiplicity())
                pespt.getMolecule().setSymbolList(EqMol.getSymbolList())
                pespt.getMolecule().setAtomicNoList(Z)
                pespt.getMolecule().setMassNoList(A)
                pespt.getMolecule().setMassList(m)
                pespt.setEnergy(0)
                pes.setPESpt(pt, pespt)

        else:
            print("this shouldn't happen")

        for pt in Npts:
            pespt = pes.getPointByPt(pt)
            if not pyfghutil.closeContactTest(pespt.getMolecule()):
                self.validate_msg = "in PES point {0}, atoms are too close together".format(pt)
                return False

        self.set("PES",pes)
        return True




#TODO take the values in Eignevalues and Eigenvectos and write them to a CSV file in main on line 104.
class OutputData:
    def __init__(self,logfile):
        self.nparam = 6
        self.paramdict = {
            "D":0,
            "N":[],
            "L":[],
            "NEigen":0,
            "EVal":[],
            "EVec":[]
        }
        self.logfile = logfile

    def get(self,param):
        try:
            return self.paramdict[param]
        except KeyError:
            raise ("error: trying to get unknown parameter {0} in OutputData".format(param))

    def set(self,param,value):
        try:
            self.paramdict[param] = value
        except KeyError:
            raise ("error: trying to set unknown parameter {0} in OutputData".format(param))

    def getOutputAsJson(self):
        return {
            "num_eigenvalues": self.get("NEigen"),
            "eigenvalues": self.get("EVal"),
            "eigenvectors": self.get("EVec")
        }

    def generateValues(self, pes):
        D = self.get("D")
        N = self.get("N")
        Npts = np.prod(N)
        Neig = self.get("NEigen")
        eigvals = self.get("EVal")
        eigvecs = self.get("EVec")
        wfnorder = np.argsort(eigvals)
        freq = np.zeros(Neig, dtype=float)

        for i in range(Neig):
            freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
            print("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))
            self.logfile.write("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))

        self.set("EVal", freq)

        wfn = np.zeros([Neig, Npts], dtype=float)
        wfn2 = np.zeros([Neig, Npts, D + 1], dtype=float)

        for p in range(Neig):
            for alpha in range(Npts):
                wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

                q = pes.getPointByPt(alpha).getQList()
                for d in range(D):
                    wfn2[p][alpha][d] = q[d]
                wfn2[p][alpha][D] = eigvecs[alpha][wfnorder[p]]

        for p in range(Neig):
            norm = 0
            for pt in range(Npts):
                norm = norm + wfn2[p][pt][D] * wfn2[p][pt][D]
            norm = 1 / np.sqrt(norm)
            for pt in range(Npts):
                wfn2[p][pt][D] = wfn2[p][pt][D] * norm

        self.set("EVec", wfn2)
        return

    def plot_data_2d(self, wfn_no, q_ind, qprojlist):
        D = self.get("D")
        N = self.get("N")
        L = self.get("L")
        wfn = self.get("EVec")[wfn_no]

        q_mask = np.zeros(D,dtype=int)
        q_mask[q_ind] = 1

        n = (N[q_ind]-1)//2
        dx = L[q_ind]/N[q_ind]
        x = np.array([(j - n) * dx for j in range(N[q_ind])],dtype=float)

        q_idx = np.zeros(D,dtype=int)
        i = 0
        for d in range(D):
            if (d != q_ind):
                q_idx[d] = int(qprojlist[i].current())
                i = i + 1

        q_idx_mask = ma.array(q_idx,mask=q_mask)
        y = np.zeros(N[q_ind],dtype=float)

        Npts = np.prod(N)
        for pt in range(Npts):
            idx = np.array(pyfghutil.PointToIndex(N, pt),dtype=int)
            idx_mask = ma.array(idx,mask=q_mask)
            if (np.equal(q_idx_mask,idx_mask).all()):
                y[idx[q_ind]] = wfn[pt][D]

        figure = self.plot_scatter(wfn_no, q_ind, x, y)

        return figure


    def plot_scatter(self, no, q_ind, x, y):
        figure = Figure(figsize=(6,4), dpi=100)
        titlestr = "Wavefunction {:0d}".format(no)
        xlabel = "q{:0d} (bohr)".format(q_ind+1)
        plot1 = figure.add_subplot(xlabel=xlabel, ylabel="Normalized Wavefunction",title=titlestr)
        plot1.plot(x,y)
        return figure

    def plot_data_contour(self, wfn_no, q_indx, q_indy, qprojlist):
        D = self.get("D")
        N = self.get("N")
        L = self.get("L")
        wfn = self.get("EVec")[wfn_no]

        q_mask = np.zeros(D,dtype=int)
        q_mask[q_indx] = 1
        q_mask[q_indy] = 1

        nx = (N[q_indx]-1)//2
        dx = L[q_indx]/N[q_indx]
        x = np.array([(j - nx) * dx for j in range(N[q_indx])],dtype=float)

        ny = (N[q_indy]-1)//2
        dy = L[q_indy]/N[q_indy]
        y = np.array([(j - ny) * dy for j in range(N[q_indy])],dtype=float)

        q_idx = np.zeros(D,dtype=int)
        i = 0
        for d in range(D):
            if ((d != q_indx) and (d != q_indy)):
                q_idx[d] = int(qprojlist[i].current())
                i = i + 1

        q_idx_mask = ma.array(q_idx,mask=q_mask)
        z = np.zeros((N[q_indx],N[q_indy]),dtype=float)

        Npts = np.prod(N)
        for pt in range(Npts):
            idx = np.array(pyfghutil.PointToIndex(N, pt),dtype=int)
            idx_mask = ma.array(idx,mask=q_mask)
            if (np.equal(q_idx_mask,idx_mask).all()):
                z[idx[q_indx],idx[q_indy]] = wfn[pt][D]

        fig = self.plot_contour(wfn_no, x, y, z, q_indx, q_indy)

        return fig


    def plot_contour(self, no, x, y, z, qx, qy):
        x2d, y2d = np.meshgrid(x, y)
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x2d, y2d, z)
        fig.colorbar(cp)  # Add a colorbar to a plot
        ax.set_title("Wavefunction {:0d}".format(no))
        ax.set_xlabel('q{:0d} (bohr)'.format(qx+1))
        ax.set_ylabel('q{:0d} (bohr)'.format(qy+1))

        return fig
