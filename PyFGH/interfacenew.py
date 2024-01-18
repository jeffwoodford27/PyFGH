import tkinter as tk

class App:
  def __init__(self, master):
    frame = tk.Frame(master)
    frame.pack()
    self.button = tk.Button(frame,
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack(side="left")
    self.slogan = tk.Button(frame,
                         text="Hello",
                         command=self.write_slogan)
    self.slogan.pack(side="left")
  def write_slogan(self):
    print("Tkinter is easy to use!")

root = tk.Tk()
app = App(root)
root.mainloop()





