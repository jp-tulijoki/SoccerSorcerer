import requests
from dotenv import dotenv_values
import json
import pandas as pd
from time import sleep

#   In your .env you need to have two values:
#       API_KEY, your personal key for the API
#       API_URL, which is either 'api-football-v1.p.rapidapi.com' or 
#       'v3.football.api-sports.io' depending on which subscription you have

config = dotenv_values(".env")
API_KEY = config["API_KEY"]
API_URL = config["API_URL"]

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_URL
}

# Utility function to form a valid API URL based on .env config
def makeUrl(endpoint):
    if API_URL == "api-football-v1.p.rapidapi.com":
        return "https://" + API_URL + "/v3" + endpoint
    elif API_URL == "v3.football.api-sports.io":
        return "https://" + API_URL + endpoint
    else:
        raise Exception("Unknown API_URL, check your .env!")

# Works for api sports at least
def getStatus():
    url = makeUrl("/status")
    querystring = {}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data

def getLeagueID(league_name):
    url = makeUrl("/leagues")
    querystring = {
        "name" : league_name
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    if data["results"] != 1:
        print("No league or multiple leagues found")
    return data["response"][0]["league"]["id"]

def getTeams(league_id, season):
    url = makeUrl("/teams")
    querystring = {
        "league" : league_id,
        "season" : season
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data

def getTeamStats(league_id, season, team_id):
    url = makeUrl("/teams/statistics")
    querystring = {
        "league" : league_id,
        "season" : season,
        "team" : team_id
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data

# Save team stats to a .csv, stats and file name given
def saveTeamStatsCSV(teams, name):
    first_team_id = teams["response"][0]["team"]["id"]
    first_team_stats = getTeamStats(244, 2021, first_team_id)
    df = pd.json_normalize(first_team_stats["response"])
    for team_item in teams["response"][1:6]:
        team_id = team_item["team"]["id"]
        team_stats = getTeamStats(244, 2021, team_id)
        next_row = pd.json_normalize(team_stats["response"])
        df = df.append(next_row, ignore_index=True)
    sleep(70) # due to api calls limit
    for team_item in teams["response"][6:]:
        team_id = team_item["team"]["id"]
        team_stats = getTeamStats(244, 2021, team_id)
        next_row = pd.json_normalize(team_stats["response"])
        df = df.append(next_row, ignore_index=True)
    df.to_csv(name + ".csv", sep=",")


#teams = getTeams(244, 2021)
#saveTeamStatsCSV(teams, "stats")

df = pd.read_csv("stats.csv")


probabilities = pd.DataFrame({"team": df["team.name"], "overall_wins": df["fixtures.wins.total"] / df["fixtures.played.total"],
                "home_wins": df["fixtures.wins.home"] / df["fixtures.played.home"], 
                "away_wins": df["fixtures.wins.away"] / df["fixtures.played.away"],
                "overall_draws": df["fixtures.draws.total"] / df["fixtures.played.total"],
                "home_draws": df["fixtures.draws.home"] / df["fixtures.played.home"], 
                "away_draws": df["fixtures.draws.away"] / df["fixtures.played.away"],
                "overall_loses": df["fixtures.loses.total"] / df["fixtures.played.total"],
                "home_loses": df["fixtures.loses.home"] / df["fixtures.played.home"], 
                "away_loses": df["fixtures.loses.away"] / df["fixtures.played.away"]})

while True:
    print("Teams")
    print(probabilities["team"])
    home_index = int(input("Home team index:"))
    away_index = int(input("Away team index:"))
    home_team = probabilities.iloc[home_index, :]
    away_team = probabilities.iloc[away_index, :]
    home_win = (home_team["overall_wins"] + away_team["overall_loses"] + home_team["home_wins"] + away_team["away_loses"]) / 4
    draw = (home_team["overall_draws"] + away_team["overall_draws"] + home_team["home_draws"] + away_team["away_draws"]) / 4
    away_win = (home_team["overall_loses"] + away_team["overall_wins"] + home_team["home_loses"] + away_team["away_wins"]) / 4
    print(f"Probabilities:\n Home team wins: {home_win}\n Draw: {draw}\n Away team wins {away_win}")

#df = pd.read_csv("mariehamn.csv")
#print(df.keys().to_numpy())

#print(df.columns)
#print(df['penalty.scored.total'][0])
#print(df['biggest.loses.away'][0])
#print(df['goals.for.minute.61-75.percentage'][0])
#print(df['failed_to_score.away'][0])