
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

        self.row_current = 0

        plots = []
        for i in range(self.Nplot):
            plots.append(('Plot {:0d}'.format(i), '{:0d}'.format(i)))

        self.wfnframe = guc.RadioButtonFrame(self, "Plot Option", plots, self.null)
        self.wfnframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        if (self.D > 1):
            self.qlist = []
            for i in range(self.D):
                self.qlist.append(('q{:0d}'.format(i+1), '{:0d}'.format(i)))

            clist = [("Scatter Plot", 0), ("Contour Plot",1)]

            self.plotTypeFrame = guc.RadioButtonFrame(self, "Plot Choice", clist, self.clear_input)
            self.plotTypeFrame.grid(column=0, row=self.row_current)
            self.row_current = self.row_current + 1

            self.plotSelectFrame = guc.ButtonFrame(self, "Select", self.choice_selector)
            self.plotSelectFrame.grid(column=0, row=self.row_current)
            self.row_current = self.row_current + 1

            self.pcFrame = ttk.Frame(self)
            self.pcFrame.grid(column=0,row=self.row_current)
            self.row_current = self.row_current + 1

            self.plotframe = ttk.Frame(self, width=500)
            self.plotframe.grid(column=2, row=0, rowspan=2)


        else:
            plotbutton = guc.ButtonFrame(self, "plot", self.plot_data)
            plotbutton.grid(column=0, row=self.row_current)
            self.row_current = self.row_current + 1

            self.plotframe = ttk.Frame(self, width=500)
            self.plotframe.grid(column=0, row=0)

            self.plotframe = ttk.Frame(self, width=500)
            self.plotframe.grid(column=2, row=0, rowspan=2)


    def choice_selector(self):
        result = int(self.plotTypeFrame.get())
        if(result == 0):
            self.scatter_input()
        else:
            self.contour_input()

    def scatter_input(self):
        self.indvarframe = guc.RadioButtonFrame(self.pcFrame, "Independent Variable", self.qlist, self.clear_projvarframe)
        self.indvarframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        self.indvarbutton = guc.ButtonFrame(self.pcFrame, "Select", self.select_indvar)
        self.indvarbutton.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        self.projvarframe = ttk.Frame(self.pcFrame)
        self.projvarframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        plotbutton = guc.ButtonFrame(self.pcFrame, "plot", self.plot_data)
        plotbutton.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1


    def contour_input(self):
        self.xframe = guc.RadioButtonFrame(self.pcFrame, "X Coordinate", self.qlist, self.clear_projvarframe)
        self.xframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        self.yframe = guc.RadioButtonFrame(self.pcFrame, "Y Coordinate", self.qlist, self.clear_projvarframe)
        self.yframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        self.maskframe = guc.ButtonFrame(self.pcFrame, "Projections", self.projselect)
        self.maskframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        self.projvarframe = ttk.Frame(self.pcFrame)
        self.projvarframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1

        plotbutton = guc.ButtonFrame(self.pcFrame, "plot", self.plot_data_contour)
        plotbutton.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1



    def null(self):
        return

    def clear_projvarframe(self):
        for child in self.projvarframe.winfo_children():
            child.destroy()
        return

    def clear_input(self):
        for child in self.pcFrame.winfo_children():
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

    def projselect(self):
        x = int(self.xframe.get())
        y = int(self.yframe.get())

        self.qprojlist = []
        row_count = 0
        for d in range(self.D):
            if (d != x and d != y):
                n = (self.N[d]-1)//2
                dx = self.L[d]/self.N[d]
                q = [(j-n)*dx for j in range(self.N[d])]
                txt = "q{:0d} projection".format(d+1)
                cb = guc.ComboboxFrame(self.projvarframe, txt, q)
                cb.grid(column=0, row=row_count)
                row_count = row_count + 1
                self.qprojlist.append(cb)

        return

    def plot_data(self):
        for child in self.plotframe.winfo_children():
            child.destroy()

        figure = self.obj.plot_data(
            int(self.wfnframe.get()), int(self.indvarframe.get()), self.D, self.N, self.L, self.qprojlist)

        figure_canvas = FigureCanvasTkAgg(figure, self.plotframe)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return

    def plot_data_contour(self):
        for child in self.plotframe.winfo_children():
            child.destroy()

        fig = self.obj.plot_data_contour(int(self.wfnframe.get()), int(self.xframe.get()),
                                         int(self.yframe.get()), self.D, self.N, self.L, self.qprojlist)
        figure_canvas = FigureCanvasTkAgg(fig, self.plotframe)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return
