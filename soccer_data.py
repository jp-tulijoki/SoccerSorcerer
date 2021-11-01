import requests
from dotenv import load_dotenv
import json
import pandas as pd
import numpy as np
from time import sleep
import os

from requests.api import head

#   In your .env you need to have two values:
#       API_KEY, your personal key for the API
#       API_URL, which is either 'api-football-v1.p.rapidapi.com' or 
#       'v3.football.api-sports.io' depending on which subscription you have

load_dotenv()
API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")

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
def saveTeamStatsCSV(teams, name, season):
    first_team_id = teams["response"][0]["team"]["id"]
    first_team_stats = getTeamStats(244, season, first_team_id)
    df = pd.json_normalize(first_team_stats["response"])
    for team_item in teams["response"][1:6]:
        team_id = team_item["team"]["id"]
        team_stats = getTeamStats(244, season, team_id)
        next_row = pd.json_normalize(team_stats["response"])
        df = df.append(next_row, ignore_index=True)
    sleep(70) # due to api calls limit
    for team_item in teams["response"][6:]:
        team_id = team_item["team"]["id"]
        team_stats = getTeamStats(244, season, team_id)
        next_row = pd.json_normalize(team_stats["response"])
        df = df.append(next_row, ignore_index=True)
    df.to_csv(name + ".csv", sep=",")

def getAllFixturesCSV(league_id, season):
    url = makeUrl("/fixtures")
    querystring = {
        "league" : league_id,
        "season" : season,
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    df = pd.json_normalize(data["response"])
    df.to_csv(f"fixtures{season}.csv", sep=",")

# The API is inconsistent with this, sometimes there are 3 different standings, you have to adjust the last index by hand
def getLeaugeStandingsCSV(league_id, season):
    url = makeUrl("/standings")
    querystring = {
        "league" : league_id,
        "season" : season,
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    df = pd.json_normalize(data["response"][0]["league"]["standings"][0]) # sometimes this last 0 needs to be 2
    df.to_csv(f"standings{season}.csv", sep=",")

def getHeadToHeadStats(fixture_file, teams):
    head_to_heads = pd.DataFrame(index=teams, columns=teams)
    head_to_heads = head_to_heads.fillna("")
    head_to_heads.index.name = "away team"
    head_to_heads.columns.name = "home_team"

    fixtures = pd.read_csv(fixture_file)
    fixtures = fixtures[(fixtures["fixture.status.long"] == "Match Finished")]
    home_team = fixtures.columns.get_loc("teams.home.name")
    away_team = fixtures.columns.get_loc("teams.away.name")
    home_goals = fixtures.columns.get_loc("goals.home")
    away_goals = fixtures.columns.get_loc("goals.away")
    for fixture in fixtures.itertuples(index=False):
        if fixture[home_team] not in head_to_heads.columns or fixture[away_team] not in head_to_heads.columns:
            continue
        if fixture[home_goals] > fixture[away_goals]:
            head_to_heads[fixture[home_team]][fixture[away_team]] += "W"
        elif fixture[home_goals] < fixture[away_goals]:
            head_to_heads[fixture[home_team]][fixture[away_team]] += "L"
        else:
            head_to_heads[fixture[home_team]][fixture[away_team]] += "D"
    return head_to_heads

def getUpcomingFixtures(fixture_file):
    fixtures = pd.read_csv(fixture_file)
    return fixtures[(fixtures["fixture.status.long"] == "Not Started")]


#getAllFixturesCSV(244, 2019)
#getAllFixturesCSV(244, 2020)
#getAllFixturesCSV(244, 2021)

#stats = pd.read_csv("stats.csv")
#teams = stats["team.name"]

#hth_stats_2019 = getHeadToHeadStats("fixtures2019.csv", teams)
#hth_stats_2020 = getHeadToHeadStats("fixtures2020.csv", teams)
#hth_stats_2021 = getHeadToHeadStats("fixtures2021.csv", teams)

#hth_stats = hth_stats_2019 + hth_stats_2020 + hth_stats_2021

#upcoming = getUpcomingFixtures("fixtures2021.csv")