import requests
from datetime import datetime, time
import os

def fetchData():
    api_url = "https://api.uiucbus.com/api/getdeparturesbystop?stop_id=1STDAN"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return ""

def fetchBusInfoFromData(data):
    departures = data.get("departures", [])
    south, north = None, None
    
    # If no busses, return empty list
    if not departures: 
        return ()
    found = set([])
    # For every bus get the headsign and expected time (split into multiple fields)
    for busInfo in departures:
        busDict = {}
        busDict["headsign"] = headsign = busInfo.get("headsign", "")
        left = headsign.split(" ")[0]
        n, let = left[0], left[-1]
        name = n+let
        if name not in ["2N", "2S", "5E"]:
            continue
        if name in found:
            continue
        found.add(name)
        expString = busInfo.get("expected", "")
        if expString == "":
            continue
        expStringHMS = expString[-14:-6]
        busDict["expectedHMS"] = expStringHMS
        h = int(expStringHMS[:2])
        m = int(expStringHMS[3:5])
        s = int(expStringHMS[6:8])
        busDict["time"] = time(hour=h, minute=m, second=s)
        busDict["e_min"] = busInfo["expected_mins"]
        if name == "2S":
            if south == None:
                south = busDict
            elif busDict["e_min"] < south["e_min"]:
                south = busDict
        elif name == "2N":
            if north == None:
                north = busDict
            elif busDict["e_min"] < north["e_min"]:
                north = busDict
            
    
    return north, south

def fetchTemp():
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    appid = os.getenv("API_KEY") 
    r = requests.get(url=api_url, params=dict(q='Champaign', APPID=appid))
    print(r)
    print(r.json())
    K = (r.json())["main"]["feels_like"]
    F = ((K - 273.15) * 9/5) + 32
    return int(F)

def myMain():
    data = fetchData()
    N, S = fetchBusInfoFromData(data)
    today = datetime.today()
    now = datetime.now()
    
    total_seconds = (datetime.combine(today, N["time"]) - now).total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    N["time_left"] = (minutes, seconds)

    total_seconds = (datetime.combine(today, S["time"]) - now).total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    S["time_left"] = (minutes, seconds)
    
    return N, S
