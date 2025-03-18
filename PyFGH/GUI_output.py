import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyFGH import GUI_Classes as guc
import sys


# Output GUI, it does the plotting here but values are generated in DataObject in output object
class App(tk.Tk):
    def close_gui(self):
        self.destroy()
        sys.exit()
    def __init__(self, obj):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.close_gui)
        self.obj = obj
        self.D = self.obj.get("D")
        self.N = self.obj.get("N")
        self.L = self.obj.get("L")
        self.Nplot = self.obj.get("NEigen")

        self.row_current = 0

        plots = []
        for i in range(self.Nplot):
            plots.append(i+1)

        self.wfnframe = guc.ComboboxFrame(self, "Plot Option", plots)
        self.wfnframe.grid(column=0, row=self.row_current)
        self.row_current = self.row_current + 1
        self.wfnframe.set(0)

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
            self.plotframe.grid(column=2, row=0, rowspan=4)


        else:
            plotbutton = guc.ButtonFrame(self, "plot", self.plot_data_2d)
            plotbutton.grid(column=0, row=self.row_current)
            self.row_current = self.row_current + 1

            self.plotframe = ttk.Frame(self, width=500)
            self.plotframe.grid(column=0, row=0)

            self.plotframe = ttk.Frame(self, width=500)
            self.plotframe.grid(column=2, row=0, rowspan=2)


    # Chooses between plot types
    def choice_selector(self):
        self.clear_input()
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

        plotbutton = guc.ButtonFrame(self.pcFrame, "plot", self.plot_data_2d)
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

    # This will choose which projection for scatter
    def select_indvar(self):
        rb_result = int(self.indvarframe.get())
        self.qprojlist = []
        row_count = 0
        for d in [x for x in range(self.D) if x != rb_result]:
            n = (self.N[d]-1)//2
            dx = self.L[d]/self.N[d]
            q = [round((j-n)*dx, 3) for j in range(self.N[d])]
            txt = "q{:0d} projection".format(d+1)
            cb = guc.ComboboxFrame(self.projvarframe, txt, q)
            cb.grid(column=0, row=row_count)
            row_count = row_count + 1
            self.qprojlist.append(cb)

        return

    # This will select the projection that the graph will use for contour
    def projselect(self):
        x = int(self.xframe.get())
        y = int(self.yframe.get())

        self.qprojlist = []
        row_count = 0
        for d in range(self.D):
            if (d != x and d != y):
                n = (self.N[d]-1)//2
                dx = self.L[d]/self.N[d]
                q = [round((j-n)*dx,3) for j in range(self.N[d])]
                txt = "q{:0d} projection".format(d+1)
                cb = guc.ComboboxFrame(self.projvarframe, txt, q)
                cb.grid(column=0, row=row_count)
                row_count = row_count + 1
                self.qprojlist.append(cb)

        return

    # This will simply plot the data as a scatter
    def plot_data_2d(self):
        for child in self.plotframe.winfo_children():
            child.destroy()

        figure = self.obj.plot_data_2d(
            int(self.wfnframe.get()), int(self.indvarframe.get()), self.qprojlist)

        figure_canvas = FigureCanvasTkAgg(figure, self.plotframe)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return

    # This will plot the data as a contour
    def plot_data_contour(self):
        for child in self.plotframe.winfo_children():
            child.destroy()

        fig = self.obj.plot_data_contour(int(self.wfnframe.get()), int(self.xframe.get()),
                                         int(self.yframe.get()), self.qprojlist)

        figure_canvas = FigureCanvasTkAgg(fig, self.plotframe)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return
