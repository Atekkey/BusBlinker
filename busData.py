import requests
from datetime import datetime, time
import os
from env import W_KEY

def fetchData():
    api_url = "https://api.uiucbus.com/api/getdeparturesbystop?stop_id=1STDAN"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return ""

def fetchDataGreen():
    api_url = "https://api.uiucbus.com/api/getdeparturesbystop?stop_id=GRN2ND"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return ""
    
def fetchBusInfoFromDataGreen(data):
    if not data:
        return None
    departures = data.get("departures", [])
    east = None
    
    # If no busses, return None
    if not departures: 
        return None
    
    # For every bus get the headsign and expected time (split into multiple fields)
    for busInfo in departures:
        busDict = {}
        busDict["headsign"] = headsign = busInfo.get("headsign", "")
        left = headsign.split(" ")[0]
        n, let = left[0], left[-1]
        name = n+let
        if name != "5E":
            continue
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

        if east == None:
            east = busDict
        elif busDict["e_min"] < east["e_min"]:
            east = busDict
            
    
    return east


def fetchBusInfoFromData(data):
    if not data:
        return None, None
    departures = data.get("departures", [])
    south, north = None, None
    
    # If no busses, return empty list
    if not departures: 
        return None, None
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
    appid = W_KEY
    r = requests.get(url=api_url, params=dict(q='Champaign', APPID=appid))
    K = (r.json())["main"]["temp_max"] # Taking Max, check if accurate
    F = ((K - 273.15) * 9/5) + 32
    return int(F)

def myMain():
    dataNS = fetchData()
    N, S = fetchBusInfoFromData(dataNS) if dataNS else (None, None)
    dataE = fetchDataGreen()
    E = fetchBusInfoFromDataGreen(dataE) if dataE else None
    today = datetime.today()
    now = datetime.now()
    
    if N != None:
        total_seconds = (datetime.combine(today, N["time"]) - now).total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        N["time_left"] = (minutes, seconds)
    
    if S != None:
        total_seconds = (datetime.combine(today, S["time"]) - now).total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        S["time_left"] = (minutes, seconds)
    
    if E != None:
        total_seconds = (datetime.combine(today, E["time"]) - now).total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        E["time_left"] = (minutes, seconds)
    
    return N, S, E