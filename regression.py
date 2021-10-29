# This file is unused at the moment, the current functionality will be moved to parse_features!
# When feature parsing is complete, this file will contain the script for the actual regression.
# Regression is TODO!

import pandas as pd
import soccer_data as sd

# Read data
fixtures = pd.read_csv("fixtures_with_weather.csv")

# Form head-to-head dataframe
head_to_head = sd.getHeadToHeadStats("fixtures_with_weather.csv", fixtures['teams.home.name'].unique())

# Select only relevant columns
fixtures = fixtures[['league.season',\
                     'teams.home.name',\
                     'teams.home.winner',\
                     'teams.away.name',\
                     'teams.away.winner',\
                     'goals.home',\
                     'goals.away',\
                     'fh.rain.amount',\
                     'sh.rain.amount',\
                     'fh.rain.intensity',\
                     'sh.rain.intensity',\
                     'fh.humidity',\
                     'sh.humidity',\
                     'fh.clouds',\
                     'sh.clouds',\
                     'fh.air.temp',\
                     'sh.air.temp',\
                     'fh.wind.speed',\
                     'sh.wind.speed',\
                     'venue.dist']]

# Process weather data to match averages, combining first and second half data
fixtures['rain.amount'] = fixtures[['fh.rain.amount', 'sh.rain.amount']].mean(axis=1)
fixtures['rain.intensity'] = fixtures[['fh.rain.intensity', 'sh.rain.intensity']].mean(axis=1)
fixtures['humidity'] = fixtures[['fh.humidity', 'sh.humidity']].mean(axis=1)
fixtures['clouds'] = fixtures[['fh.clouds', 'sh.clouds']].mean(axis=1)
fixtures['air.temp'] = fixtures[['fh.air.temp', 'sh.air.temp']].mean(axis=1)
fixtures['wind.speed'] = fixtures[['fh.wind.speed', 'sh.wind.speed']].mean(axis=1)

# Drop first and second half weather data
fixtures.drop(['fh.rain.amount',\
               'sh.rain.amount',\
               'fh.rain.intensity',\
               'sh.rain.intensity',\
               'fh.humidity',\
               'sh.humidity',\
               'fh.clouds',\
               'sh.clouds',\
               'fh.air.temp',\
               'sh.air.temp',\
               'fh.wind.speed',\
               'sh.wind.speed'],\
               axis=1, inplace=True)

# Input draws
fixtures['teams.home.winner'] = fixtures['teams.home.winner'].fillna('Draw')
fixtures['teams.away.winner'] = fixtures['teams.away.winner'].fillna('Draw')

# Parse data so that every match has a row for both the home team and the opponent
home = fixtures.copy()
away = fixtures.copy()
home['team'] = home['teams.home.name']
away['team'] = away['teams.away.name']
home['opponent'] = home['teams.away.name']
away['opponent'] = away['teams.home.name']
home['home'] = 1
away['home'] = 0
home['result'] = home['teams.home.winner']
away['result'] = away['teams.away.winner']
home.drop(['teams.home.name', 'teams.away.name', 'teams.home.winner', 'teams.away.winner'], axis=1, inplace=True)
away.drop(['teams.home.name', 'teams.away.name', 'teams.home.winner', 'teams.away.winner'], axis=1, inplace=True)
fixtures = pd.concat([home, away])

#print(fixtures.head(10))

head_to_head.to_csv('hth.csv', sep=',')