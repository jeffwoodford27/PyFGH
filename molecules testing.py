from util import pyfghutil

holder = pyfghutil.Atom()
Z = []
list2: list[str] = []
list3: list[str] = []
with open("molecules.csv") as f:
    for row in f:
        list2.append(row.split('-')[0])
        list3.append(row.split(',')[0])
    for x in list2:  # x is the atomic symbol
        if x in pyfghutil.AtomicSymbolLookup.values():
            print(x + " is a valid element")
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
            if x == key:
                holder.A.append(value)
                print("Atomic mass of " + x + ":" , value)


print("\n")
print("Atomic Number: ", holder.Z)  # Atomic Number
print("Atomic Mass: ", holder.A)  # Atomic Mass
print("Symbol: ", list2)  # Symbol
