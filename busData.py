import requests
from datetime import datetime, time

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
    out = []
    
    # If no busses, return empty list
    if not departures: 
        return out
    found = set([])
    # For every bus get the headsign and expected time (split into multiple fields)
    for busInfo in departures:
        busDict = {}
        busDict["headsign"] = headsign = busInfo.get("headsign", "")
        left = headsign.split(" ")[0]
        if left not in ["220N", "220S", "22N", "22S", "50E", "5E"]:
            continue
        if left in found:
            continue
        found.add(left)
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
        out.append(busDict)
    
    return out



def myMain():
    data = fetchData()
    bus_info = fetchBusInfoFromData(data)
    today = datetime.today()
    now = datetime.now()

    for bus in bus_info:
        total_seconds = (datetime.combine(today, bus["time"]) - now).total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        bus["time_left"] = (minutes, seconds)
    
    return bus_info



