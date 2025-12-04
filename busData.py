import requests
def fetchData():
    api_url = "https://api.uiucbus.com/api/getdeparturesbystop?stop_id=1STSTDM"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return ""
data = fetchData()