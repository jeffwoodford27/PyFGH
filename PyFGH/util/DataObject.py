import numpy as np
import gc
import csv
from PyFGH import Constants as co
from PyFGH.util import pyfghutil
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import ma

"""
DataObject is a place to hold data. All values in these classes are first assigned to zero. In GUI_old.py these values get 
reassigned new values based on the input of the GUI. When the GUI is terminated, these values change from zero to the 
values from the input. After the GUI is terminated, these new values can be called from any file in this project.
"""

class InputData:

    def __init__(self):
        self.D = 0
        self.cores_amount = 1
        self.N = None
        self.L = None
        self.equilibrium_file = None
        self.potential_energy_file = None
        self.EquilMolecule = None
        self.PES = None
        self.num_eigenvalues = 10
        self.eigenvalue_flag = False
        self.Vmethod = None
        self.model_data = None
        self.psi4method = None
        self.inputobject = None
        self.gui = False
        self.EPFlag = False
        self.debug = False


    """
    The following methods are setters. These values get set in test1.py
    """


    def setinputobject(self, inputobject):
        self.inputobject = inputobject
        return

    def getinputobject(self):
        return self.inputobject


    def getD(self):
        return self.D

    def getNlist(self):
        return self.N

    def getN(self,j):
        return self.N[j]

    def getLlist(self):
        return self.L

    def getL(self,j):
        return self.L[j]

    def getEquilFile(self):
        return self.equilibrium_file

    def getPESFile(self):
        return self.potential_energy_file

    def getEquilMolecule(self):
        return self.EquilMolecule

    def getPES(self):
        return self.PES

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues

    def getEigenvalueMethod(self):
        print(self.eigenvalue_flag)
        return self.eigenvalue_flag

    def getVmethod(self):
        return self.Vmethod

    def getPsi4Method(self):
        return self.psi4method

    def getCoresAmount(self):
        return int(self.cores_amount)

    def getgui(self):
        return self.gui

    """
    The following methods are setters. These values get set in test1.py
    """

    def setgui(self, gui):
        self.gui = gui
        return

    def setcores_amount(self, cores):
        self.cores_amount = cores
        return

    def setequilibrium_file(self, equilibrium_file):
        self.equilibrium_file = equilibrium_file
        return

    def setpotential_energy(self, potential_energy):
        self.potential_energy_file = potential_energy
        return

    def setD(self,D):
        self.D = D
        return

    def setNlist(self,N):
        self.N = np.array(N,dtype=int)
        return

    def setLlist(self,L):
        self.L = np.array(L,dtype=float)
        return

    def setEquilMolecule(self,eq):
        self.EquilMolecule = eq
        return

    def setPES(self,pes):
        self.PES = pes
        return

    def setNumberOfEigenvalues(self, num):
        self.num_eigenvalues = num
        return

    def setEigenvalueMethod(self, eigenmethod):
        print(self.eigenvalue_flag)
        self.eigenvalue_flag = eigenmethod
        return

    def setVmethod(self,vmethod):
        self.Vmethod = vmethod
        return

    def setPsi4Method(self,method):
        self.psi4method = method
        return


    # This is the validate method
    # It will check all user accessible values to see if valid
    # It will return True if everything is correct
    def validate(self):
        if not self.checkD():
            print("prob D")
            return False
        if not self.checkN():
            print("prob N")
            return False
        if not self.checkL():
            print("prob L")
            return False
        if not self.checkCores():
            print("prob cores")
            return False
        if not self.checkNumEig():
            print("prob eig")
            return False
        if not self.checkVMethod():
            print("prob V")
            return False
        if not self.checkEqPes():
            print("prob eqpes")
            return False
        return True

    # The following are the individual checks used in validate
    def checkD(self):
        if self.D > 0 and isinstance(self.D, int):
            return True
        else:
            print("D must be an integer")
            return False

    def checkN(self):
        if self.N is None:
            print("N must be set")
            return False
        for i in range(self.D):
            if isinstance(self.N[i], np.int32):
                if self.N[i] < 5:
                    print("N must be greater than 5")
                    return False
                if self.N[i] % 2 == 0:
                    print("N must be an odd number")
                    return False
                return True
            else:
                print("N must be an integer")
                return False

    def checkL(self):
        if self.L is None:
            print("L must be set")
            return False
        for i in range(self.D):
            if(isinstance(self.L[i], np.float64)):
                if (self.L[i] <= 0):
                    print("L must be greater than 0")
                    return False
                return True
            else:
                print("L must be a float")
                return False

    def checkEqPes(self):
        eq, pes = self.molecule_testing()
        gc.collect()
        self.setEquilMolecule(eq)
        self.setPES(pes)
        return True

    def checkNumEig(self):
        if self.num_eigenvalues > 0 and isinstance(self.num_eigenvalues, int):
            return True
        else:
            print("Number of eigenvalues must be an integer")
            return False

    def checkCores(self):
        if self.cores_amount > 0 and isinstance(self.cores_amount, int):
            return True
        else:
            print("Cores must be an integer")
            return False

    def checkVMethod(self):
        if self.Vmethod == co.CMETHOD[0] or self.Vmethod == co.CMETHOD[1]:
            return True
        else:
            print("Vmethod should be either 'Read From File' or 'Calculate With Psi4'")
            return False

    def checkPsi4(self):
        if self.psi4method in co.PSI4M:
            return True
        else:
            return False


    # Former molecule_gui file
    # Now used as part of the checkEqPes section of validate
    # It will calculate the potential energies and generate the points
    def readEqfile(self):
        S = []
        A = []
        Z = []
        x = []
        y = []
        z = []
        m = []
        try:
            with open(self.equilibrium_file, newline='') as f:
                reader = csv.reader(f, delimiter=',')
                row = next(reader)
                try:
                    Q = int(row[0])
                    Mult = int(row[1])
                except IndexError:
                    print('In Equilibrium File: First Line Should Contain Charge and Multiplicity')
                    self.EPFlag = False
                    return
                except ValueError:
                    print('In Equilibrium File: First Line Should Contain Charge and Multiplicity')
                    self.EPFlag = False
                if (Mult < 1):
                    print('Read Multiplicity of {0}, Should Be A Positive Integer'.format(Mult))
                    self.EPFlag = False

                print("Charge is {0}, Multiplicity is {1}".format(Q, Mult))

                Nat = 0
                for row in reader:
                    try:
                        S.append(row[0])
                        A.append(int(row[1]))
                        x.append(float(row[2]) / 0.529177249)
                        y.append(float(row[3]) / 0.529177249)
                        z.append(float(row[4]) / 0.529177249)
                    except IndexError:
                        print('In Equilibrium File: Missing Data on Line {0}'.format(Nat + 2))
                        self.EPFlag = False
                    except ValueError:
                        print('In Equilibrium File, Wrong Format Found on Line {0}'.format(Nat + 2))
                        self.EPFlag = False
                    Nat = Nat + 1

        except FileNotFoundError:
            raise

        print("Read {0} Atoms from Equilibrium File".format(Nat))

        eqmol = pyfghutil.Molecule()
        eqmol.setNatom(Nat)
        eqmol.setCharge(Q)
        eqmol.setMultiplicity(Mult)
        eqmol.setSymbolList(S)
        eqmol.setMassNoList(np.array(A))
        eqmol.setXList(np.array(x))
        eqmol.setYList(np.array(y))
        eqmol.setZList(np.array(z))
        for n in range(Nat):
            symbolFound = False
            for key, value in pyfghutil.AtomicSymbolLookup.items():
                if (value == S[n]):
                    Z.append(key)
                    symbolFound = True
                    break
            if (not symbolFound):
                print('Atom {0} Symbol {1} Not Found In Dictionary'.format(n + 1, S[n]))
                self.EPFlag = False

        eqmol.setAtomicNoList(np.array(Z))

        Nel = np.sum(Z) - Q
        if ((Nel % 2) == (Mult % 2)):
            print('Charge {0} And Multiplicity {1} Are Inconsistent'.format(Q, Mult))
            self.EPFlag = False

        for n in range(Nat):
            nucl = S[n] + "-" + str(A[n])
            m.append(pyfghutil.MassLookup.get(nucl))
            if (m[n] == None):
                print('Atom {0} Nuclide {1} Not Found In Dictionary'.format(n + 1, nucl))
                self.EPFlag = False
            else:
                m[n] = float(m[n]) * 1822.89
        eqmol.setMassList(np.array(m))

        return eqmol

    def readPESfile(self, equil):
        Npts = np.prod(self.N)
        Nat = equil.getNatom()

        pes = pyfghutil.PotentialEnergySurface(self.N)
        try:
            with open(self.getPESFile(), newline='') as f:
                reader = csv.reader(f)

                n = 0
                for row in reader:
                    pespt = pyfghutil.PESpoint(n)

                    try:
                        q = np.zeros(self.D, dtype=float)
                        for i in range(self.D):
                            q[i] = float(row[i])

                        x = np.zeros(Nat, dtype=float)
                        y = np.zeros(Nat, dtype=float)
                        z = np.zeros(Nat, dtype=float)
                        for i in range(Nat):
                            x[i] = float(row[self.D + 3 * i])
                            y[i] = float(row[self.D + 3 * i + 1])
                            z[i] = float(row[self.D + 3 * i + 2])

                        en = float(row[self.D + 3 * Nat])
                    except IndexError:
                        print("In PES file: Missing data on line {0}".format(n + 1))
                        self.EPFlag = False
                    except ValueError:
                        print('In PES file, Wrong Format Found on Line {0}'.format(n + 1))
                        self.EPFlag = False

                    pespt.setQList(q)
                    pespt.setXList(x)
                    pespt.setYList(y)
                    pespt.setZList(z)
                    pespt.getMolecule().setNatom(Nat)
                    pespt.getMolecule().setCharge(equil.getCharge())
                    pespt.getMolecule().setMultiplicity(equil.getMultiplicity())
                    pespt.getMolecule().setSymbolList(equil.getSymbolList())
                    pespt.getMolecule().setAtomicNoList(equil.getAtomicNoList())
                    pespt.getMolecule().setMassNoList(equil.getMassNoList())
                    pespt.getMolecule().setMassList(equil.getMassList())
                    pespt.setEnergy(en)
                    pes.setPESpt(n, pespt)
                    n = n + 1
        except FileNotFoundError:
            raise

        if (Npts != n):
            print("Error: Expecting {0} lines in PES file, read {1}".format(Npts, n))
            self.EPFlag = False

        print("Read {0} lines from potential energy file".format(n))

        return pes

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

    def generatePESCoordinates_Psi4(self, equil):
        Nat = equil.getNatom()

        if not (((self.D == 1) and (Nat == 2)) or ((self.D == 3) and (Nat == 3))):
            print("Psi4 Calculation Method only implemented for diatomic and triatomic molecules.")
            self.EPFlag = False

        Npts = np.prod(self.N)
        xeq = equil.getXList()
        yeq = equil.getYList()
        zeq = equil.getZList()
        Z = equil.getAtomicNoList()
        A = equil.getMassNoList()
        m = equil.getMassList()

        pes = pyfghutil.PotentialEnergySurface(self.N)
        if (self.D == 1):
            Req = np.linalg.norm(np.array([xeq[1] - xeq[0], yeq[1] - yeq[0], zeq[1] - zeq[0]]))

            xeq[0] = xeq[1] = yeq[0] = yeq[1] = 0
            zeq[0] = -Req / 2
            zeq[1] = Req / 2

            equil.setXList(xeq)
            equil.setYList(yeq)
            equil.setZList(zeq)

            for pt in Npts:
                pespt = pyfghutil.PESpoint(pt)
                idx = pyfghutil.PointToIndex(self.N, pt)
                q = np.zeros(self.D, dtype=float)
                for d in range(self.D):
                    dq = self.L[d] / self.N[d]
                    q[d] = idx[d] * dq - self.L[d] / 2 + dq / 2

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
                pespt.getMolecule().setCharge(equil.getCharge())
                pespt.getMolecule().setMultiplicity(equil.getMultiplicity())
                pespt.getMolecule().setSymbolList(equil.getSymbolList())
                pespt.getMolecule().setAtomicNoList(Z)
                pespt.getMolecule().setMassNoList(A)
                pespt.getMolecule().setMassList(m)
                pespt.setEnergy(0)
                pes.setPESpt(pt, pespt)

        elif (self.D == 3):
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

            equil.setXList(xeq)
            equil.setYList(yeq)
            equil.setZList(zeq)

            for pt in range(Npts):
                pespt = pyfghutil.PESpoint(pt)
                idx = pyfghutil.PointToIndex(self.N, pt)
                q = np.zeros(self.D, dtype=float)
                for d in range(self.D):
                    dq = self.L[d] / self.N[d]
                    q[d] = idx[d] * dq - self.L[d] / 2 + dq / 2
                if self.debug: print(pt, q)

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
                pespt.getMolecule().setCharge(equil.getCharge())
                pespt.getMolecule().setMultiplicity(equil.getMultiplicity())
                pespt.getMolecule().setSymbolList(equil.getSymbolList())
                pespt.getMolecule().setAtomicNoList(Z)
                pespt.getMolecule().setMassNoList(A)
                pespt.getMolecule().setMassList(m)
                pespt.setEnergy(0)
                pes.setPESpt(pt, pespt)

        else:
            print("this shouldn't happen")

        return pes

    def closeContactTest(self, mol, dist_cutoff=0.05):
        Nat = mol.getNatom()
        x = mol.getXList()
        y = mol.getYList()
        z = mol.getZList()
        for i in range(Nat):
            for j in range(i + 1, Nat):
                d = np.sqrt(
                    (x[j] - x[i]) * (x[j] - x[i]) + (y[j] - y[i]) * (y[j] - y[i]) + (z[j] - z[i]) * (z[j] - z[i]))
                if (d < dist_cutoff):
                    return False

        return True

    def linearTest(self, mol, cutoff=0.05):
        Nat = mol.getNatom()
        x = mol.getXList()
        y = mol.getYList()
        z = mol.getZList()
        for at1 in range(Nat):
            for at2 in range(at1 + 1, Nat):
                for at3 in range(at2 + 1, Nat):
                    v12 = np.array([x[at2] - x[at1], y[at2] - y[at1], z[at2] - z[at1]])
                    v13 = np.array([x[at3] - x[at1], y[at3] - y[at1], z[at3] - z[at1]])
                    dot1213 = np.dot(v12, v13)
                    v12len = np.linalg.norm(v12)
                    v13len = np.linalg.norm(v13)
                    costheta = dot1213 / (v12len * v13len)
                    if (costheta > (1 - cutoff)) or (costheta < (-1 + cutoff)):
                        return False
        return True

    def molecule_testing(self):
        D = self.getD()
        N = self.getNlist()
        if self.debug: print(D)
        if self.debug: print(N)

        eqfile = self.getEquilFile()
        if (not eqfile):
            print("No Equilibrium Structure file input!")
            self.EPFlag = False

        equil = self.readEqfile()
        if (self.closeContactTest(equil) == False):
            print("Atoms less than 0.05 bohr apart in the equilibrium structure.")
            self.EPFlag = False
        #    if (linearTest(equil) == False):
        #        raise ValidationError("The equilibrium structure is linear. Linear molecules not yet supported.")

        if (self.getVmethod() == co.READ):
            pesfile = self.getPESFile()
            if (pesfile == None):
                print("No Potential Energy file input!")
            pes = self.readPESfile(equil)
            Npts = np.prod(N)
            for pt in range(Npts):
                mol = pes.getPointByPt(pt).getMolecule()
                if (self.closeContactTest(mol) == False):
                    print("Atoms less than 0.05 bohr apart in PES structure " + str(pt + 1))
                    self.EPFlag = False
        #            if (linearTest(mol) == False):
        #                raise ValidationError("PES structure " + str(pt + 1) + " is linear. Linear molecules not yet supported.")
        else:
            if self.debug: print("Generating pes")
            L = self.getLlist()
            pes = self.generatePESCoordinates_Psi4(equil)

        return equil, pes
    # End of former molecule_gui


#TODO take the values in Eignevalues and Eigenvectos and write them to a CSV file in main on line 104.
class OutputData:
    def __init__(self):
        self.num_eigenvalues = 0
        self.eigenvalues = []
        self.eigenvectors = []

    def setEigenvalues(self, evalues):
        self.eigenvalues = evalues
        return

    def setEigenvectors(self, evectors):
        self.eigenvectors = evectors
        return

    def setNumberOfEigenvalues(self, num):
        self.num_eigenvalues = num
        return

    def getEigenvalue(self, idx):
        return self.eigenvalues[idx]

    def getEigenvalues(self):
        return self.eigenvalues

    def getEigenvector(self, idx):
        return self.eigenvectors[idx]

    def getEigenvectors(self):
        return self.eigenvectors

    def getNumberOfEigenvalues(self):
        return self.num_eigenvalues

    def getOutputAsJson(self):
        return {
            "num_eigenvalues": self.num_eigenvalues,
            "eigenvalues": self.eigenvalues,
            "eigenvectors": self.eigenvectors
        }

    def generateValues(self, holder):
        D = holder.getD()
        N = holder.getNlist()
        L = holder.getLlist()
        Npts = np.prod(N)
        Neig = self.getNumberOfEigenvalues()
        eigvals = self.getEigenvalues()
        eigvecs = self.getEigenvectors()
        wfnorder = np.argsort(eigvals)
        freq = np.zeros(Neig, dtype=float)

        for i in range(Neig):
            freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
            print("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))

        self.setEigenvalues(freq)

        wfn = np.zeros([Neig, Npts], dtype=float)
        wfn2 = np.zeros([Neig, Npts, D + 1], dtype=float)

        for p in range(Neig):
            for alpha in range(Npts):
                wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

                q = holder.getPES().getPointByPt(alpha).getQList()
                for d in range(D):
                    wfn2[p][alpha][d] = q[d]
                wfn2[p][alpha][D] = eigvecs[alpha][wfnorder[p]]

        for p in range(Neig):
            norm = 0
            for pt in range(Npts):
                norm = norm + wfn2[p][pt][D] * wfn2[p][pt][D]
            print(norm)
            norm = 1 / np.sqrt(norm)
            for pt in range(Npts):
                wfn2[p][pt][D] = wfn2[p][pt][D] * norm

        self.setEigenvectors(wfn2)

    def plot_data(self,wfn_no, q_ind, D, N, L, qprojlist):
        wfn = self.getEigenvector(wfn_no)

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
        xlabel = "q{:0d} (bohr)".format(q_ind)
        plot1 = figure.add_subplot(xlabel=xlabel, ylabel="Normalized Wavefunction",title=titlestr)
        plot1.plot(x,y)
        return figure

    def plot_data_contour(self, wfn_no, q_indx, q_indy, D, N, L, qprojlist):

        wfn = self.getEigenvector(wfn_no)

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
