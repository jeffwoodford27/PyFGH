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
    ResultObj.generateValues(holder.get("PES"))

    if holder.getgui():
        D = ResultObj.get("D")
        N = ResultObj.get("N")
        L = ResultObj.get("L")
        Neig=ResultObj.get("NEigen")
        eigvals=ResultObj.get("EVal")
        wfnorder = np.argsort(eigvals)
        Npts = np.prod(N)
        wfn = ResultObj.get("EVec")


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

                with open(filepath, "w") as f:
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

        obj = GUI_output.App(ResultObj)
        obj.mainloop()


    return ResultObj


if __name__ == '__main__':
    tracemalloc.start()
    t0 = time.perf_counter()
    molecule = ""
    #molecule = "NITROGEN"
    #molecule = "WATER"

    # These are default cases as examples
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
