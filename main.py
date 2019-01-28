import requests, time, json
from threading import Thread

from classes.getSiteInfo import getSiteInfo
from modules.monitor import Monitor

SYNC_SLEEP = 120

# -> open and read config files
with open('config/siteInfo.json') as outfile:  
    siteInfo = json.load(outfile)


# -> get links from database
def getLinks():
    for x in range(0, 3):
        req = requests.get('https://motion-backend.herokuapp.com/api/monitors/links/shopify?apiKey=Uo4oJzjbX9kpCnl')
        if req.status_code == 200:
            return req.json()
    return []

if __name__ == "__main__":
    sitesRunning = []

    while True:
        for link in getLinks():
            link = link.replace("www.", "").replace("http://", "https://")
            if link.endswith("/"):
                link = link[:-1]

            if link not in list(sitesRunning):
                if not siteInfo.get(link):
                    siteInfo = getSiteInfo(link)
                    sitesRunning.append(siteInfo)
                    Thread(target=Monitor, args=(link, siteInfo)).start()

                else:
                    sitesRunning.append(siteInfo[link])
                    Thread(target=Monitor, args=(link, siteInfo[link])).start()

        time.sleep(SYNC_SLEEP)


