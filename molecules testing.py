import csv
with open('isotopes.csv', newline='') as csvfile:
    pamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in pamreader:
        print(', '.join(row))