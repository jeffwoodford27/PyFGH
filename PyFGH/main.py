import csv
import os
import PyFGH.GUI as GUI
import numpy as np
from multiprocessing import Process, Queue
import PyFGH.GUItoCalc as GTC
import time
import PyFGH.util.pyfghutil as pyfghutil

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
    D = holder.getD()
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

    wfn = np.zeros([Neig, Npts], dtype=float)

    for p in range(Neig):
        for alpha in range(Npts):
            wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

    #filename = "./output files/Eigenvector-" + str(p) + ".csv"

    q = np.zeros(D,dtype=float)
    for i in range(D):
        q[i] = (L[i]/N[i])*(i-N[i]//2)

    for p in range(Neig):
        file = Path(__file__).parent / "./output files/Eigenvector-"
        filepath = str(file) + str(p) + ".csv"

        with open(filepath, "r") as f:
            with open(f.name, 'w', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)

                for pt in range(Npts):
                    idx = pyfghutil.PointToIndex(N,pt)
                    row = []
                    for d in range(D):
                        row.append(q[idx[d]])
                    row.append(wfn[p][pt])
                    writer.writerow(row)



    return wfn, freq


if __name__ == '__main__':
    datagrabber()
    print('done')
