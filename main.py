import requests
from dotenv import dotenv_values
import json
import pandas as pd

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

# Does this endpoint exist? The rapidapi version says it doesn't
""" def getStatus():
    url = make_url("/status")
    querystring = {}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data """

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
def saveTeamStatsCSV(data, name):
    df = pd.json_normalize(data["response"])
    df.to_csv(name + ".csv", sep=",")

saveTeamStatsCSV(getTeamStats(244, 2021, 587), "mariehamn")

df = pd.read_csv("mariehamn.csv")
#print(df.keys().to_numpy())

print(df['penalty.scored.total'][0])
print(df['biggest.loses.away'][0])
print(df['goals.for.minute.61-75.percentage'][0])
print(df['failed_to_score.away'][0])