def NInputBox():
    window = tk.Tk()
    x = 2

    style = Style()
    window.title('PyFGH')
    box_len_str = '300x' + str(x * 55 + 70)
    window.geometry(box_len_str)
    # window.geometry('300x450')
    # Label

    fireflies = 0
    for number in range(x):
        ttk.Label(window, text="Input Values For N:", font=("Times New Roman", 15)).place(x=60, y=10)
        d = tk.StringVar()
        N1text = ttk.Combobox(window, width=15, textvariable=d)

        x1 = ttk.Entry(window, font=("Times New Roman", 10))
        c = tk.StringVar()
        N1box = ttk.Combobox(window, textvariable=c)

        ttk.Label(window, text=number + 1, font=("Times New Roman", 15)).place(x=80, y=(40 + fireflies))
        d = tk.StringVar()
        N1text = ttk.Combobox(window, width=15, textvariable=d)

        x1.place(x=100, y=(40 + fireflies), width=100)
        fireflies += 40


def YInputBox():
    window = tk.Tk()
    yvalue = 2

    style = Style()
    window.title('PyFGH')
    box_len_str = '300x' + str(yvalue * 55 + 70)
    window.geometry(box_len_str)
    # window.geometry('300x450')
    # Label

    fireflies = 0
    for number in range(yvalue):
        ttk.Label(window, text="Input Values For Y:", font=("Times New Roman", 15)).place(x=60, y=10)
        d = tk.StringVar()
        N1text = ttk.Combobox(window, width=15, textvariable=d)

        x1 = ttk.Entry(window, font=("Times New Roman", 10))
        c = tk.StringVar()
        N1box = ttk.Combobox(window, textvariable=c)

        ttk.Label(window, text=number + 1, font=("Times New Roman", 15)).place(x=80, y=(40 + fireflies))
        d = tk.StringVar()
        N1text = ttk.Combobox(window, width=15, textvariable=d)

        x1.place(x=100, y=(40 + fireflies), width=100)
        fireflies += 40


def enter_button():
    print()


yvalue = 2
enter = tk.Button(window, text='Enter', bd='20', bg='green', fg='white',
                  command=enter_button).place(x=110, y=(yvalue * 45 + 20))