import time, json
from threading import Thread

from modules.monitor import Monitor

if __name__ == "__main__":
    with open('config/testingSites.json') as outfile:  
        sites = json.load(outfile)

    for site in sites:
        siteInfo = sites[site]
        if siteInfo['active']:
            Thread(target=Monitor, args=(site, siteInfo)).start()


