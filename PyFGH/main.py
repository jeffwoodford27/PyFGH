import csv
import os
import PyFGH.GUI as GUI
import numpy as np
from multiprocessing import Process, Queue
import PyFGH.GUItoCalc as GTC
import time

import PyFGH.molecule_gui as molecule_gui

"""
This one uses Queues
This communicates by using SSH
Also connected to test3.py
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""


# TODO fix the name of file. not passing file name.
# TODO fix ssh problem. problem is with pes in remotegmatrix.py

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

    ReturnObj = GTC.passToCalc(holder1)
    q.put(ReturnObj)

    # return


# this is the parent process
class Tcl_AsyncDelete:
    pass


def datagrabber(holder=None):
    q = Queue()
    p1 = Process(target=datamuncher, args=(q,))
    p1.start()
    time.sleep(1)
    if holder is None:
        holder = GUI.main_window()
    else:
        def test():
            try:
                eq, pes = molecule_gui.molecule_testing(holder)
                holder.setEquilMolecule(eq)
                holder.setPES(pes)
            except:
                pass

        test()

    print('The interface is started Process: ', os.getpid())

    holder.setMessage("This is from the parent")
    q.put(holder)

    # At this point, insert the data into the handler
    ResultObj = q.get()  # an object of type OutputData

    eigvals = ResultObj.getEigenvalues()
    eigvecs = ResultObj.getEigenvectors()
    Neig = ResultObj.getNumberOfEigenvalues()

    wfnorder = np.argsort(eigvals)
    N = holder.getNlist()
    L = holder.getLlist()
    Npts = np.prod(N)

    from pathlib import Path

    filepath = Path(__file__).parent / "./output files/Eigenvalues.csv"

    with open(filepath, "r") as f:
        with open(f.name, 'w',
                  newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            for i in range(Neig):
                val = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
                writer.writerow([val])



    freq = np.zeros(Neig, dtype=float)

    for i in range(Neig):
        freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
        print(freq[i])

    wfn = np.zeros([Neig, N[0], N[1], N[2]], float)

    for p in range(Neig):
        for alpha in range(Npts):
            l = np.mod(alpha, N[2])
            f = int(alpha / N[2])
            k = np.mod(f, N[1])
            f2 = int(f / N[1])
            j = np.mod(f2, N[0])

            wfn[p][j][k][l] = eigvecs[alpha][wfnorder[p]]

    dq1 = L[0] / float(N[0])
    dq2 = L[1] / float(N[1])
    dq3 = L[2] / float(N[2])

    #filename = "./output files/Eigenvector-" + str(p) + ".csv"


    for p in range(Neig):
        file = Path(__file__).parent / "./output files/Eigenvector-"
        filepath = str(file) + str(p) + ".csv"

        with open(filepath, "r") as f:
            with open(f.name, 'w', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)

                for n in range(Npts):
                    l = np.mod(n, N[2])
                    f = int(n / N[2])
                    k = np.mod(f, N[1])
                    f2 = int(f / N[1])
                    j = np.mod(f2, N[0])

                    q1 = dq1 * float(j - int(N[0] / 2))
                    q2 = dq2 * float(k - int(N[1] / 2))
                    q3 = dq3 * float(l - int(N[2] / 2))
                    writer.writerow([q1, q2, q3, wfn[p][j][k][l]])



    return wfn, freq


if __name__ == '__main__':
    datagrabber()
    print('done')
