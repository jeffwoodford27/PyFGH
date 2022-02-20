import self

from util import pyfghutil
import math

# holder = pyfghutil.Atom()
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

# TODO For atom molecule Atom(Z, A, m, x y). Implement this into this here.
# TODO molecules Li 6,  Li 7, Ce 20. Fix this in the program.
# TODO ask the user for two files. File 1 is the equilibrium file or the molecules.csv file
# TODO File 2 is the potential energies file which is the waterpot-data.csv
# TODO do distance test with potential energy file which is x1 and so forth
# TODO waterpot.csv: Q1, Q2, Q3, x1, y1, x2, y2, x3, y3, energies

with open("molecules.csv") as f:
    for row in f:
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
        print(list3)  # ['Li-6']
        print("\n")
    for x in list2:
        print(x)

    for x in list2:  # x is the atomic symbol
        if x in pyfghutil.AtomicSymbolLookup.values():
            print(x + " is a valid element")
            s.append(x)
        else:
            print(x + " is not a valid element")

    print("\n")
    for x in list2:  # x is the atomic symbol
        for key, value in pyfghutil.AtomicSymbolLookup.items():
            if x == value:
                Z.append(key)
                print("Atomic number of " + x + ":", key)

    print("\n")
    for x in list3:  # x is the atomic symbol
        for key, value in pyfghutil.MassLookup.items():
            if value in masslist:
                print("valid atomic mass")

            if x == key:
                A.append(value)
                print("Atomic mass of " + x + ":", value)

    print("\n")
    for x in list3:
        for key, value in pyfghutil.MassLookup.items():
            if x == key:
                print(x + " is a valid element")
                if value in masslist:
                    print("valid atomic mass")
    for x in A:
        atomic = x * 1822.89
        m.append(atomic)
        print("amu to atomic ", m)


"""
This does validation checking. Calculates the distance and the cos theta
"""

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
    print("Cos Theta is: ", costheta)

    if -1 < costheta < 1:
        print('molecule is non-linear')
        print("Cos Theta is: ", costheta)
    else:
        print("Molecule is linear")

    if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
        print("Distance is", d + d2 + d3, " Atom is unique")
    else:
        print("Atom is not unique")

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
with open("waterpot-data.csv", ) as f:
    for x in f:
        potx1.append(x.split(',')[3])
        potx2.append(x.split(',')[5])
        potx3.append(x.split(',')[7])

        poty1.append(x.split(',')[4])
        poty2.append(x.split(',')[6])
        poty3.append(x.split(',')[8])

potxlist1 = [float(x) for x in potx1]
potxlist2 = [float(x) for x in potx2]
potxlist3 = [float(x) for x in potx3]

potylist1 = [float(x) for x in poty1]
potylist2 = [float(x) for x in poty2]
potylist3 = [float(x) for x in poty3]


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
    print("Cos Theta is: ", costheta)

    if -1 < costheta < 1:
        print('molecule is non-linear')
        print("Cos Theta is: ", costheta)
    else:
        print("Molecule is linear")
        raise Exception("Molecule is linear")

    if d >= 0.10 and d2 >= 0.10 and d3 >= 0.10:
        print("Distance is", d + d2 + d3, " Atom is unique")
    else:
        print("Atom is not unique")
        raise Exception("Atom is not unique")

        # First atom is assumed to be the central atom

"""
This does validation checking for the waterpot-data.csv file
"""
for x in range(
        len(potxlist1) and len(potxlist2) and len(potxlist3) and len(potylist1) and len(potylist2) and len(potylist3)):
    calculations2(potxlist1[x], potylist1[x], potxlist2[x], potylist2[x], potxlist3[x], potylist3[x])
    x += 1

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
calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3)
test = pyfghutil.Atom(Z, A, m, xlist, ylist)
print(getattr(test, 'Z'))
