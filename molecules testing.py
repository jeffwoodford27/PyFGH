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

with open("molecules.csv") as f:
    for row in f:
        list2.append(row.split('-')[0])
        list3.append(row.split(',')[0])
        x_coordinates.append(row.split(',')[2])
        y_coordinates.append(row.split(',')[3])
        z_coordinates.append((row.split(',')[4]).strip())
        mass.append(row.split(',')[1])
        masslist = ([float(x) for x in mass])

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
            else:
                print("not valid atomic mass")
            if x == key:
                holder.A.append(value)
                print("Atomic mass of " + x + ":" , value)

    print("\n")
    for x in list3:
        for key, value in pyfghutil.MassLookup.items():
            if x == key:
                print(x + " is a valid element")
                if value in masslist:
                    print("valid atomic mass")
                else:
                    print("not valid atomic mass")


# Function to find distance
def distance(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3):
    global d, d2
    d = math.sqrt(math.pow(x2 - x1, 2) +
                  math.pow(y2 - y1, 2) +
                  math.pow(z2 - z1, 2) * 1.0)
    d2 = math.sqrt(math.pow(xx3 - xx2, 2) +
                  math.pow(yy3 - yy2, 2) +
                  math.pow(zz3 - zz2, 2) * 1.0)
    if d >= 0.10 and d2 >= 0.10:
        print("Distance is ", d + d2, " Atom is unique")
    else:
        print("Atom is not unique")

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

def dotproduct(x1, y1, z1, x2, y2, z2, xx3, yy3, zz3):
    dot = (x2-x1)*(xx3-x1)+(y2-y1)*(yy3-y1)+(z2-z1)*(zz3-z1) / d*d2
    print("Dot Product is: ", (dot))
    if dot == 1:
        print('molecule is linear')
    if dot == -1:
        print('molecule is linear')




print("\n")
print("X Coordinates of the elements: ", xlist)
print("Y Coordinates of the elements: ", ylist)
print("Z Coordinates of the elements: ", zlist)
print("\n")
print("Atomic Number: ", holder.Z)  # Atomic Number
print("Atomic Mass: ", holder.A)  # Atomic Mass
print("Symbol: ", holder.s)  # Symbol
distance(x1, y1, z1, x2, y2, z2, xx2, yy2, zz2, xx3, yy3, zz3)
dotproduct(x1, y1, z1, x2, y2, z2, xx3, yy3, zz3)
