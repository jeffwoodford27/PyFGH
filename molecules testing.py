from util import pyfghutil
import math

holder = pyfghutil.Atom()
Z = []
s = []
list2: list[str] = []
list3: list[str] = []
x_coordinates: list[str] = []
y_coordinates: list[str] = []
z_coordinates: list[str] = []
mass: list[str] = []

# TODO For atom molecule Atom(Z, A, m, x y). Implement this into this here.
# TODO molecules Li 6,  Li 7, Ce 20. Fix this in the program.
# TODO ask the user for two files. File 1 is the equilibrium file or the molecules.csv file
# TODO File 2 is the potential energies file which is the waterpot-data.csv
# TODO do distance test with potential energy file which is x1 and so forth
# TODO waterpot.csv: Q1, Q2, Q3, x1, y1, x2, y2, x3, y3, energies

from collections.abc import Iterable


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


with open("molecules.csv") as f:
    for row in f:
        list2.append(row.split(',')[0])  # Li
        # list3.append((row.split(' ')[0]) + (row[1])) # Li-6
        new_row = ['-'.join([row.split(',')[0], row.split(',')[1]])]
        x = ' '.join(new_row)
        list3.append(x)
        x_coordinates.append(row.split(',')[2])
        y_coordinates.append(row.split(',')[3])
        z_coordinates.append((row.split(',')[4]).strip())
        mass.append(row.split(',')[1])
        masslist = ([float(x) for x in mass])
        #print(list2)  # ['Li']
        print(list3)  # ['Li-6']
        print("\n")
    for x in list2:
        print(x)


    for x in list2:  # x is the atomic symbol
        if x in pyfghutil.AtomicSymbolLookup.values():
            print(x + " is a valid element")
            holder.s.append(x)
        else:
            print(x + " is not a valid element")

    print("\n")
    for x in list2:  # x is the atomic symbol
        for key, value in pyfghutil.AtomicSymbolLookup.items():
            if x == value:
                holder.Z.append(key)
                print("Atomic number of " + x + ":", key)

    print("\n")
    for x in list3:  # x is the atomic symbol
        for key, value in pyfghutil.MassLookup.items():
            if value in masslist:
                print("valid atomic mass")

            if x == key:
                holder.A.append(value)
                print("Atomic mass of " + x + ":", value)

    print("\n")
    for x in list3:
        for key, value in pyfghutil.MassLookup.items():
            if x == key:
                print(x + " is a valid element")
                if value in masslist:
                    print("valid atomic mass")


# Function to find distance
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

print("\n")
print("X Coordinates of the elements: ", xlist)
print("Y Coordinates of the elements: ", ylist)
print("Z Coordinates of the elements: ", zlist)
print("\n")
print("Atomic Number: ", holder.Z)  # Atomic Number
print("Atomic Mass: ", holder.A)  # Atomic Mass
print("Symbol: ", holder.s)  # Symbol
calculations(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3)
