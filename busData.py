import requests
from datetime import datetime
def fetchData():
    api_url = "https://api.uiucbus.com/api/getdeparturesbystop?stop_id=1STSTDM"
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
        busDict["expectedH"] = int(expStringHMS[:2])
        busDict["expectedM"] = int(expStringHMS[3:5])
        busDict["expectedS"] = int(expStringHMS[6:8])
        out.append(busDict)
    
    return out

def thisTimeSec():
    now = datetime.now()
    h,m  = now.strftime("%I:%M").split(":")
    sec = now.strftime("%S").zfill(2)
    tot = int(h)*3600 + int(m)*60 + int(sec)
    print(tot)
    return tot

data = fetchData()
bus_info = fetchBusInfoFromData(data)
print(bus_info)
thisTimeSec()


