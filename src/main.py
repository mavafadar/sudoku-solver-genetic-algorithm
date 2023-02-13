from UserInterface import UserInterface

import tkinter as tk
from tkinter import ttk


if __name__ == '__main__':
    root = tk.Tk()
    s = ttk.Style(root)
    s.configure('Green.TButton', font=("Helvetica", 16), background='#26a69a')
    s.configure('Red.TButton', font=("Helvetica", 16), background='#ef5350')
    s.configure('Yellow.TEntry', font=("Helvetica", 16), background='#fff9c4')
    app = UserInterface(root)
    root.mainloop()
