import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style


def testing(x, y, z):
    # Model 1
    if x == 2 and y == 2 and z == 2:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x300')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        " This is for the harmonic "
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        a = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=a)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="\u03BC for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=75)
        a2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=a2)
        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=145)
        a3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=a3)
        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="K for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.K = K.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.K2 = K2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.K3 = K3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=215)

        Mu.place(x=130, y=10, width=100)
        K.place(x=130, y=40, width=100)
        Mu2.place(x=130, y=75, width=100)
        K2.place(x=130, y=110, width=100)
        Mu3.place(x=130, y=145, width=100)
        K3.place(x=130, y=180, width=100)
        window1.mainloop()
    # Model 2
    if x == 2 and y == 2 and z == 3:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x325')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        a = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=a)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="\u03BC for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=75)
        a2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=a2)
        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=145)
        a3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=a3)
        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="D for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="a for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        a3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.K = K.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.K2 = K2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.D3 = D3.get()
            InputData.output.items.a3 = a3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=250)

        Mu.place(x=130, y=10, width=100)
        K.place(x=130, y=40, width=100)
        Mu2.place(x=130, y=75, width=100)
        K2.place(x=130, y=110, width=100)
        Mu3.place(x=130, y=145, width=100)
        D3.place(x=130, y=180, width=100)
        a3.place(x=130, y=215, width=100)
        window1.mainloop()
    # Model 3
    if x == 2 and y == 3 and z == 2:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x325')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        a = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=a)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="\u03BC for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="a for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        a2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="K for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.K = K.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.K2 = D2.get()
            InputData.output.items.Mu3 = a2.get()
            InputData.output.items.D3 = Mu3.get()
            InputData.output.items.a3 = K3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=250)

        Mu.place(x=130, y=10, width=100)
        K.place(x=130, y=40, width=100)
        Mu2.place(x=130, y=75, width=100)
        D2.place(x=130, y=110, width=100)
        a2.place(x=130, y=145, width=100)
        Mu3.place(x=130, y=180, width=100)
        K3.place(x=130, y=215, width=100)
        window1.mainloop()
    # Model 4
    if x == 2 and y == 3 and z == 3:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x350')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        a = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=a)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="K for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="\u03BC for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="a for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        a2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="D for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="a for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=250)
        b = tk.StringVar()
        c5 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        a3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i4 = tk.StringVar()
        Kbox5 = ttk.Combobox(window1, textvariable=i4)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.K = K.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.D2 = D2.get()
            InputData.output.items.a2 = a2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.D3 = D3.get()
            InputData.output.items.a3 = a3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=280)

        Mu.place(x=130, y=10, width=100)
        K.place(x=130, y=40, width=100)
        Mu2.place(x=130, y=75, width=100)
        D2.place(x=130, y=110, width=100)
        a2.place(x=130, y=145, width=100)
        Mu3.place(x=130, y=180, width=100)
        D3.place(x=130, y=215, width=100)
        a3.place(x=130, y=250, width=100)
        window1.mainloop()
    # Model 5
    if x == 3 and y == 2 and z == 2:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x325')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        z = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=z)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="a for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        a = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="\u03BC for Q\u2082", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="K for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        K2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="K for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.D = D.get()
            InputData.output.items.a = a.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.K2 = K2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.K3 = K3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=250)

        Mu.place(x=130, y=10, width=100)
        D.place(x=130, y=40, width=100)
        a.place(x=130, y=75, width=100)
        Mu2.place(x=130, y=110, width=100)
        K2.place(x=130, y=145, width=100)
        Mu3.place(x=130, y=180, width=100)
        K3.place(x=130, y=215, width=100)
        window1.mainloop()
    # Model 6
    if x == 3 and y == 2 and z == 3:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x350')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        z = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=z)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="a for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        a = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="\u03BC for Q\u2082", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="K for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        K2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="D for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="a for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=250)
        b = tk.StringVar()
        c5 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        a3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i4 = tk.StringVar()
        Kbox5 = ttk.Combobox(window1, textvariable=i4)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.D = D.get()
            InputData.output.items.a = a.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.K2 = K2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.D3 = D3.get()
            InputData.output.items.a3 = a3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=280)

        Mu.place(x=130, y=10, width=100)
        D.place(x=130, y=40, width=100)
        a.place(x=130, y=75, width=100)
        Mu2.place(x=130, y=110, width=100)
        K2.place(x=130, y=145, width=100)
        Mu3.place(x=130, y=180, width=100)
        D3.place(x=130, y=215, width=100)
        a3.place(x=130, y=250, width=100)
        window1.mainloop()
    # Model 7
    if x == 3 and y == 3 and z == 2:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x350')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        z = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=z)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="a for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        a = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="\u03BC for Q\u2082", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="D for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        D2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="a for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        a2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="\u03BC for Q\u2083", font=("Times New Roman", 15)).place(x=50, y=215)
        b = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="K for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=250)
        b = tk.StringVar()
        c5 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        K3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i4 = tk.StringVar()
        Kbox5 = ttk.Combobox(window1, textvariable=i4)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.D = D.get()
            InputData.output.items.a = a.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.D2 = D2.get()
            InputData.output.items.a2 = a2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.K3 = K3.get()
            window1.destroy()
            save_file_prompt()
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=280)

        Mu.place(x=130, y=10, width=100)
        D.place(x=130, y=40, width=100)
        a.place(x=130, y=75, width=100)
        Mu2.place(x=130, y=110, width=100)
        D2.place(x=130, y=145, width=100)
        a2.place(x=130, y=180, width=100)
        Mu3.place(x=130, y=215, width=100)
        K3.place(x=130, y=250, width=100)
        window1.mainloop()
    # Model 9
    if x == 3 and y == 3 and z == 3:
        window1 = tk.Tk()
        style = Style()
        window1.title('PyFGH')
        window1.geometry('300x400')
        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')

        # Water molecule icon in the top left conner
        window1.iconbitmap(default='icon.ico')
        " This is for the harmonic "
        ttk.Label(window1, text="\u03BC for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=5)
        z = tk.StringVar()
        Mutext = ttk.Combobox(window1, width=15, textvariable=z)
        # Entry
        Mu = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="D for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=40)
        b = tk.StringVar()
        c = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        D = ttk.Entry(window1, font=("Times New Roman", 10))
        i1 = tk.StringVar()
        Kbox = ttk.Combobox(window1, textvariable=i1)

        ttk.Label(window1, text="a for Q\u2081:", font=("Times New Roman", 15)).place(x=50, y=75)
        z2 = tk.StringVar()
        Mutext2 = ttk.Combobox(window1, width=15, textvariable=z2)
        # Entry
        a = ttk.Entry(window1, font=("Times New Roman", 10))
        i = tk.StringVar()
        Mubox2 = ttk.Combobox(window1, textvariable=i)

        ttk.Label(window1, text="\u03BC for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=110)
        b = tk.StringVar()
        c2 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        Mu2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox2 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="D for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=145)
        z3 = tk.StringVar()
        Mutext3 = ttk.Combobox(window1, width=15, textvariable=z3)
        # Entry
        D2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Mubox3 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="a for Q\u2082:", font=("Times New Roman", 15)).place(x=50, y=180)
        b = tk.StringVar()
        c3 = ttk.Combobox(window1, width=15, textvariable=b)

        # Entry
        a2 = ttk.Entry(window1, font=("Times New Roman", 10))
        i2 = tk.StringVar()
        Kbox3 = ttk.Combobox(window1, textvariable=i2)

        ttk.Label(window1, text="\u03BC for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=215)
        b2 = tk.StringVar()
        c4 = ttk.Combobox(window1, width=15, textvariable=b2)

        # Entry
        Mu3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox4 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="D for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=250)
        b2 = tk.StringVar()
        c5 = ttk.Combobox(window1, width=15, textvariable=b2)

        # Entry
        D3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i3 = tk.StringVar()
        Kbox5 = ttk.Combobox(window1, textvariable=i3)

        ttk.Label(window1, text="a for Q\u2083:", font=("Times New Roman", 15)).place(x=50, y=285)
        b2 = tk.StringVar()
        c6 = ttk.Combobox(window1, width=15, textvariable=b2)

        # Entry
        a3 = ttk.Entry(window1, font=("Times New Roman", 10))
        i4 = tk.StringVar()
        Kbox6 = ttk.Combobox(window1, textvariable=i4)
        """
        def enter_button():
            InputData.output.items.Mu = Mu.get()
            InputData.output.items.D = D.get()
            InputData.output.items.a = a.get()
            InputData.output.items.Mu2 = Mu2.get()
            InputData.output.items.D2 = D2.get()
            InputData.output.items.a2 = a2.get()
            InputData.output.items.Mu3 = Mu3.get()
            InputData.output.items.D3 = D3.get()
            InputData.output.items.a3 = a3.get()
            window1.destroy()
            save_file_prompt()
            enter_button
        """
        enter = tk.Button(window1, text='Enter', bd='20', bg='green', fg='white',
                          command=window1.destroy).place(x=110, y=325)

        Mu.place(x=130, y=10, width=100)
        D.place(x=130, y=40, width=100)
        a.place(x=130, y=75, width=100)
        Mu2.place(x=130, y=110, width=100)
        D2.place(x=130, y=145, width=100)
        a2.place(x=130, y=180, width=100)
        Mu3.place(x=130, y=215, width=100)
        D3.place(x=130, y=250, width=100)
        a3.place(x=130, y=285, width=100)
        window1.mainloop()

        window1.mainloop()


testing(3, 3, 2)
