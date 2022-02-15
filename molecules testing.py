import csv
from typing import List
from util import pyfghutil

list2: list[str] = []
with open("molecules.csv") as f:
    for row in f:
        list2.append(row[0])
    for x in list2:
        if x in pyfghutil.AtomicSymbolLookup.values():
            print(f"'{x}' is a valid element")
        else:
            print(f"'{x}' is not a valid element")

print(list2)