import csv
import time
import tracemalloc
import PyFGH.GUI as GUI
import numpy as np
import PyFGH.GUItoCalc as GTC
import PyFGH.molecule_gui as molecule_gui
import PyFGH.util.pyfghutil as pyfghutil
import numpy.ma as ma

import PyFGH.util.DataObject as DataObject

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RadioButtonFrame(ttk.LabelFrame):
    def __init__(self, container, txt, opts, cmd):
        super().__init__(container)

        self.config(text=txt)

        self.rvar = tk.StringVar()
        self.rlist = []

        for i in range(len(opts)):
            r = ttk.Radiobutton(self,text=opts[i][0], value=opts[i][1], variable=self.rvar, command=cmd)
            r.grid(column=0, row=i)
            self.rlist.append(r)

    def get(self):
        return self.rvar.get()

    def clear(self):
        self.rvar.set("")
        return

class ComboboxFrame(ttk.LabelFrame):
    def __init__(self, container, txt, dropdownlist):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.cboxstrvar = tk.StringVar()
        self.cbox = ttk.Combobox(self, textvariable=self.cboxstrvar)
        self.cbox['values'] = dropdownlist
        self.cbox.state(['readonly'])
        self.cbox.grid(column=0, row=0)

    def get(self):
        return self.cbox.get()

    def clear(self):
        self.cboxstrvar.set('')
        return

    def current(self, *args):
        return self.cbox.current(*args)

class ButtonFrame(ttk.Frame):
    def __init__(self, container, txt, f):
        super().__init__(container)

        self.txtboxbutton = ttk.Button(self, text=txt, command=f)
        self.txtboxbutton.grid(column=0, row=0)

class App(tk.Tk):
    def __init__(self, D, N, L, obj):
        super().__init__()

        self.D = D
        self.N = N
        self.L = L
        self.obj = obj
        self.Nplot = self.obj.getNumberOfEigenvalues()

        row_current = 0

        plots = []
        for i in range(self.Nplot):
            plots.append(('Plot {:0d}'.format(i), '{:0d}'.format(i)))

        self.wfnframe = RadioButtonFrame(self, "Plot Option", plots, self.null)
        self.wfnframe.grid(column=0, row=row_current)
        row_current = row_current + 1

        if (self.D > 1):
            qlist = []
            for i in range(self.D):
                qlist.append(('q{:0d}'.format(i+1), '{:0d}'.format(i)))

            self.indvarframe = RadioButtonFrame(self,"Independent Variable",qlist, self.clear_projvarframe)
            self.indvarframe.grid(column=0, row=row_current)
            row_current = row_current + 1

            self.indvarbutton = ButtonFrame(self, "Select", self.select_indvar)
            self.indvarbutton.grid(column=0, row=row_current)
            row_current = row_current + 1

            self.projvarframe = ttk.Frame(self)
            self.projvarframe.grid(column=0, row=row_current)
            row_current = row_current + 1

        plotbutton = ButtonFrame(self, "plot", self.plot_data)
        plotbutton.grid(column=0, row=row_current)
        row_current = row_current + 1

        self.plotframe = ttk.Frame(self, width=500)
        self.plotframe.grid(column=1, row=0)


        print(self.plotframe.winfo_children())

    def null(self):
        return

    def clear_projvarframe(self):
        for child in self.projvarframe.winfo_children():
            child.destroy()
        return

    def select_indvar(self):
        rb_result = int(self.indvarframe.get())

        self.qprojlist = []
        row_count = 0
        for d in [x for x in range(self.D) if x != rb_result]:
            n = (self.N[d]-1)//2
            dx = self.L[d]/self.N[d]
            q = [(j-n)*dx for j in range(self.N[d])]
            txt = "q{:0d} projection".format(d+1)
            cb = ComboboxFrame(self.projvarframe, txt, q)
            cb.grid(column=0, row=row_count)
            row_count = row_count + 1
            self.qprojlist.append(cb)

        return

    def plot_scatter_old(self, no):
        figure = Figure(figsize=(6,4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.plotframe)
        wfn = self.obj.getEigenvector(no)
        N = wfn.shape[0]
        titlestr = "Wavefunction " + str(no)
        x = np.zeros(N,dtype=float)
        y = np.zeros(N,dtype=float)
        for i in range(N):
            x[i] = wfn[i][0]
            y[i] = wfn[i][1]
        plot1 = figure.add_subplot(xlabel="q (bohr)", ylabel="Normalized Wavefunction",title=titlestr)
        plot1.plot(x,y)
        return figure_canvas

    def plot_scatter(self, no, q_ind, x, y):
        figure = Figure(figsize=(6,4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.plotframe)
        titlestr = "Wavefunction {:0d}".format(no)
        xlabel = "q{:0d} (bohr)".format(q_ind)
        plot1 = figure.add_subplot(xlabel=xlabel, ylabel="Normalized Wavefunction",title=titlestr)
        plot1.plot(x,y)
        return figure_canvas

    def plot_data(self):
        for child in self.plotframe.winfo_children():
            child.destroy()

        wfn_no = int(self.wfnframe.get())
        print(wfn_no)
        wfn = self.obj.getEigenvector(wfn_no)

        q_ind = int(self.indvarframe.get())
        q_mask = np.zeros(self.D,dtype=int)
        q_mask[q_ind] = 1
        print(q_ind,q_mask)

        n = (self.N[q_ind]-1)//2
        dx = self.L[q_ind]/self.N[q_ind]
        x = np.array([(j - n) * dx for j in range(self.N[q_ind])],dtype=float)

        q_idx = np.zeros(self.D,dtype=int)
        i = 0
        for d in range(self.D):
            if (d != q_ind):
                q_idx[d] = int(self.qprojlist[i].current())
                i = i + 1
        print(q_idx)

        q_idx_mask = ma.array(q_idx,mask=q_mask)
        y = np.zeros(self.N[q_ind],dtype=float)

        Npts = np.prod(self.N)
        for pt in range(Npts):
            idx = np.array(pyfghutil.PointToIndex(self.N, pt),dtype=int)
            idx_mask = ma.array(idx,mask=q_mask)
            if (np.equal(q_idx_mask,idx_mask).all()):
                print(idx)
                y[idx[q_ind]] = wfn[pt][self.D]

        print(x)
        print(y)

        figure_canvas = self.plot_scatter(wfn_no, q_ind, x, y)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        print(self.plotframe.winfo_children())
        return

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
    L = holder.getLlist()
    Npts = np.prod(N)

    freq = np.zeros(Neig, dtype=float)

    for i in range(Neig):
        freq[i] = eigvals[wfnorder[i]] - eigvals[wfnorder[0]]
        print("Eigenvalue #{:d}: {:.1f} cm-1".format(i + 1, freq[i]))

    ResultObj.setEigenvalues(freq)

    wfn = np.zeros([Neig, Npts], dtype=float)
    wfn2 = np.zeros([Neig, Npts, D+1], dtype=float)

    for p in range(Neig):
        for alpha in range(Npts):
            wfn[p][alpha] = eigvecs[alpha][wfnorder[p]]

            q = holder.getPES().getPointByPt(alpha).getQList()
            for d in range(D):
                wfn2[p][alpha][d] = q[d]
            wfn2[p][alpha][D] = eigvecs[alpha][wfnorder[p]]

    for p in range(Neig):
        norm = 0
        for pt in range(Npts):
            norm = norm + wfn2[p][pt][D] * wfn2[p][pt][D]
        print(norm)
        norm = 1/np.sqrt(norm)
        for pt in range(Npts):
            wfn2[p][pt][D] = wfn2[p][pt][D] * norm



    ResultObj.setEigenvectors(wfn2)

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

    obj = App(D, N, L, ResultObj)
    obj.mainloop()

    return wfn, freq


if __name__ == '__main__':
    tracemalloc.start()
    t0 = time.perf_counter()

#    molecule = "NITROGEN"
    molecule = "WATER"

    if (molecule == "NITROGEN"):
        holder = DataObject.InputData()
        holder.setD(1)
        holder.setNlist([15])
        holder.setLlist([0.75])
        holder.setcores_amount(2)
        holder.setequilibrium_file("testingfiles/n2-ccsd-equil.csv")
        holder.setpotential_energy("testingfiles/n2-ccsd-potential.csv")
        holder.setNumberOfEigenvalues(10)
        holder.setEigenvalueMethod(False)
        holder.setVmethod('Read from File')
        holder.setcalculation('Full Method')
        holder.setcalculation2('Read from File')
        datagrabber(holder=holder)
    elif (molecule == "WATER"):
        holder = DataObject.InputData()
        holder.setD(3)
        holder.setNlist([11,11,11])
        holder.setLlist([1.1,1.1,1.65])
        holder.setcores_amount(2)
        holder.setequilibrium_file("testingfiles/water-equil.csv")
        holder.setpotential_energy("testingfiles/water-potential.csv")
        holder.setNumberOfEigenvalues(10)
        holder.setEigenvalueMethod(False)
        holder.setVmethod('Read from File')
        holder.setcalculation('Full Method')
        holder.setcalculation2('Read from File')
        datagrabber(holder=holder)
    else:
        datagrabber()

    t1 = time.perf_counter()
    print('done. wall clock time = ' + str(t1-t0))
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()