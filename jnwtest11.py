import csv
import math
import os
import numpy as np
from util import pyfghutil, DataObject

# Proposed replacement for molecule_gui

Q1 = []
Q2 = []
Q3 = []
Z = []
s = []
A = []
m = []
list2 = []
list3 = []
x_coordinates = []
y_coordinates = []
z_coordinates = []
mass = []
potx1 = []
potx2 = []
potx3 = []
poty1 = []
poty2 = []
poty3 = []
potenergy = []
energy = []
totalN = 0

"""
When selecting the files must select first and then select enter N and L values!!!
"""

class ValidationError(Exception):
    pass

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
            reader = csv.reader(f,delimiter=',')
            Nat = 1
            for row in reader:
                try:
                    S.append(row[0])
                    A.append(int(row[1]))
                    x.append(float(row[2]))
                    y.append(float(row[3]))
                    z.append(float(row[4]))
                except IndexError:
                    raise ValidationError('In Equil File: Missing Data on Line {0}'.format(Nat))
                Nat = Nat + 1

    except FileNotFoundError:
        raise

    eqmol = pyfghutil.Molecule()
    eqmol.setNatom(Nat)
    eqmol.setSymbolList(S)
    eqmol.setMassNoList(A)
    eqmol.setXList(x)
    eqmol.setYList(y)
    eqmol.setZList(z)
    for n in range(Nat):
        symbolFound = False
        for key, value in pyfghutil.AtomicSymbolLookup.items():
            if (value == S[n]):
                Z.append(key)
                symbolFound = True
                break
        if (not symbolFound):
            raise ValidationError('Atom {0} Symbol {1} Not Found In Dictionary'.format(n+1,S[n]))

    for n in range(Nat):
        nucl = S[n] + "-" + str(A[n])
        m.append(pyfghutil.MassLookup.get(nucl))
        if (m[n] == None):
            raise ValidationError('Atom {0} Nuclide {1} Not Found In Dictionary'.format(n+1,nucl))
        else:
            m[n] = float(m[n]) * 1822.89

    return eqmol

def readPESfile(pesfile, equil, D, N):
    Npts = np.prod(N)
    Nat = equil.getNatom()

    pes = pyfghutil.PotentialEnergySurface()
    pes.setN(N)
    try:
        with open(pesfile, newline='') as f:
            reader = csv.reader(f)

            n = 0
            for row in reader:
                pespt = pyfghutil.PESpoint()
                pespt.setN(n)

                try:
                    q = np.zeros(D, dtype=float)
                    for i in range(D):
                        q[i] = float(row[i])


                    x = np.zeros(Nat, dtype=float)
                    y = np.zeros(Nat, dtype=float)
                    z = np.zeros(Nat, dtype=float)

                    for i in range(Nat):
                        x[i] = float(row[D+3*i])
                        y[i] = float(row[D+3*i+1])
                        z[i] = float(row[D+3*i+2])

                    en = float(row[D+3*Nat])
                except IndexError:
                    raise ValidationError("In PES file: Missing data on line {0}".format(n+1))
                    os._exit(0)

                pespt.setQList(q)
                pespt.setXList(x)
                pespt.setYList(y)
                pespt.setZList(z)
                pespt.getMolecule().setNatom(Nat)
                pespt.getMolecule().setSymbolList(equil.getSymbolList())
                pespt.getMolecule().setAtomicNumberList(equil.getAtomicNumberList())
                pespt.getMolecule().setMassNumberList(equil.getMassNumberList())
                pespt.getMolecule().setMassList(equil.getMassList())
                pespt.setEnergy(en)
                pes.appendPESpt(pespt)
                n = n + 1
    except FileNotFoundError:
        raise

    if (Npts != n):
        raise ValidationError("Error: Expecting {0} lines in PES file, received {1}".format(Npts,n))

    return pes

def closeContactTest(mol, no, dist_cutoff):
    Nat = mol.getNatom(mol)
    x = mol.getXList(mol)
    y = mol.getYList(mol)
    z = mol.getZList(mol)
    for i in range(Nat):
        for j in range(i+1,Nat):
            d = np.sqrt((x[j]-x[i])*(x[j]-x[i]) + (y[j]-y[i])*(y[j]-y[i]) + (z[j]-z[i])*(z[j]-z[i]))
            if (d < dist_cutoff):
                if (no < 0):
                    raise ValidationError("Error: In equil structure, distance between atom {0} and atom {1} is less than the cutoff distance of {2}".format(i+1,j+1,dist_cutoff))
                else:
                    raise ValidationError("Error: In PES point {0}, distance between atom {1} and atom {2} is less than the cutoff distance of {3}".format(no+1,i+1,j+1,dist_cutoff))

    return




def molecule_testing_v1(D, N, L, eqfile, pesfile):
    Npts = np.prod(N)

    equil = readEqfile(eqfile)
    pes = readPESfile(pesfile, equil, D, N)

    dist_cutoff = 0.10
    closeContactTest(equil, -1, dist_cutoff)

    for i in range(Npts):
        closeContactTest(pes.getPointByPt(i).getMolecule(), i, dist_cutoff)

    holder = DataObject.InputData()
    holder.setD(D)
    holder.setNList(N)
    holder.setLList(L)
    holder.setEquilMolecule(equil)
    holder.setPES(pes)

    return holder

def molecule_testing_v2(holder):
    D = holder.getD()
    N = holder.getNList()
    Npts = np.prod(N)

    equil = readEqfile(holder.getEquilFile())
    pes = readPESfile(holder.getPESFile(), equil, D, N)

    dist_cutoff = 0.10
    closeContactTest(equil, -1, dist_cutoff)

    for i in range(Npts):
        closeContactTest(pes.getPointByPt(i).getMolecule(), i, dist_cutoff)

    holder.setEquilMolecule(equil)
    holder.setPES(pes)

    return

def molecule_testing_old(N1, L1, N2, L2, N3, L3, eqfile, pesfile):
    #print(DataObject.test.equilibrium_file)
    N1_1 = N1
    N2_1 = N2
    N3_1 = N3
    #print(N1_1)
#    with open(DataObject.test.equilibrium_file) as f:
    with open(eqfile) as f:
        for row in f:
            #print(row)
            list2.append(row.split(',')[0])  # Li
            new_row = ['-'.join([row.split(',')[0], row.split(',')[1]])]
            x = ' '.join(new_row)
            list3.append(x)
            x_coordinates.append(row.split(',')[2])
            y_coordinates.append(row.split(',')[3])
            z_coordinates.append((row.split(',')[4]).strip())
            mass.append(row.split(',')[1])
            masslist = ([float(x) for x in mass])
            # print(list2)  # ['Li']
            #print(list3)  # ['Li-6']
            #print("\n")

        """
        for x in list2:
            print(x)
        """

        for x in list2:  # x is the atomic symbol
            if x in pyfghutil.AtomicSymbolLookup.values():
                #print(x + " is a valid element")
                s.append(x)
            else:
                raise Exception("Atom is not valid")
                # throw an error

        print("\n")
        for x in list2:  # x is the atomic symbol
            for key, value in pyfghutil.AtomicSymbolLookup.items():
                if x == value:
                    Z.append(key)
                    #print("Atomic number of " + x + ":", key)

        print("\n")
        for x in list3:  # x is the atomic symbol
            for key, value in pyfghutil.MassLookup.items():
                if value is masslist:
                    #raise Exception("Atom is not valid")
                    pass
                """
                else:
                    raise Exception("Atom is not valid")
                """
                if x == key:
                    A.append(value)
                    #print("Atomic mass of " + x + ":", value)
        """
        print("\n")
        for x in list3:
            for key, value in pyfghutil.MassLookup.items():
                if x == key:
                    print(x + " is a valid element")
                    if value in masslist:
                        print("valid atomic mass")
        """
        for x in A:
            atomic = x * 1822.89
            m.append(atomic)
            #print("amu to atomic ", m)

    def getNs():
#        file = open(DataObject.test.potential_energy_file)
        file = open(pesfile)
        reader = csv.reader(file)
        lines = len(list(reader))
        f.close()
        totalN_2 = N1_1 * N2_1 * N3_1
        if lines == totalN_2:
            #print("The lines of waterpot-data equals the total of all N vales")
            pass
        else:
            #print("The lines of waterpot-data do not equal the total of all N vales ", lines)
            #raise Exception("N is not valid")
            pass
            # come back and fix this
        return totalN_2

    def calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3):
        d = math.sqrt(math.pow(x2 - x1, 2) +
                      math.pow(y2 - y1, 2) +
                      math.pow(z2 - z1, 2))

        d2 = math.sqrt(math.pow(xx3 - x1, 2) +
                       math.pow(yy3 - y1, 2) +
                       math.pow(zz3 - z1, 2))

        d3 = math.sqrt(math.pow(xx3 - xx2, 2) +
                       math.pow(yy3 - yy2, 2) +
                       math.pow(zz3 - zz2, 2))
        # cos theta equation
        costheta = (((x2 - x1) * (xx3 - x1) + (y2 - y1) * (yy3 - y1) + (z2 - z1) * (zz3 - z1)) / (d * d2))
        #print("Cos Theta is: ", costheta)

        if -1 < costheta < 1:
            #print('molecule is non-linear')
            #print("Cos Theta is: ", costheta)
            pass
        else:
            raise Exception("Molecular is linear")
            # throw an error

        if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
            #print("Distance is", d + d2 + d3, " Atom is unique")
            pass
        else:
            raise Exception("Atom is not unique")
            #throw an error

        return

            # First atom is assumed to be the central atom

    xlist = [float(x) for x in x_coordinates]
    ylist = [float(x) for x in y_coordinates]
    zlist = [float(x) for x in z_coordinates]

    # Driver Code
    x1 = xlist[0]
    y1 = ylist[0]
    z1 = zlist[0]
    x2 = xlist[1]
    y2 = ylist[1]
    z2 = zlist[1]

    xx2 = xlist[1]
    yy2 = ylist[1]
    zz2 = zlist[1]
    xx3 = xlist[2]
    yy3 = ylist[2]
    zz3 = zlist[2]

    """
    Splices the data in the waterpot-data.csv file
    """

    def hi():
        holder = DataObject.InputData()
        r = holder.potential_energy_file
        #print(r)
#        hola = open(DataObject.test.potential_energy_file)
#        hola = open(pesfile)
        with open(pesfile) as hola:
            for hello in hola:
                potx1.append(hello.split(',')[3])
                potx2.append(hello.split(',')[5])
                potx3.append(hello.split(',')[7])

                poty1.append(hello.split(',')[4])
                poty2.append(hello.split(',')[6])
                poty3.append(hello.split(',')[8])
                energy.append(hello.split(',')[9])
        return

    hi()

    potxlist1 = [float(x) for x in potx1]
    potxlist2 = [float(x) for x in potx2]
    potxlist3 = [float(x) for x in potx3]

    potylist1 = [float(x) for x in poty1]
    potylist2 = [float(x) for x in poty2]
    potylist3 = [float(x) for x in poty3]
    potenergy = [float(x) for x in energy]

    """
    This does validation checking. Calculates the distance and the cos theta
    """

    def calculations2(x1, y1, x2, y2, x3, y3):
        d = math.sqrt(math.pow(x2 - x1, 2) +
                      math.pow(y2 - y1, 2))

        d2 = math.sqrt(math.pow(x3 - x1, 2) +
                       math.pow(y3 - y1, 2))

        d3 = math.sqrt(math.pow(x3 - x2, 2) +
                       math.pow(y3 - y2, 2))

        # cos theta equation
        costheta = (((x2 - x1) * (x3 - x1) + (y2 - y1) * (y3 - y1)) / (d * d2))
        #print("Cos Theta is: ", costheta)

        if -1 < costheta < 1:
            #print('molecule is non-linear')
            #print("Cos Theta is: ", costheta)
            pass
        else:
            #print("Molecule is linear")
            raise Exception("Molecule is linear")

        if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
            #print("Distance is", d + d2 + d3, " Atom is unique")
            pass
        else:
            #print("Atom is not unique")
            raise Exception("Atom is not unique")

        return

            # First atom is assumed to be the central atom

    """
    This does validation checking for the waterpot-data.csv file
    """
    for x in range(
            len(potxlist1) and len(potxlist2) and len(potxlist3) and len(potylist1) and len(potylist2) and len(
                potylist3)):
        calculations2(potxlist1[x], potylist1[x], potxlist2[x], potylist2[x], potxlist3[x], potylist3[x])
    """
    print("\n")
    print("WaterPot for x1: ", potxlist1)
    print("WaterPot for x2: ", potxlist2)
    print("WaterPot for x3: ", potxlist3)
    print("WaterPot for y1: ", potylist1)
    print("WaterPot for y2: ", potylist2)
    print("WaterPot for y3: ", potylist3)
    print("\n")
    print("X Coordinates of the elements: ", xlist)
    print("Y Coordinates of the elements: ", ylist)
    print("Z Coordinates of the elements: ", zlist)
    print("\n")
    print("Atomic Number: ", Z)  # Atomic Number
    print("Atomic Mass: ", A)  # Atomic Mass
    print("Symbol: ", s)  # Symbol
    """
    calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3)

    EquilMolecule = pyfghutil.Molecule()
    EquilMolecule.setAtomicNoList(Z)
    EquilMolecule.setMassNoList(A)
    EquilMolecule.setMassList(m)
    EquilMolecule.setXList(xlist)
    EquilMolecule.setYList(ylist)
    EquilMolecule.setZList(np.zeros(3,dtype=float))

    #print("This is from the molecule gui: ", EquilMolecule.Z)
    getNs()

    # validateQ()

    """
    This is for validating the water potential energy file
    """
    N1_2 = N1
    L1_2 = L1
    N2_2 = N2
    L2_2 = L2
    N3_2 = N3
    L3_2 = L3

    deltaQ1 = L1_2 / float(N1_2)
    deltaQ2 = L2_2 / float(N2_2)
    deltaQ3 = L3_2 / float(N3_2)
#    with open(DataObject.test.potential_energy_file) as a:
    with open(pesfile) as a:
        for x in a:
            Q1.append(float(x.split(',')[0]))
            Q2.append(float(x.split(',')[1]))
            Q3.append(float(x.split(',')[2]))

    pes = pyfghutil.PotentialEnergySurface()
    pes.setN([N1,N2,N3])
    pes.setNpts(N1*N2*N3)
    n = 0
    for i in range(N1_2):
        for j in range(N2_2):
            for k in range(N3_2):
                q1 = deltaQ1 * float(i - int(N1_2 / 2))
                q2 = deltaQ2 * float(j - int(N2_2 / 2))
                q3 = deltaQ3 * float(k - int(N3_2 / 2))

                if (round(q1, 3) == round(Q1[n], 3)) \
                        and (round(q2, 3) == round(Q2[n], 3))\
                        and (round(q3, 3) == round(Q3[n], 3)):
                    pass
                else:
                    #print(round(q1, 3), round(Q1[n], 3), round(q2, 3), round(Q2[n], 3), round(q3, 3), round(Q3[n], 3))
                    print("Error!!!!!!!!!!!!!!!, File is NOT Valid")
                    os._exit(0)
                    #print('Values are not valid')


                pt = pyfghutil.PESpoint()
                pt.setN(n)
                pt.setQList([q1, q2, q3])
                pt.setXList([potxlist1[n],potxlist2[n],potxlist3[n]])
                pt.setYList([potylist1[n], potylist2[n], potylist3[n]])
                pt.setZList([0, 0, 0])
                pt.setEnergy(potenergy[n])
                pes.appendPESpt(pt)
                n += 1

    return EquilMolecule, pes


def setMessage(param):
    return None


eqfile = "./testing files/water-equxl.csv"
equil = readEqfile(eqfile)
print(equil.getXList())