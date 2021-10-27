from numpy.core.numeric import NaN
import pandas as pd
from datetime import datetime, timedelta

espoo_weather = pd.read_csv("data/espoo_tapiola_1km.csv")
hattula_weather = pd.read_csv("data/hattula_lepaa_eituulta_eipilvia_22km.csv")
helsinki_weather = pd.read_csv("data/helsinki_kaisaniemi_2km.csv")
kotka_weather = pd.read_csv("data/kotka_rankki_9km.csv")
kuopio_weather = pd.read_csv("data/kuopio_savilahti_2km.csv")
lahti_weather = pd.read_csv("data/lahti_sopenkorpi_eituulta_1km.csv")
maarianhamina_weather = pd.read_csv("data/maarianhamina_lentoasema_eisadetta_3km.csv")
oulu_weather = pd.read_csv("data/oulu_oulunsalo_10km.csv")
seinajoki_weather = pd.read_csv("data/seinajoki_pelmaa_eipilvia_24km.csv")
tampere_weather = pd.read_csv("data/tampere_harmala_eituulta_4km.csv")
turku_weather = pd.read_csv("data/turku_artukainen_6km.csv")

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
    return ret

def get_weather_stats(match_timestamp, venue_name):
    date = datetime.fromisoformat(match_timestamp)
    
    if venue_name == "Tapiolan Urheilupuisto":
        return form_return_dict(espoo_weather, date, 1)
    elif venue_name == "Tehtaan kenttä":
        return form_return_dict(hattula_weather, date, 22)
    elif venue_name == "Bolt Arena":
        return form_return_dict(helsinki_weather, date, 2)
    elif venue_name == "Arto Tolsa Areena":
        return form_return_dict(kotka_weather, date, 9)
    elif venue_name == "Savon Sanomat Areena" or venue_name == "Väre Areena":
        return form_return_dict(kuopio_weather, date, 2)
    elif venue_name == "Lahden Stadion":
        return form_return_dict(lahti_weather, date, 1)
    elif venue_name == "Wiklöf Holding Arena" or venue_name == "Wiklof Holding Arena":
        return form_return_dict(maarianhamina_weather, date, 3)
    elif venue_name == "Raatin stadion" or venue_name == "Raatti Tekonurmi":
        return form_return_dict(oulu_weather, date, 10)
    elif venue_name == "OmaSP Stadion":
        return form_return_dict(seinajoki_weather, date, 24)
    elif venue_name == "Ratinan Stadion":
        return form_return_dict(tampere_weather, date, 4)
    elif venue_name == "Veritas Stadion":
        return form_return_dict(turku_weather, date, 6)
    else:
        raise Exception("Venue name unknown: " + venue_name + "!")

# Testing functionality
print(get_weather_stats("2021-09-19T12:00:00+00:00", "Tapiolan Urheilupuisto"))
print(get_weather_stats("2021-06-30T15:30:00+00:00", "OmaSP Stadion"))
print(get_weather_stats("2021-10-23T14:00:00+00:00", "Wiklof Holding Arena"))
print(get_weather_stats("2021-09-26T15:30:00+00:00", "Väre Areena"))

