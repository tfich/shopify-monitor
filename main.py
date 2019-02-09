import time, json
from threading import Thread

from modules.monitor import Monitor

DEVELOPMENT = False

if __name__ == "__main__":
    with open('config/' + ('testingSites' if DEVELOPMENT else 'sites') + '.json') as outfile:  
        sites = json.load(outfile)

    for site in sites:
        siteInfo = sites[site]
        if siteInfo['active']:
            Thread(target=Monitor, args=(site, siteInfo)).start()


