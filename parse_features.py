import datetime
from fmiopendata.wfs import download_stored_query
import numpy as np
import pandas as pd

START_YEAR = 2012
END_YEAR = 2021
RESULTS_2011 = {'HJK helsinki': 1, 'Inter Turku': 2, 'Turku PS': 3, 'KuPS': 4,\
                'IFK Mariehamn': 5, 'Rops': 6, 'JJK': 7, 'Honka': 8,\
                'MyPa':9, 'haka': 10, 'vaasa PS': 11, 'FF Jaro': 12}

def add_streaks(fixtures):
    fixt = fixtures.copy()
    cur_streaks = {}
    home_streaks = []
    away_streaks = []
    for team in fixtures["teams.home.name"].unique():
        cur_streaks[team] = 0
    
    for i, row in fixt.iterrows():
        home = row["teams.home.name"]
        away = row["teams.away.name"]
        home_streaks.append(cur_streaks[home])
        away_streaks.append(cur_streaks[away])
        if row['teams.home.winner'] == "Draw":
            cur_streaks[home] = 0
            cur_streaks[away] = 0
        elif row['teams.home.winner'] == True:
            cur_streaks[home] = max(1, cur_streaks[home] + 1)
            cur_streaks[away] = min(-1, cur_streaks[away] - 1)
        else:
            cur_streaks[home] = min(-1, cur_streaks[home] - 1)
            cur_streaks[away] = max(1, cur_streaks[away] + 1)
    
    fixt['home.streak'] = home_streaks
    fixt['away.streak'] = away_streaks
    return fixt        

def process_single_fixtures(path):
    i = START_YEAR
    fixt = []
    while i <= END_YEAR:
        f = pd.read_csv(path + "/fixtures" + str(i) + ".csv")
        f = f.sort_values(by=['fixture.timestamp', 'fixture.venue.name'])
        f = f.dropna(subset=["fixture.date", "fixture.venue.name",\
                             "teams.home.name", "teams.away.name",\
                             "fixture.status.long"])
        f = f[f["fixture.status.long"] == "Match Finished"]
        f['teams.home.winner'] = f['teams.home.winner'].fillna('Draw')
        f['teams.away.winner'] = f['teams.away.winner'].fillna('Draw')
        f = f.sort_values(by=['fixture.timestamp', 'fixture.id'])
        f = add_streaks(f)
        fixt.append(f)
        i += 1

    fixtures = pd.concat(fixt)
    return fixtures

def calculate_win_percentage(fixtures):
    fixt = fixtures.copy()
    total_wins = {}
    total_matches = {}
    h2h_wins = {}
    h2h_matches = {}
    team_total_win = []
    opponent_total_win = []
    team_h2h_win = []
    opponent_h2h_win = []
    for team in fixtures['teams.home.name'].unique():
        total_wins[team] = 0
        total_matches[team] = 0
        h2h_wins[team] = {}
        h2h_matches[team] = {}
        for opponent in fixtures['teams.away.name'].unique():
            if team == opponent:
                continue
            h2h_wins[team][opponent] = 0
            h2h_matches[team][opponent] = 0
    
    for i, row in fixt.iterrows():
        team = row["teams.home.name"]
        opponent = row["teams.away.name"]
        if total_matches[team] == 0:
            team_total_win.append(0.5)
        else:
            team_total_win.append(total_wins[team] / total_matches[team])
        if total_matches[opponent] == 0:
            opponent_total_win.append(0.5)
        else:
            opponent_total_win.append(total_wins[opponent] / total_matches[opponent])
        if h2h_matches[team][opponent] == 0:
            team_h2h_win.append(0.5)
            opponent_h2h_win.append(0.5)
        else:
            team_h2h_win.append(h2h_wins[team][opponent] / h2h_matches[team][opponent])
            opponent_h2h_win.append(h2h_wins[opponent][team] / h2h_matches[opponent][team])
        # ---- 
        total_matches[team] += 1
        total_matches[opponent] += 1
        h2h_matches[team][opponent] += 1
        h2h_matches[opponent][team] += 1
        if row['teams.home.winner'] == "Draw":
            continue
        elif row['teams.home.winner'] == True:
            total_wins[team] += 1
            h2h_wins[team][opponent] += 1
        else:
            total_wins[opponent] += 1
            h2h_wins[opponent][team] += 1
    
    fixt['home.win.percent'] = team_total_win
    fixt['away.win.percent'] = opponent_total_win
    fixt['home.h2h.win.percent'] = team_h2h_win
    fixt['away.h2h.win.percent'] = opponent_h2h_win
    return fixt

def get_nearest_weather_station(venue_name, timestamp):
    if venue_name == "Tapiolan Urheilupuisto" or\
       venue_name == "Tapiolan Urheilupuisto (Espoo (Esbo))":
        if timestamp > 1388527200: # year > 2013
            return ("Espoo Tapiola", "874863", 1)
        else:
            return ("Espoo Sepänkylä", "101005", 4)
    elif venue_name == "Tehtaan kenttä":
        return ("Hattula Lepaa", "101151", 22)
    elif venue_name == "Bolt Arena" or\
         venue_name == "Sonera Stadium" or\
         venue_name == "Sonera Stadium (Helsinki)" or\
         venue_name == "Telia 5G -areena" or\
         venue_name == "Telia 5G -areena (Helsinki)" or\
         venue_name == "Telia 5G-Areena (Helsinki)":
        return ("Helsinki Kaisaniemi", "100971", 2)
    elif venue_name == "Arto Tolsa Areena":
        return ("Kotka Rankki", "101030", 9)
    elif venue_name == "Savon Sanomat Areena" or\
         venue_name == "Savon Sanomat Areena (Kuopio)" or\
         venue_name == "Väre Areena":
        return ("Kuopio Savilahti", "101586", 2)
    elif venue_name == "Väinölänniemen stadion (Kuopio)":
        return ("Kuopio Savilahti", "101586", 3)
    elif venue_name == "Lahden Stadion" or\
         venue_name == "Lahden Stadion (Lahti)":
        if timestamp > 1546293600: # year > 2018
            return ("Lahti Sopenkorpi", "104796", 1)
        else:
            return ("Lahti Laune", "101152", 3)
    elif venue_name == "Lahti Kisapuisto" or\
         venue_name == "Lahden Kisapuisto (Lahti)" or\
         venue_name == "Kisapuisto (Lahti)" or\
         venue_name == "Kisapuisto":
        if timestamp > 1546293600: # year > 2018
            return ("Lahti Sopenkorpi", "104796", 2)
        else:
            return ("Lahti Laune", "101152", 3)
    elif venue_name == "Wiklöf Holding Arena" or\
         venue_name == "Wiklof Holding Arena" or\
         venue_name == "Wiklöf Holding Arena (Maarianhamina (Mariehamn), Ahvenanmaa (Åland))" or\
         venue_name == "Wiklöf Holding Arena konstgräs (Maarianhamina (Mariehamn), Ahvenanmaa (Åland))":
        return ("Jomala Maarianhamina lentoasema", "100907", 3)
    elif venue_name == "Raatin stadion" or\
         venue_name == "Raatin stadion (Oulu)" or\
         venue_name == "Raatti Tekonurmi":
        return ("Oulu Oulunsalo Pellonpää", "101799", 10)
    elif venue_name == "OmaSP Stadion" or\
         venue_name == "OmaSP Stadion (Seinäjoki)" or\
         venue_name == "Seinäjoen keskuskenttä" or\
         venue_name == "Seinäjoen keskuskenttä (Seinäjoki)" or\
         venue_name == "Jouppilanvuoren tekonurmi (Seinäjoki)":
        return ("Seinäjoki Pelmaa", "101486", 24)
    elif venue_name == "Ratinan Stadion" or\
         venue_name == "Ratinan Stadion (Tampere (Tammerfors))" or\
         venue_name == "Tampere Stadium" or\
         venue_name == "Tammela Stadium" or\
         venue_name == "Tammela Stadion" or\
         venue_name == "Tammelan Stadion" or\
         venue_name == "Tammelan Stadion (Tampere)":
        return ("Tampere Härmälä", "101124", 4)
    elif venue_name == "Veritas Stadium" or\
         venue_name == "Veritas Stadion" or\
         venue_name == "Veritas Stadion (Turku (Åbo))":
        return ("Turku Artukainen", "100949", 6)
    elif venue_name == "Paavo Nurmi Stadion" or\
         venue_name == "Urheilupuiston Yläkenttä":
        return ("Turku Artukainen", "100949", 4)
    elif venue_name == "Rovaniemen keskuskenttä" or\
         venue_name == "Rovaniemen Keskuskenttä" or\
         venue_name == "Rovaniemen Keskuskenttä (Rovaniemi)":
        return ("Rovaniemi rautatieasema", "101928", 1)
    elif venue_name == "Elisa Stadion" or\
         venue_name == "Elisa Stadion (Vaasa)" or\
         venue_name == "Hietalahden jalkapallostadion" or\
         venue_name == "Kaarlen kenttä" or\
         venue_name == "Kaarlen kenttä (Vaasa)":
        return ("Vaasa Klemettilä", "101485", 1)
    elif venue_name == "Kokkolan keskuskenttä" or\
         venue_name == "Kokkolan Keskuskenttä" or\
         venue_name == "Kokkolan Keskuskenttä (Kokkola)":
        return ("Kruunupyy Kokkola-Pietarsaari lentoasema", "101662", 13)
    elif venue_name == "Jakobstads Centralplan" or\
         venue_name == "Länsikenttä tekonurmi":
        return ("Kruunupyy Kokkola-Pietarsaari lentoasema", "101662", 22)
    elif venue_name == "Saviniemen jalkapallostadion" or\
         venue_name == "Kymenlaakson Sähkö Stadion":
        return ("Kouvola Utti lentoasema", "101191", 15)
    elif venue_name == "Harjun stadion" or\
         venue_name == "Harjun Stadion" or\
         venue_name == "Harjun stadion (Jyväskylä)":
        return ("Jyväskylä lentoasema", "101339", 17)
    elif venue_name == "Vaajakosken urheilukenttä (Vaajakoski)":
        return ("Jyväskylä lentoasema", "101339", 19)
    elif venue_name == "Kaurialan kenttä":
        return ("Hämeenlinna Katinen", "101150", 3)
    elif venue_name == "Myyrmäen jalkapallostadion" or\
         venue_name == "Myyrmäen jalkapallostadion (Vantaa)":
        return ("Vantaa Helsinki-Vantaan lentoasema", "100968", 7)
    elif venue_name == "Sauvosaaren urheilupuisto" or\
         venue_name == "Sauvosaaren urheilupuisto (Kemi)" or\
         venue_name == "Sauvosaaren Takakenttä N (Kemi)":
        if timestamp < 1525899600 or timestamp > 1526331600: # handling a strange specific case
            return ("Kemi Kemi-Tornio lentoasema", "101840", 5) # of missing data from the FMI API
        else:
            return ("Kemi Ajos", "101846", 7)
    elif venue_name == "City Sport Areena (Kemi)":
        return ("Kemi Kemi-Tornio lentoasema", "101840", 4)
    else:
        raise Exception("Venue name unknown: " + venue_name + "!")

def add_weather(fixtures):
    fixt = fixtures.copy()
    air_temp = []
    cloud_amount = []
    dewpoint = []
    rain_amount = []
    rain_intensity = []
    humidity = []
    wind_speed = []
    station_dist = []
    for i, row in fixt.iterrows():
        start_time = datetime.datetime.fromisoformat(row['fixture.date'])
        end_time = start_time + datetime.timedelta(minutes=90)
        start_time = start_time.isoformat().replace("+00:00", "Z")
        end_time = end_time.isoformat().replace("+00:00", "Z")
        station = get_nearest_weather_station(row['fixture.venue.name'], row['fixture.timestamp'])
        obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["fmisid=" + station[1],
                                  "starttime=" + start_time,
                                  "endtime=" + end_time])
        weather_features = ['Air temperature',
                            'Cloud amount',
                            'Dew-point temperature',
                            'Precipitation amount',
                            'Precipitation intensity',
                            'Relative humidity',
                            'Wind speed']
        avg_obs = dict.fromkeys(weather_features)
        for feature in weather_features:
            t = list(obs.data.values())[0]
            if np.isnan(t[station[0]][feature]['value']) and\
            (feature != 'Precipitation intensity' or\
            np.isnan(t[station[0]]['Precipitation amount']['value'])):
                avg_obs[feature] = np.nan
            else:
                vals = obs.data.values()
                points = []
                for o in vals:
                    if feature == 'Precipitation amount':
                        points.append(max(0, o[station[0]][feature]['value']))
                    elif feature == 'Precipitation intensity' and np.isnan(o[station[0]][feature]['value']):
                        points.append(0)
                    else:
                        points.append(o[station[0]][feature]['value'])
                if feature == 'Precipitation amount':
                    avg_obs[feature] = sum(points)
                else:
                    avg_obs[feature] = (sum(points) / len(points))
        air_temp.append(avg_obs['Air temperature'])
        cloud_amount.append(avg_obs['Cloud amount'])
        dewpoint.append(avg_obs['Dew-point temperature'])
        rain_amount.append(avg_obs['Precipitation amount'])
        rain_intensity.append(avg_obs['Precipitation intensity'])
        humidity.append(avg_obs['Relative humidity'])
        wind_speed.append(avg_obs['Wind speed'])
        station_dist.append(station[2])
    fixt['air.temp'] = air_temp
    fixt['cloud.amount'] = cloud_amount
    fixt['dewpoint.temp'] = dewpoint
    fixt['rain.amount'] = rain_amount
    fixt['rain.intensity'] = rain_intensity
    fixt['humidity'] = humidity
    fixt['wind.speed'] = wind_speed
    fixt['station.distance'] = station_dist
    return fixt

def separate_home_away(fixtures):
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
    home['streak'] = home['home.streak']
    away['streak'] = away['away.streak']
    home['opp.streak'] = home['away.streak']
    away['opp.streak'] = away['home.streak']
    home['win.percent'] = home['home.win.percent']
    away['win.percent'] = away['away.win.percent']
    home['opp.win.percent'] = home['away.win.percent']
    away['opp.win.percent'] = away['home.win.percent']
    home['h2h.win.percent'] = home['home.h2h.win.percent']
    away['h2h.win.percent'] = away['away.h2h.win.percent']
    home['opp.h2h.win.percent'] = home['away.h2h.win.percent']
    away['opp.h2h.win.percent'] = away['home.h2h.win.percent']
    ret = pd.concat([home, away])
    return ret.sort_values(by=['fixture.timestamp', 'fixture.id'])

def add_last_season_placement(fixtures):
    standings = {}
    standings[2011] = RESULTS_2011
    for y in range(START_YEAR, (END_YEAR + 1)):
        results = {}
        data = pd.read_csv("data/standings/standings" + str(y) + ".csv")
        for i, row in data.iterrows():
            results[row["team.name"]] = row["rank"]
        standings[y] = results
    
    fixt = fixtures.copy()
    team_placements = []
    opponent_placements = []
    for i, row in fixt.iterrows():
        lastyear = row["league.season"] - 1
        if row["team"] in standings[lastyear].keys():
            team_placements.append(standings[lastyear][row["team"]])
        else:
            team_placements.append(13)
        if row["opponent"] in standings[lastyear].keys():
            opponent_placements.append(standings[lastyear][row["opponent"]])
        else:
            opponent_placements.append(13)
    fixt["team.last.placement"] = team_placements
    fixt["opponent.last.placement"] = opponent_placements
    return fixt

""" fixtures = process_single_fixtures("data/fixtures")
fixtures = calculate_win_percentage(fixtures)
fixtures = add_weather(fixtures)
fixtures = separate_home_away(fixtures)
fixtures = add_last_season_placement(fixtures)
fixtures.to_csv("fixtures_features.csv", sep=",") """