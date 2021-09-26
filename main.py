import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
API_KEY = config["API_KEY"]

endpoint = 'leagues'

url = f"https://v3.football.api-sports.io/{endpoint}"

payload = {}
headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
