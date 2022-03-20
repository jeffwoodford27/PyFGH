import csv
import os
import molecule_gui
from multiprocessing import Process, Queue
import RemoteGUItoCalc as GTC
import time
"""
This one uses Queues
This communicates by using SSH
Also connected to test3.py
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""
#TODO fix the name of file. not passing file name.
#TODO fix ssh problem. problem is with pes in remotegmatrix.py


list2 = []
list3 = []

with open('countries.csv') as f:
    for row in f:
        list2.append(row.split(',')[0])
        print(row)
        list2.append(row)

    for element in list2:
        list3.append(element.strip())

list3.pop(0)
list3.pop(2)
list3.pop(1)
list3[0].split(",")

N1 = list3[0][0]
N2 = list3[0][2]
N3 = list3[0][4]

L1 = list3[0][1]
L2 = list3[0][3]
L3 = list3[0][5]

# This is the parent process
def datamuncher(q):
    print('This is the child process: ', os.getpid())
    holder1 = q.get()
    print(holder1.message)
    # print("Filename: ", holder1.file_name)

    print("Energy from Main: ", holder1.PES.pts[0].en)

    ReturnObj = GTC.passToCalc(holder1)
    q.put(ReturnObj)

    # print("File Name : ", holder1.file_name, " This is from the child process")
    # print("Model Data : ", holder1.model_data, " This is from the child process")
    return


# this is the parent process
def datagrabber():
    q = Queue()
    p1 = Process(target=datamuncher, args=(q,))
    p1.start()
    time.sleep(1)
    holder = molecule_gui.molecule_testing(N1, L1, N2, L2, N3, L3)
    print('The interface is started Process: ', os.getpid())

    holder.setMessage("This is from the parent")
    # holder.setModelData(DataObject.holdData.model_data)  # look into pickling possibly un-pickling
    q.put(holder)

    # At this point, insert the data into the handler

    ResultObj = q.get()  # an object of type OutputData

    hola = []
    hola.append('Eigen Vectors: ')
    hola.append(ResultObj.getEigenvectors())
    hi = []
    hi.append('Eigen Values: ')
    print("Eigenvalues:")
    for i in range(1, int(N1) * int(N2) * int(N3)):
        value = ResultObj.eigenvalues[i] - ResultObj.eigenvalues[0]
        print(value)
        hi.append(value)

    with open("./output files/Eigenvalues.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        for word in hi:
            writer.writerow([word])

        # write the data
        # writer.writerow(data)

        # writer.writerow(data2)
        f.close()

    with open("./output files/Eigenvectors.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        for word in hola:
            writer.writerow([word])

        # write the data
        # writer.writerow(data)

        # writer.writerow(data2)
        f.close()



    return


if __name__ == '__main__':
    datagrabber()
    print('done')
