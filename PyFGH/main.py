import csv
import time
import tracemalloc
import numpy as np
import PyFGH.GUItoCalc as GTC
import PyFGH.GUI_2 as GUI2
import PyFGH.util.DataObject as DataObject
from PyFGH import GUI_output
from PyFGH import Constants as co

# this is the parent process
def run(holder=None):
    if holder is None:
        win = GUI2.GUI()
        win.mainloop()
        holder = win.DataReturner()
    else:
        holder.setgui(False)

    holder.validate_all()

    ResultObj = GTC.passToCalc(holder)
    ResultObj.generateValues(holder)

    # eigvals = ResultObj.getEigenvalues()
    # eigvecs = ResultObj.getEigenvectors()
    # Neig = ResultObj.getNumberOfEigenvalues()
    #
    # wfnorder = np.argsort(eigvals)
    # D = holder.getD()
    # N = holder.getNlist()
    # L = holder.getLlist()
    # Npts = np.prod(N)
    #
    # freq = np.zeros(Neig, dtype=float)
    #
    # for i in range(Neig):
    #     freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
    #     print("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))
    #
    # ResultObj.setEigenvalues(freq)
    #
    # wfn = np.zeros([Neig, Npts], dtype=float)
    # wfn2 = np.zeros([Neig, Npts, D+1], dtype=float)
    #
    # for p in range(Neig):
    #     for alpha in range(Npts):
    #         wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]
    #
    #         q = holder.getPES().getPointByPt(alpha).getQList()
    #         for d in range(D):
    #             wfn2[p][alpha][d] = q[d]
    #         wfn2[p][alpha][D] = eigvecs[alpha][wfnorder[p]]
    #
    # for p in range(Neig):
    #     norm = 0
    #     for pt in range(Npts):
    #         norm = norm + wfn2[p][pt][D] * wfn2[p][pt][D]
    #     print(norm)
    #     norm = 1/np.sqrt(norm)
    #     for pt in range(Npts):
    #         wfn2[p][pt][D] = wfn2[p][pt][D] * norm
    #
    #
    #
    # ResultObj.setEigenvectors(wfn2)

    if holder.getgui():
        D = holder.get("D")
        N = holder.get("N")
        L = holder.get("L")
        Neig=ResultObj.getNumberOfEigenvalues()
        eigvals=ResultObj.getEigenvalues()
        wfnorder = np.argsort(eigvals)
        Npts = np.prod(N)
        wfn = np.zeros([Neig, Npts], dtype=float)


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
            for p in range(Neig):
                file = Path(__file__).parent / "./outputfiles/Eigenvector-"
                filepath = str(file) + str(p) + ".csv"

                with open(filepath, "r") as f:
                    with open(f.name, 'w', newline='', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        for pt in range(Npts):
                            q = holder.get("PES").getPointByPt(pt).getQList()
                            row = []
                            for d in range(D):
                                row.append(q[d])
                            row.append(wfn[p][pt])
                            writer.writerow(row)
        except:
            raise "Could not write eigenvalues or eigenfunctions to files."

        obj = GUI_output.App(D, N, L, ResultObj)
        obj.mainloop()

    return ResultObj


if __name__ == '__main__':
    tracemalloc.start()
    t0 = time.perf_counter()
    molecule = ""
    #molecule = "NITROGEN"
    #molecule = "WATER"

    if (molecule == "NITROGEN"):
        holder = DataObject.InputData()
        holder.set("D",1)
        holder.set("N",[15])
        holder.set("L",[0.75])
        holder.set("NCores",2)
        holder.set("EqFile","testingfiles/n2-ccsd-equil.csv")
        holder.set("PEFile","testingfiles/n2-ccsd-potential.csv")
        holder.set("NEigen",10)
        holder.set("EigenMethod",co.FMAT)
        holder.set("PEMethod",co.READ)
        run(holder=holder)
    elif (molecule == "WATER"):
        holder = DataObject.InputData()
        holder.set("D",3)
        holder.set("N",[11,11,11])
        holder.set("L",[1.1,1.1,1.65])
        holder.set("NCores",4)
        holder.set("EqFile","testingfiles/water-equil.csv")
        holder.set("PEFile","testingfiles/water-potential.csv")
        holder.set("NEigen",10)
        holder.set("EigenMethod",co.FMAT)
        holder.set("PEMethod",co.READ)
        holder.setgui(True)
        holder.validate_all()
        run(holder=holder)

    else:
        run()

    t1 = time.perf_counter()
    print('done. wall clock time = ' + str(t1-t0))
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()