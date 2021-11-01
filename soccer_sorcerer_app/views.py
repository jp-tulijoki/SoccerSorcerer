from logging import error
from django.shortcuts import render, redirect
import pandas as pd
from soccer_data import getHeadToHeadStats
from probability_counter import countOverallProbabilities, countHomeAwayProbabilities, countHeadToHeadProbability
from regression import predict as regression_predict

stats = pd.read_csv("stats.csv")
teams = stats["team.name"]
hth_stats_2019 = getHeadToHeadStats("fixtures2019.csv", teams)
hth_stats_2020 = getHeadToHeadStats("fixtures2020.csv", teams)
hth_stats_2021 = getHeadToHeadStats("fixtures2021.csv", teams)
hth_stats = hth_stats_2019 + hth_stats_2020 + hth_stats_2021

convert = {"AC Oulu": "AC oulu", "Haka": "haka", "HIFK": "HIFK Elsinki", "HJK": "HJK helsinki", "KTP": "Kooteepee"}
cloudiness_to_int = {"Clear sky": 0, "Half-cloudy": 1, "Cloudy": 2}
wind_to_int = {"Calm": 0, "Windy": 1, "Stormy": 2}
humidity_to_int = {"Dry": 0, "Average": 1, "Humid": 2} 

def home(request):
    home_team = request.session.get("home_team", None)
    away_team = request.session.get("away_team", None)
    home_win = request.session.get("home_win", None)
    draw = request.session.get("draw", None)
    away_win = request.session.get("away_win", None)
    regression_prediction = request.session.get("regression_prediction", None)
    error = request.session.get("error", None)
    return render(request, 'index.html', {"home_team": home_team, "away_team": away_team, "home_win": home_win, "draw": draw,
                  "away_win": away_win, "regression_prediction": regression_prediction, "error": error})

def predict(request):
    home_team = request.POST.get("homeTeam")
    away_team = request.POST.get("awayTeam")
    cloudiness = cloudiness_to_int[request.POST.get("cloudiness")]
    wind = wind_to_int[request.POST.get("wind")]
    humidity = humidity_to_int[request.POST.get("humidity")]
    temperature = int(request.POST.get("temperature"))
    print(temperature)
    request.session["home_team"] = home_team
    request.session["away_team"] = away_team
    if home_team == away_team:
        request.session["error"] = "Home and away teams can't be the same."
        request.session["home_win"] = None
        return redirect("/")
    if home_team in convert:
        home_team = convert[home_team]
    if away_team in convert:
        away_team = convert[away_team]
    overall = countOverallProbabilities(stats, home_team, away_team)
    home_away = countHomeAwayProbabilities(stats, home_team, away_team)
    head_to_head = countHeadToHeadProbability(hth_stats, home_team, away_team)
    regression_prediction = regression_predict(home_team, away_team, 1, cloudiness, wind, humidity, temperature)
    request.session["home_win"] = f"{((overall[0] + home_away[0] + head_to_head[0]) / 3):.2f}"
    request.session["draw"] = f"{((overall[1] + home_away[1] + head_to_head[1]) / 3):.2f}"
    request.session["away_win"] = f"{((overall[2] + home_away[2] + head_to_head[2]) / 3):.2f}"
    request.session["regression_prediction"] = regression_prediction
    request.session["error"] = None
    return redirect("/")