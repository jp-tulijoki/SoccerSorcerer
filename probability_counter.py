import pandas as pd

def countOverallProbabilities(stats, home_team, away_team):
    home_stats = stats[stats["team.name"] == home_team]
    away_stats = stats[stats["team.name"] == away_team]
    home_win = (float(home_stats["fixtures.wins.total"] / home_stats["fixtures.played.total"]) + float(away_stats["fixtures.loses.total"] / away_stats["fixtures.played.total"])) / 2
    draw = (float(home_stats["fixtures.draws.total"] / home_stats["fixtures.played.total"]) + float(away_stats["fixtures.draws.total"] / away_stats["fixtures.played.total"])) / 2 
    away_win = (float(home_stats["fixtures.loses.total"] / home_stats["fixtures.played.total"]) + float(away_stats["fixtures.wins.total"] / away_stats["fixtures.played.total"])) / 2
    return (home_win, draw, away_win)

def countHomeAwayProbabilities(stats, home_team, away_team):
    home_stats = stats[stats["team.name"] == home_team]
    away_stats = stats[stats["team.name"] == away_team]
    home_win = (float(home_stats["fixtures.wins.home"] / home_stats["fixtures.played.home"]) + float(away_stats["fixtures.loses.away"] / away_stats["fixtures.played.away"])) / 2
    draw = (float(home_stats["fixtures.draws.home"] / home_stats["fixtures.played.home"]) + float(away_stats["fixtures.draws.away"] / away_stats["fixtures.played.away"])) / 2 
    away_win = (float(home_stats["fixtures.loses.home"] / home_stats["fixtures.played.home"]) + float(away_stats["fixtures.wins.away"] / away_stats["fixtures.played.away"])) / 2
    return (home_win, draw, away_win)

def countHeadToHeadProbability(head_to_head_stats, home_team, away_team):
    history = head_to_head_stats[home_team][away_team]
    probabilities = (history.count("W") / len(history), history.count("D") / len(history), history.count("L") / len(history))
    return probabilities

df = pd.read_csv("stats.csv")
print(countHomeAwayProbabilities(df, "HJK helsinki", "IFK Mariehamn"))