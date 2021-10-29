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


fixtures = process_single_fixtures("data/fixtures")
fixtures = calculate_win_percentage(fixtures)
fixtures = separate_home_away(fixtures)


fixtures.to_csv("fixtures_features.csv", sep=",")
#print(fixtures.info())