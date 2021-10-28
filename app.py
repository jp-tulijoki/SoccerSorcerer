import tkinter as tk
from probability_counter import countOverallProbabilities, countHomeAwayProbabilities, countHeadToHeadProbability


class App():
    def __init__(self, future_matches, stats, hth_stats):
        self.window = tk.Tk()
        self.window.title("Soccer sorcerer")
        self.future_matches = future_matches
        self.stats = stats
        self.hth_stats = hth_stats
        self.matchlist = future_matches.values.tolist()
        self.window.geometry("600x600")
        self.var = tk.StringVar(self.window)
        self.var.set(self.matchlist[0])
        self.match_selection = tk.OptionMenu(self.window, self.var, *self.matchlist, command=self.select_match)
        self.match_selection.pack()

    def start(self):
        self.window.mainloop()

    def select_match(self, *args):
        parts = self.var.get().split("'")
        home_team = parts[3]
        away_team = parts[5]
        print(countOverallProbabilities(self.stats, home_team, away_team))
