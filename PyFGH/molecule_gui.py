import csv
import numpy as np
from PyFGH.util import pyfghutil as pyfghutil
from PyFGH.util.pyfghutil import ValidationError as ValidationError


def readEqfile(eqfile):
    S = []
    A = []
    Z = []
    x = []
    y = []
    z = []
    m = []
    try:
        with open(eqfile, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            row = next(reader)
            try:
                Q = int(row[0])
                Mult = int(row[1])
            except IndexError:
                raise ValidationError('In Equilibrium File: First Line Should Contain Charge and Multiplicity')
            except ValueError:
                raise ValidationError('In Equilibrium File: First Line Should Contain Charge and Multiplicity')
            if (Mult < 1):
                raise ValidationError('Read Multiplicity of {0}, Should Be A Positive Integer'.format(Mult))

            print("Charge is {0}, Multiplicity is {1}".format(Q, Mult))

            Nat = 0
            for row in reader:
                try:
                    S.append(row[0])
                    A.append(int(row[1]))
                    x.append(float(row[2]))
                    y.append(float(row[3]))
                    z.append(float(row[4]))
                except IndexError:
                    raise ValidationError('In Equilibrium File: Missing Data on Line {0}'.format(Nat + 2))
                except ValueError:
                    raise ValidationError('In Equilibrium File, Wrong Format Found on Line {0}'.format(Nat + 2))
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
            raise ValidationError('Atom {0} Symbol {1} Not Found In Dictionary'.format(n + 1, S[n]))

    eqmol.setAtomicNoList(np.array(Z))

    Nel = np.sum(Z) - Q
    if ((Nel % 2) == (Mult % 2)):
        raise ValidationError('Charge {0} And Multiplicity {1} Are Inconsistent'.format(Q, Mult))

    for n in range(Nat):
        nucl = S[n] + "-" + str(A[n])
        m.append(pyfghutil.MassLookup.get(nucl))
        if (m[n] == None):
            raise ValidationError('Atom {0} Nuclide {1} Not Found In Dictionary'.format(n + 1, nucl))
        else:
            m[n] = float(m[n]) * 1822.89
    eqmol.setMassList(np.array(m))

    return eqmol


def readPESfile(pesfile, equil, D, N):
    Npts = np.prod(N)
    Nat = equil.getNatom()

    pes = pyfghutil.PotentialEnergySurface(N)
    try:
        with open(pesfile, newline='') as f:
            reader = csv.reader(f)

            n = 0
            for row in reader:
                pespt = pyfghutil.PESpoint(n)

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
                except IndexError:
                    raise ValidationError("In PES file: Missing data on line {0}".format(n + 1))
                except ValueError:
                    raise ValidationError('In PES file, Wrong Format Found on Line {0}'.format(n + 1))

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
        raise ValidationError("Error: Expecting {0} lines in PES file, read {1}".format(Npts, n))

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


def generatePESCoordinates_Psi4(D, N, L, equil):
    Nat = equil.getNatom()

    if not (((D == 1) and (Nat == 2)) or ((D == 3) and (Nat == 3))):
        raise ValidationError("Psi4 Calculation Method only implemented for diatomic and triatomic molecules.")

    Npts = np.prod(N)
    xeq = equil.getXList()
    yeq = equil.getYList()
    zeq = equil.getZList()
    Z = equil.getAtomicNoList()
    A = equil.getMassNoList()
    m = equil.getMassList()

    pes = pyfghutil.PotentialEnergySurface(N)
    if (D == 1):
        Req = np.linalg.norm(np.array([xeq[1] - xeq[0], yeq[1] - yeq[0], zeq[1] - zeq[0]]))

        xeq[0] = xeq[1] = yeq[0] = yeq[1] = 0
        zeq[0] = -Req / 2
        zeq[1] = Req / 2

        equil.setXList(xeq)
        equil.setYList(yeq)
        equil.setZList(zeq)

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
            pespt.getMolecule().setCharge(equil.getCharge())
            pespt.getMolecule().setMultiplicity(equil.getMultiplicity())
            pespt.getMolecule().setSymbolList(equil.getSymbolList())
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

        equil.x = xeq
        equil.setYList(yeq)
        equil.setZList(zeq)

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
            pespt.getMolecule().setCharge(equil.getCharge())
            pespt.getMolecule().setMultiplicity(equil.getMultiplicity())
            pespt.getMolecule().setSymbolList(equil.getSymbolList())
            pespt.getMolecule().setAtomicNoList(Z)
            pespt.getMolecule().setMassNoList(A)
            pespt.getMolecule().setMassList(m)
            pespt.setEnergy(0)
            pes.setPESpt(pt, pespt)

    else:
        print ("this shouldn't happen")

    return pes


def closeContactTest(mol, dist_cutoff=0.05):
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


def linearTest(mol, cutoff=0.05):
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


def molecule_testing(holder):
    D = holder.getD()
    N = holder.getNlist()

    eqfile = holder.getEquilFile()
    if (not eqfile):
        raise ValidationError("No Equilibrium Structure file input!")

    equil = readEqfile(eqfile)
    if (closeContactTest(equil) == False):
        raise ValidationError("Atoms less than 0.05 bohr apart in the equilibrium structure.")
    if (linearTest(equil) == False):
        raise ValidationError("The equilibrium structure is linear. Linear molecules not yet supported.")

    if (holder.getVmethod() == "Read from File"):
        pesfile = holder.getPESFile()
        if (pesfile == None):
            raise ValidationError("No Potential Energy file input!")
        pes = readPESfile(pesfile, equil, D, N)
        Npts = np.prod(N)
        for pt in range(Npts):
            mol = pes.getPointByPt(pt).getMolecule()
            if (closeContactTest(mol) == False):
                raise ValidationError("Atoms less than 0.05 bohr apart in PES structure " + str(pt + 1))
#            if (linearTest(mol) == False):
#                raise ValidationError("PES structure " + str(pt + 1) + " is linear. Linear molecules not yet supported.")
    else:
        L = holder.getLlist()
        pes = generatePESCoordinates_Psi4(D, N, L, equil)

    return equil, pes
