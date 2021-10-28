from numpy.core.numeric import NaN
import pandas as pd
from datetime import datetime, timedelta

espoo_weather = pd.read_csv("data/espoo_tapiola_1km.csv")
hattula_weather = pd.read_csv("data/hattula_lepaa_eituulta_eipilvia_22km.csv")
helsinki_weather = pd.read_csv("data/helsinki_kaisaniemi_2km.csv")
kokkola_weather = pd.read_csv("data/kokkola_lentoasema_eisadetta_13km.csv")
kotka_weather = pd.read_csv("data/kotka_rankki_9km.csv")
kuopio_weather = pd.read_csv("data/kuopio_savilahti_2km.csv")
lahti_weather = pd.read_csv("data/lahti_sopenkorpi_eituulta_1km.csv")
maarianhamina_weather = pd.read_csv("data/maarianhamina_lentoasema_eisadetta_3km.csv")
oulu_weather = pd.read_csv("data/oulu_oulunsalo_10km.csv")
rovaniemi_weather = pd.read_csv("data/rovaniemi_rautatieasema_eisadetta_1km.csv")
seinajoki_weather = pd.read_csv("data/seinajoki_pelmaa_eipilvia_24km.csv")
tampere_weather = pd.read_csv("data/tampere_harmala_eituulta_4km.csv")
turku_weather = pd.read_csv("data/turku_artukainen_6km.csv")
vaasa_weather = pd.read_csv("data/vaasa_klemettila_1km.csv")

def form_return_dict(weather, date, venuedist):
    # Rounding the time down when a game begins half past (i.e. 15:30 > 15:00)
    # Could be done better using averaging or more precise data: TODO!
    fh = date.replace(microsecond=0, second=0, minute=0)
    firsthalf = weather.loc[(weather['Vuosi'] == fh.year) &\
                            (weather['Kk'] == fh.month) &\
                            (weather['Pv'] == fh.day) &\
                            (weather['Klo'] == fh.strftime("%H:%M"))]
    sh = fh + timedelta(hours=1)
    secondhalf = weather.loc[(weather['Vuosi'] == sh.year) &\
                            (weather['Kk'] == sh.month) &\
                            (weather['Pv'] == sh.day) &\
                            (weather['Klo'] == sh.strftime("%H:%M"))]
    
    ret = {}
    if ("Sademäärä (mm)" in firsthalf) and ("Sademäärä (mm)" in secondhalf):
        ret["fh.rain.amount"] = firsthalf["Sademäärä (mm)"].iloc[0]
        ret["sh.rain.amount"] = secondhalf["Sademäärä (mm)"].iloc[0]
    else:
        ret["fh.rain.amount"] = NaN
        ret["sh.rain.amount"] = NaN
    
    if ("Sateen intensiteetti (mm/h)" in firsthalf) and ("Sateen intensiteetti (mm/h)" in secondhalf):
        ret["fh.rain.intensity"] = firsthalf["Sateen intensiteetti (mm/h)"].iloc[0]
        ret["sh.rain.intensity"] = secondhalf["Sateen intensiteetti (mm/h)"].iloc[0]
    else:
        ret["fh.rain.intensity"] = NaN
        ret["sh.rain.intensity"] = NaN
        
    if ("Suhteellinen kosteus (%)" in firsthalf) and ("Suhteellinen kosteus (%)" in secondhalf):
        ret["fh.humidity"] = firsthalf["Suhteellinen kosteus (%)"].iloc[0]
        ret["sh.humidity"] = secondhalf["Suhteellinen kosteus (%)"].iloc[0]
    else:
        ret["fh.humidity"] = NaN
        ret["sh.humidity"] = NaN
    
    if ("Pilvien määrä (1/8)" in firsthalf) and ("Pilvien määrä (1/8)" in secondhalf):
        ret["fh.clouds"] = firsthalf["Pilvien määrä (1/8)"].iloc[0]
        ret["sh.clouds"] = secondhalf["Pilvien määrä (1/8)"].iloc[0]
    else:
        ret["fh.clouds"] = NaN
        ret["sh.clouds"] = NaN
    
    if ("Ilman lämpötila (degC)" in firsthalf) and ("Ilman lämpötila (degC)" in secondhalf):
        ret["fh.air.temp"] = firsthalf["Ilman lämpötila (degC)"].iloc[0]
        ret["sh.air.temp"] = secondhalf["Ilman lämpötila (degC)"].iloc[0]
    else:
        ret["fh.air.temp"] = NaN
        ret["sh.air.temp"] = NaN
    
    if ("Tuulen nopeus (m/s)" in firsthalf) and ("Tuulen nopeus (m/s)" in secondhalf):
        ret["fh.wind.speed"] = firsthalf["Tuulen nopeus (m/s)"].iloc[0]
        ret["sh.wind.speed"] = secondhalf["Tuulen nopeus (m/s)"].iloc[0]
    else:
        ret["fh.wind.speed"] = NaN
        ret["sh.wind.speed"] = NaN
    
    ret["venue.dist"] = venuedist
    return pd.Series(ret)

def get_weather_stats(match_timestamp, venue_name):
    date = datetime.fromisoformat(match_timestamp)
    
    if venue_name == "Tapiolan Urheilupuisto" or\
       venue_name == "Tapiolan Urheilupuisto (Espoo (Esbo))":
        return form_return_dict(espoo_weather, date, 1)
    elif venue_name == "Tehtaan kenttä":
        return form_return_dict(hattula_weather, date, 22)
    elif venue_name == "Bolt Arena" or\
         venue_name == "Telia 5G -areena" or\
         venue_name == "Telia 5G -areena (Helsinki)":
        return form_return_dict(helsinki_weather, date, 2)
    elif venue_name == "Arto Tolsa Areena":
        return form_return_dict(kotka_weather, date, 9)
    elif venue_name == "Savon Sanomat Areena" or\
         venue_name == "Savon Sanomat Areena (Kuopio)" or\
         venue_name == "Väre Areena":
        return form_return_dict(kuopio_weather, date, 2)
    elif venue_name == "Lahden Stadion" or\
         venue_name == "Lahden Stadion (Lahti)":
        return form_return_dict(lahti_weather, date, 1)
    elif venue_name == "Lahti Kisapuisto":
        return form_return_dict(lahti_weather, date, 2)
    elif venue_name == "Wiklöf Holding Arena" or\
         venue_name == "Wiklof Holding Arena" or\
         venue_name == "Wiklöf Holding Arena (Maarianhamina (Mariehamn), Ahvenanmaa (Åland))":
        return form_return_dict(maarianhamina_weather, date, 3)
    elif venue_name == "Raatin stadion" or\
         venue_name == "Raatti Tekonurmi":
        return form_return_dict(oulu_weather, date, 10)
    elif venue_name == "OmaSP Stadion" or\
         venue_name == "OmaSP Stadion (Seinäjoki)":
        return form_return_dict(seinajoki_weather, date, 24)
    elif venue_name == "Ratinan Stadion" or\
         venue_name == "Tampere Stadium" or\
         venue_name == "Tammela Stadium" or\
         venue_name == "Tammela Stadion" or\
         venue_name == "Tammelan Stadion" or\
         venue_name == "Tammelan Stadion (Tampere)":
        return form_return_dict(tampere_weather, date, 4)
    elif venue_name == "Veritas Stadium" or\
         venue_name == "Veritas Stadion" or\
         venue_name == "Veritas Stadion (Turku (Åbo))":
        return form_return_dict(turku_weather, date, 6)
    elif venue_name == "Rovaniemen keskuskenttä" or\
         venue_name == "Rovaniemen Keskuskenttä" or\
         venue_name == "Rovaniemen Keskuskenttä (Rovaniemi)":
        return form_return_dict(rovaniemi_weather, date, 1)
    elif venue_name == "Elisa Stadion" or\
         venue_name == "Elisa Stadion (Vaasa)":
        return form_return_dict(vaasa_weather, date, 1)
    elif venue_name == "Kokkolan keskuskenttä" or\
         venue_name == "Kokkolan Keskuskenttä (Kokkola)":
        return form_return_dict(kokkola_weather, date, 13)
    else:
        print(venue_name)
        raise Exception("Venue name unknown: " + venue_name + "!")

# Testing functionality
""" print(get_weather_stats("2021-09-19T12:00:00+00:00", "Tapiolan Urheilupuisto"))
print(get_weather_stats("2021-06-30T15:30:00+00:00", "OmaSP Stadion"))
print(get_weather_stats("2021-10-23T14:00:00+00:00", "Wiklof Holding Arena"))
print(get_weather_stats("2021-09-26T15:30:00+00:00", "Väre Areena")) """

# Combine all finished matches from 2019-2021 to a single dataframe
fixtures2019 = pd.read_csv("fixtures2019.csv")
fixtures2020 = pd.read_csv("fixtures2020.csv")
fixtures2021 = pd.read_csv("fixtures2021.csv")
fixtures2021 = fixtures2021[fixtures2021["fixture.status.long"] == "Match Finished"]
fixtures = pd.concat([fixtures2019, fixtures2020, fixtures2021])
fixtures = fixtures.dropna(subset=["fixture.date", "fixture.venue.name"])

# Build a draframe using the weather_stats function and combine it with the matches
weather = fixtures.apply(lambda l: get_weather_stats(l["fixture.date"], l["fixture.venue.name"]), axis=1)
fixtures = pd.concat([fixtures, weather], axis=1)
print(fixtures.info)
fixtures.to_csv('fixtures_with_weather.csv', sep=',')