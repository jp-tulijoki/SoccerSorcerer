import pandas as pd
from app import App
from soccer_data import getUpcomingFixtures, getHeadToHeadStats

stats = pd.read_csv("stats.csv")
teams = stats["team.name"]
hth_stats_2019 = getHeadToHeadStats("fixtures2019.csv", teams)
hth_stats_2020 = getHeadToHeadStats("fixtures2020.csv", teams)
hth_stats_2021 = getHeadToHeadStats("fixtures2021.csv", teams)
hth_stats = hth_stats_2019 + hth_stats_2020 + hth_stats_2021

future_matches = getUpcomingFixtures("fixtures2021.csv")
future_matches = future_matches[["fixture.date", "teams.home.name", "teams.away.name"]]
future_matches["fixture.date"] = future_matches["fixture.date"].apply(lambda date: date[:10])
app = App(future_matches, stats, hth_stats)
app.start()