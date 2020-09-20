import tkinter as tk


class main_window:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('400x400')
        self.window.configure(background="black")
        self.mainloop()


class top_frame:

    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

