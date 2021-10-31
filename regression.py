import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

CURRENT_PARAMS = {
    'HJK helsinki': {'streak': 2, 'win.percent': 0.5895765472312704, 'rank': 1, 'h2h': {
        'haka': 0.8571428571428571,
        'KuPS': 0.42857142857142855,
        'IFK Mariehamn': 0.7931034482758621,
        'Honka': 0.42105263157894735,
        'Inter Turku': 0.41379310344827586,
        'Kooteepee': 0.8,
        'FC Lahti': 0.5357142857142857,
        'SJK': 0.6818181818181818,
        'HIFK Elsinki': 0.4,
        'Ilves Tampere': 0.6,
        'AC oulu': 0.5
    }}, 
    'Inter Turku': {'streak': -2, 'win.percent': 0.3737704918032787, 'rank': 2, 'h2h': {
        'haka': 0.8571428571428571,
        'IFK Mariehamn': 0.39285714285714285,
        'Honka': 0.15789473684210525,
        'HJK helsinki': 0.27586206896551724,
        'KuPS': 0.3103448275862069,
        'FC Lahti': 0.2962962962962963,
        'SJK': 0.2857142857142857,
        'Kooteepee': 0.8,
        'HIFK Elsinki': 0.625,
        'Ilves Tampere': 0.3684210526315789,
        'AC oulu': 0.5
    }}, 
    'KuPS': {'streak': 0, 'win.percent': 0.43278688524590164, 'rank': 3, 'h2h': {
        'haka': 0.5714285714285714,
        'IFK Mariehamn': 0.6071428571428571,
        'Honka': 0.3157894736842105,
        'Inter Turku': 0.4482758620689655,
        'HJK helsinki': 0.17857142857142858,
        'FC Lahti': 0.37037037037037035,
        'SJK': 0.3333333333333333,
        'Kooteepee': 0.6,
        'HIFK Elsinki': 0.625,
        'Ilves Tampere': 0.35,
        'AC oulu': 1.0
    }}, 
    'Honka': {'streak': 0, 'win.percent': 0.3961352657004831, 'rank': 4, 'h2h': {
        'HJK helsinki': 0.21052631578947367, 
        'Inter Turku': 0.5263157894736842, 
        'KuPS': 0.42105263157894735,  
        'FC Lahti': 0.4444444444444444, 
        'SJK': 0.3333333333333333, 
        'HIFK Elsinki': 0.16666666666666666, 
        'AC oulu': 1.0, 
        'Kooteepee': 0.6666666666666666,
        'IFK Mariehamn': 0.3333333333333333, 
        'Ilves Tampere': 0.5, 
        'haka': 0.125
    }}, 
    'FC Lahti': {'streak': 0, 'win.percent': 0.3758169934640523, 'rank': 6, 'h2h': {
        'HJK helsinki': 0.21428571428571427,
        'haka': 0.25,
        'IFK Mariehamn': 0.4444444444444444,
        'Honka': 0.2777777777777778,
        'Inter Turku': 0.37037037037037035,
        'Kooteepee': 0.6666666666666666,
        'SJK': 0.36363636363636365,
        'HIFK Elsinki': 0.5,
        'Ilves Tampere': 0.4444444444444444,
        'AC oulu': 0.0,
        'KuPS': 0.3333333333333333
    }}, 
    'SJK': {'streak': 0, 'win.percent': 0.4225941422594142, 'rank': 7, 'h2h': {
        'haka': 0.5,
        'IFK Mariehamn': 0.38095238095238093,
        'Honka': 0.3333333333333333,
        'Inter Turku': 0.47619047619047616,
        'HJK helsinki': 0.13636363636363635,
        'KuPS': 0.3333333333333333,
        'FC Lahti': 0.18181818181818182,
        'Kooteepee': 0.6,
        'HIFK Elsinki': 0.35294117647058826,
        'Ilves Tampere': 0.3157894736842105,
        'AC oulu': 1.0
    }}, 
    'HIFK Elsinki': {'streak': 0, 'win.percent': 0.29310344827586204, 'rank': 8, 'h2h': {
        'haka': 0.5,
        'IFK Mariehamn': 0.1875,
        'Honka': 0.6666666666666666,
        'Inter Turku': 0.1875,
        'HJK helsinki': 0.2,
        'KuPS': 0.0625,
        'FC Lahti': 0.0625,
        'SJK': 0.35294117647058826,
        'Kooteepee': 0.4,
        'Ilves Tampere': 0.06666666666666667,
        'AC oulu': 1.0
    }}, 
    'AC oulu': {'streak': 0, 'win.percent': 0.2, 'rank': 13, 'h2h': {
        'haka': 0.3333333333333333,
        'IFK Mariehamn': 0.3333333333333333,
        'Honka': 0.0,
        'Inter Turku': 0.5,
        'HJK helsinki': 0.5,
        'KuPS': 0.0,
        'FC Lahti': 0.0,
        'SJK': 0.0,
        'Kooteepee': 0.5,
        'HIFK Elsinki': 0.0,
        'Ilves Tampere': 0.0
    }}, 
    'Kooteepee': {'streak': 0, 'win.percent': 0.15, 'rank': 13, 'h2h': {
        'haka': 0.5,
        'IFK Mariehamn': 0.16666666666666666,
        'Honka': 0.3333333333333333,
        'Inter Turku': 0.2,
        'HJK helsinki': 0.0,
        'KuPS': 0.2,
        'FC Lahti': 0.0,
        'SJK': 0.0,
        'HIFK Elsinki': 0.2,
        'Ilves Tampere': 0.0,
        'AC oulu': 0.0
    }}, 
    'IFK Mariehamn': {'streak': 0, 'win.percent': 0.37662337662337664, 'rank': 9, 'h2h': {
        'haka': 0.5714285714285714,
        'Honka': 0.19047619047619047,
        'KuPS': 0.25,
        'Inter Turku': 0.32142857142857145,
        'HJK helsinki': 0.06896551724137931,
        'FC Lahti': 0.25925925925925924,
        'Kooteepee': 0.8333333333333334,
        'SJK': 0.38095238095238093,
        'HIFK Elsinki': 0.3125,
        'Ilves Tampere': 0.42105263157894735,
        'AC oulu': 0.6666666666666666
    }}, 
    'Ilves Tampere': {'streak': -1, 'win.percent': 0.42718446601941745, 'rank': 5, 'h2h': {
        'haka': 0.75,
        'IFK Mariehamn': 0.3684210526315789,
        'JJK': 0.3333333333333333,
        'Honka': 0.2,
        'Inter Turku': 0.42105263157894735,
        'HJK helsinki': 0.15,
        'KuPS': 0.55,
        'FC Lahti': 0.3333333333333333,
        'SJK': 0.47368421052631576,
        'Kooteepee': 0.6,
        'HIFK Elsinki': 0.5333333333333333,
        'AC oulu': 1.0
    }}, 
    'haka': {'streak': 0, 'win.percent': 0.275, 'rank': 10, 'h2h': {
        'IFK Mariehamn': 0.14285714285714285,
        'Honka': 0.5,
        'Inter Turku': 0.14285714285714285,
        'HJK helsinki': 0.0,
        'KuPS': 0.2857142857142857,
        'FC Lahti': 0.25,
        'SJK': 0.25,
        'Kooteepee': 0.0,
        'HIFK Elsinki': 0.5,
        'Ilves Tampere': 0.0,
        'AC oulu': 0.3333333333333333
    }}
}

def model_1(fixt):
    fixtures = fixt.copy()
    # Select only relevant columns
    fixtures = fixtures[['team',\
                         'opponent',\
                         'home',\
                         'win.percent',\
                         'opp.win.percent',\
                         'h2h.win.percent',\
                         'opp.h2h.win.percent',\
                         'team.last.placement',\
                         'opponent.last.placement',\
                         'streak',\
                         'opp.streak',\
                         'air.temp',\
                         'rain.amount',\
                         'humidity',\
                         'cloud.amount',\
                         'wind.speed',\
                         'station.distance',\
                         'result']]
    
    labels_a = [0, 1, 2]
    cloud_bins = [-1.0, 2.0, 5.0, 10]
    fixtures['cloud.amount'] = fixtures['cloud.amount'].fillna(fixtures['cloud.amount'].mean())
    fixtures['cloudy'] = pd.cut(fixtures['cloud.amount'], bins=cloud_bins, labels=labels_a)
    wind_bins = [-1.0, 3.0, 6.0, 15.0]
    fixtures['wind.speed'] = fixtures['wind.speed'].fillna(fixtures['wind.speed'].mean())
    fixtures['windy'] = pd.cut(fixtures['wind.speed'], bins=wind_bins, labels=labels_a)
    humid_bins = [0.0, 40.0, 80.0, 100.0]
    fixtures['humidity'] = fixtures['humidity'].fillna(fixtures['humidity'].mean())
    fixtures['humid'] = pd.cut(fixtures['humidity'], bins=humid_bins, labels=labels_a)
    #rain_bins = [-1.0, 0.15, 0.6, 10]
    #fixtures['rainy'] = pd.cut(fixtures['rain.amount'], bins=rain_bins, labels=labels_a)
    fixtures['air.temp'] = fixtures['air.temp'].fillna(fixtures['air.temp'].mean())

    station_bins = [0, 3.5, 8.5, 30]
    fixtures['distance'] = pd.cut(fixtures['station.distance'], bins=station_bins, labels=labels_a)

    labels_b = [-1, 0, 1]
    streak_bins = [-20, -2.5, 2.5, 20]
    fixtures['streak'] = pd.cut(fixtures['streak'], bins=streak_bins, labels=labels_b)
    fixtures['opp.streak'] = pd.cut(fixtures['opp.streak'], bins=streak_bins, labels=labels_b)

    fixtures['result'] = fixtures['result'].astype('category')
    fixtures['result'] = fixtures['result'].cat.reorder_categories(['False', 'Draw', 'True'], ordered=True)
    catmap_results = dict(zip(fixtures['result'].cat.codes, fixtures['result']))
    fixtures['result'] = fixtures['result'].cat.codes
    print(catmap_results)

    fixtures['team'] = fixtures['team'].astype('category')
    catmap_team = dict(zip(fixtures['team'].cat.codes, fixtures['team']))
    fixtures['team'] = fixtures['team'].cat.codes
    print(catmap_team)

    fixtures['opponent'] = fixtures['opponent'].astype('category')
    catmap_opp = dict(zip(fixtures['opponent'].cat.codes, fixtures['opponent']))
    fixtures['opponent'] = fixtures['opponent'].cat.codes
    print(catmap_opp)

    fixtures = fixtures.sample(frac=1)
    fixtures.to_csv("fixtures_features_test.csv", sep=",")
    X = fixtures.drop(['cloud.amount', 'wind.speed', 'humidity', 'rain.amount', 'station.distance', 'result'], axis=1)
    Y = fixtures['result']

    X_train = X[:3300]
    Y_train = Y[:3300]
    X_test = X[3300:]
    Y_test = Y[3300:]

    model = LinearRegression()
    lin = model.fit(X_train, Y_train)
    score = lin.score(X_test, Y_test)
    print(score)
    print(cross_val_score(model, X, Y))

    model = {'model': model,\
             'catmap_results': catmap_results,\
             'catmap_team': {val: key for key, val in catmap_team.items()},\
             'catmap_opp': {val: key for key, val in catmap_opp.items()}}

    pickle.dump(model, open('model_1.pkl', 'wb'))

def predict(team, opponent, home, cloudy, windy, humid, air_temp):
    data = pickle.load(open('model_1.pkl', 'rb'))
    model = data['model']
    catmap_results = data['catmap_results']
    catmap_team = data['catmap_team']
    catmap_opp = data['catmap_opp']

    x = [[catmap_team[team],\
         catmap_opp[opponent],\
         home,\
         CURRENT_PARAMS[team]['win.percent'],\
         CURRENT_PARAMS[opponent]['win.percent'],\
         CURRENT_PARAMS[team]['h2h'][opponent],\
         CURRENT_PARAMS[opponent]['h2h'][team],\
         CURRENT_PARAMS[team]['rank'],\
         CURRENT_PARAMS[opponent]['rank'],\
         CURRENT_PARAMS[team]['streak'],\
         CURRENT_PARAMS[opponent]['streak'],\
         air_temp,\
         cloudy,\
         windy,\
         humid,\
         0]]

    pred = model.predict(x)[0]
    print(pred)
    pred = int(round(pred))
    pred = catmap_results[pred]

    if pred == 'False':
        return 'Away win'
    if pred == 'True':
        return 'Home win'
    return 'Draw'


fixtures = pd.read_csv("fixtures_features.csv")
model_1(fixtures)

#print(predict("HJK helsinki", "AC oulu", 1, 0, 1, 1, 15))