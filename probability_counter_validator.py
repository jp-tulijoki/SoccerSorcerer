import pandas as pd
from soccer_data import getHeadToHeadStats
from probability_counter import countOverallProbabilities, countHomeAwayProbabilities, countHeadToHeadProbability

def result(prediction):
    if prediction[0] > prediction[1] and prediction[0] > prediction[2]:
        return "Home_win"
    elif prediction[2] > prediction[0] and prediction[2] > prediction[1]:
        return "Away_win"
    else:
        return "Draw"

stats = pd.read_csv("stats.csv")
teams = stats["team.name"]

hth_stats_2019 = getHeadToHeadStats("fixtures2019.csv", teams)
hth_stats_2020 = getHeadToHeadStats("fixtures2020.csv", teams)
hth_stats_2021 = getHeadToHeadStats("fixtures2021.csv", teams)

hth_stats = hth_stats_2019 + hth_stats_2020 + hth_stats_2021

fixtures2021 = pd.read_csv("fixtures2021.csv")
fixtures2021 = fixtures2021[(fixtures2021["fixture.status.long"] == "Match Finished")]
home_team_loc = fixtures2021.columns.get_loc("teams.home.name")
away_team_loc = fixtures2021.columns.get_loc("teams.away.name")
home_goals = fixtures2021.columns.get_loc("goals.home")
away_goals = fixtures2021.columns.get_loc("goals.away")

correct = 0

for fixture in fixtures2021.itertuples(index=False):
    home_team = fixture[home_team_loc]
    away_team = fixture[away_team_loc]
    overall = countOverallProbabilities(stats, home_team, away_team)
    home_away = countHomeAwayProbabilities(stats, home_team, away_team)
    hth = countHeadToHeadProbability(hth_stats, home_team, away_team)
    prediction = (overall[0] + home_away[0] + hth[0]) / 3, (overall[1] + home_away[1] + hth[1]) / 3, (overall[2] + home_away[2] + hth[2]) / 3
    if result(prediction) == "Home_win" and fixture[home_goals] > fixture[away_goals]:
        correct += 1
    if result(prediction) == "Draw" and fixture[home_goals] == fixture[away_goals]:
        correct += 1
    if result(prediction) == "Away_win" and fixture[home_goals] < fixture[away_goals]:
        correct += 1

print(f"Probability model accuracy: {correct / fixtures2021.shape[0]}")

 
