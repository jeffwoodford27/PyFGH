import csv
import time
import tracemalloc
import PyFGH.GUI as GUI
import numpy as np
import PyFGH.GUItoCalc as GTC
import PyFGH.molecule_gui as molecule_gui


# This is the parent process
def datamuncher(holder):
    ReturnObj = GTC.passToCalc(holder)

    return ReturnObj


# this is the parent process

def datagrabber(holder=None):
    if holder is None:
        holder = GUI.main_window()
        holder.GUI = True
    else:
        eq, pes = molecule_gui.molecule_testing(holder)
        holder.setEquilMolecule(eq)
        holder.setPES(pes)
        holder.GUI = False

    ResultObj = datamuncher(holder)

    eigvals = ResultObj.getEigenvalues()
    eigvecs = ResultObj.getEigenvectors()
    Neig = ResultObj.getNumberOfEigenvalues()

    wfnorder = np.argsort(eigvals)
    D = holder.getD()
    N = holder.getNlist()
    Npts = np.prod(N)

    freq = np.zeros(Neig, dtype=float)

    for i in range(Neig):
        freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
        print("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))

    wfn = np.zeros([Neig, Npts], dtype=float)

    for p in range(Neig):
        for alpha in range(Npts):
            wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

    if holder.gui == True:
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
            raise "Could not write eigenvalues or eigenfunctions to files."

    return wfn, freq


if __name__ == '__main__':
    tracemalloc.start()
    t0 = time.perf_counter()
    datagrabber()
    t1 = time.perf_counter()
    print('done. wall clock time = ' + str(t1-t0))
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()