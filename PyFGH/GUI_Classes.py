import tkinter as tk
from tkinter import ttk


class TextBoxFrame(ttk.LabelFrame):
    def __init__(self, container, txt):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.txtboxstrvar = tk.StringVar()
        self.txtbox = ttk.Entry(self, width=10, textvariable=self.txtboxstrvar)
        self.txtbox.grid(column=0, row=0)

    def get(self):
        return self.txtbox.get()

    def clear(self):
        self.txtboxstrvar.set('')
        return


class LabelFrame(ttk.Frame):
    def __init__(self, container, txt):
        super().__init__(container)

        self.lbl = ttk.Label(self, text=txt)
        self.lbl.grid(column=0, row=0)


class ButtonFrame(ttk.Frame):
    def __init__(self, container, txt, f):
        super().__init__(container)

        self.txtboxbutton = ttk.Button(self, text=txt, command=f)
        self.txtboxbutton.grid(column=0, row=0)


class ComboboxFrame(ttk.LabelFrame):
    def __init__(self, container, txt, dropdownlist):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.cboxstrvar = tk.StringVar()
        self.cbox = ttk.Combobox(self, values=dropdownlist, width=30, textvariable=self.cboxstrvar)
        self.cbox.state(['readonly'])
        self.cbox.grid(column=0, row=0, sticky=tk.NSEW)

    def get(self):
        return self.cbox.get()

    def clear(self):
        self.cboxstrvar.set('')
        return

    def current(self, *args):
        return self.cbox.current(*args)


class ListboxFrame(ttk.LabelFrame):
    def __init__(self, container, txt, dropdownlist):
        super().__init__(container)

        self.config(text=txt)
        self.config(labelanchor=tk.N)

        self.list_items = tk.Variable(value=dropdownlist)

        self.listbox = tk.Listbox(self, height=1, listvariable=self.list_items)
        self.listbox.grid(column=0, row=0, sticky=tk.N)


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