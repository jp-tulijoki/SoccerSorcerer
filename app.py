import tkinter as tk

class App():
    def __init__(self, future_matches):
        self.window = tk.Tk()
        self.window.title("Soccer sorcerer")
        self.future_matches = future_matches
        self.window.geometry("600x600")
        self.var = tk.StringVar(self.window)
        self.var.set(future_matches[0])
        self.match_selection = tk.OptionMenu(self.window, self.var, *self.future_matches)
        self.match_selection.pack()

    def start(self):
        self.window.mainloop()