import requests
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
API_KEY = config["API_KEY"]

def getLeagueID(league_name):
    url = f"https://v3.football.api-sports.io/leagues?name={league_name}"
    payload = {}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    if data["results"] != 1:
        print("No league or multiple leagues found")
    return data["response"][0]["league"]["id"]


id = getLeagueID("Veikkausliiga")
print(id)