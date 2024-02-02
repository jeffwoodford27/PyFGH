
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import ma
from PyFGH import GUI_Classes as guc

from PyFGH.util import pyfghutil


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

        self.wfnframe = guc.RadioButtonFrame(self, "Plot Option", plots, self.null)
        self.wfnframe.grid(column=0, row=row_current)
        row_current = row_current + 1

        if (self.D > 1):
            qlist = []
            for i in range(self.D):
                qlist.append(('q{:0d}'.format(i+1), '{:0d}'.format(i)))

            self.indvarframe = guc.RadioButtonFrame(self,"Independent Variable",qlist, self.clear_projvarframe)
            self.indvarframe.grid(column=0, row=row_current)
            row_current = row_current + 1

            self.indvarbutton = guc.ButtonFrame(self, "Select", self.select_indvar)
            self.indvarbutton.grid(column=0, row=row_current)
            row_current = row_current + 1

            self.projvarframe = ttk.Frame(self)
            self.projvarframe.grid(column=0, row=row_current)
            row_current = row_current + 1

        plotbutton = guc.ButtonFrame(self, "plot", self.plot_data)
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
            cb = guc.ComboboxFrame(self.projvarframe, txt, q)
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
