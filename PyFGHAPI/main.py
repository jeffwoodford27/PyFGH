import csv
import os
import GUI
import numpy as np
from multiprocessing import Process, Queue, Pool
import GUItoCalc as GTC
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

# This is the parent process
def datamuncher(q):
    print('This is the child process: ', os.getpid())
    holder1 = q.get()
    print(holder1.message)

    """
    print("N1: ", holder1.N1)
    print("L1: ", holder1.L1)
    print("N2: ", holder1.N2)
    print("L2: ", holder1.L2)
    print("N3: ", holder1.N3)
    print("L3: ", holder1.L3)
    """

    data = [holder1.equilibrium_file, holder1.N1, holder1.L1, holder1.N2,
            holder1.L2, holder1.N3, holder1.L3]

    save_path = "./resources/"
    file_name = "DataList.txt"
    completeName = os.path.join(save_path, file_name)
    file = open(completeName, "w", encoding="utf-8")
    for x in data:
        file.write('%s\n' % x)
    file.close()

    ReturnObj = GTC.passToCalc(holder1)
    q.put(ReturnObj)

    return

# this is the parent process
def datagrabber():
    q = Queue()
    p1 = Process(target=datamuncher, args=(q,))
    p1.start()
    time.sleep(1)
    holder = GUI.main_window()
    print('The interface is started Process: ', os.getpid())

    holder.setMessage("This is from the parent")
    q.put(holder)

    # At this point, insert the data into the handler

    ResultObj = q.get()  # an object of type OutputData

    wfnorder = np.argsort(ResultObj.eigenvalues)
    Npts = holder.N1*holder.N2*holder.N3

    with open("./output files/Eigenvalues.csv", 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(Npts):
            val = ResultObj.eigenvalues[wfnorder[i]]-ResultObj.eigenvalues[wfnorder[0]]
            writer.writerow([val])

    for i in range(1,11):
        val = ResultObj.eigenvalues[wfnorder[i]]-ResultObj.eigenvalues[wfnorder[0]]
        print(val)

    wfn = np.zeros([Npts, holder.N1, holder.N2, holder.N3], float)

    for p in range(Npts):
        for alpha in range(Npts):
            l = np.mod(alpha, holder.N3)
            f = int(alpha / holder.N3)
            k = np.mod(f, holder.N2)
            f2 = int(f / holder.N2)
            j = np.mod(f2, holder.N1)

            wfn[p][j][k][l] = ResultObj.eigenvectors[alpha][wfnorder[p]]

    dq1 = holder.L1/float(holder.N1)
    dq2 = holder.L2/float(holder.N2)
    dq3 = holder.L3/float(holder.N3)

    for p in range(0,21):
        filename = "./output files/Eigenvector-" + str(p) + ".csv"
        with open(filename, 'w', newline='',encoding='UTF8') as f:
            writer = csv.writer(f)

            for n in range(holder.N1*holder.N2*holder.N3):
                l = np.mod(n, holder.N3)
                f = int(n / holder.N3)
                k = np.mod(f, holder.N2)
                f2 = int(f / holder.N2)
                j = np.mod(f2, holder.N1)

                q1 = dq1 * float(j - int(holder.N1/2))
                q2 = dq2 * float(k - int(holder.N2/2))
                q3 = dq3 * float(l - int(holder.N3/2))
                writer.writerow([q1,q2,q3,wfn[p][j][k][l]])

    return


if __name__ == '__main__':
    datagrabber()
    print('done')
