import csv
import os
import PyFGH.GUI as GUI
import numpy as np
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
def datamuncher(holder):

    print(holder.message)

    """
    print("N1: ", holder1.N1)
    print("L1: ", holder1.L1)
    print("N2: ", holder1.N2)
    print("L2: ", holder1.L2)
    print("N3: ", holder1.N3)
    print("L3: ", holder1.L3)
    """

    ReturnObj = GTC.passToCalc(holder)


    return ReturnObj


# this is the parent process
class Tcl_AsyncDelete:
    pass


def datagrabber(holder=None):
    if holder is None:
        holder = GUI.main_window()
    else:
        eq, pes = molecule_gui.molecule_testing(holder)
        holder.setEquilMolecule(eq)
        holder.setPES(pes)

    print('The interface is started Process: ', os.getpid())

    holder.setMessage("This is from the parent")

    ResultObj = datamuncher(holder)

    eigvals = ResultObj.getEigenvalues()
    eigvecs = ResultObj.getEigenvectors()
    Neig = ResultObj.getNumberOfEigenvalues()

    wfnorder = np.argsort(eigvals)
    D = holder.getD()
    N = holder.getNlist()
    Npts = np.prod(N)



    try:
        from pathlib import Path

        filepath = Path(__file__).parent / "./outputfiles/Eigenvalues.csv"

        with open(filepath, "r") as f:
            with open(f.name, 'w',
                      newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                for i in range(Neig):
                    val = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
                    writer.writerow([val])
    except:
        pass



    freq = np.zeros(Neig, dtype=float)

    for i in range(Neig):
        freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
        print(freq[i])

    wfn = np.zeros([Neig, Npts], dtype=float)

    for p in range(Neig):
        for alpha in range(Npts):
            wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

    #filename = "./outputfiles/Eigenvector-" + str(p) + ".csv"

    try:
        from pathlib import Path
        for p in range(Neig):
            file = Path(__file__).parent / "./outputfiles/Eigenvector-"
            filepath = str(file) + str(p) + ".csv"

            with open(filepath, "r") as f:
                with open(f.name, 'w', newline='', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    for pt in range(Npts):
                        q = holder.getPES().getPointByPt(pt).getQList()
                        row = []
                        for d in range(D):
                            row.append(q[d])
                        row.append(wfn[p][pt])
                        writer.writerow(row)
    except:
        pass



    return wfn, freq


if __name__ == '__main__':
    datagrabber()
    print('done')
