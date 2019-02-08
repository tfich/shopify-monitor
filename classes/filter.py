import requests, time, json
from threading import Thread

from classes.logger import log

KW_SYNC_DELAY = 30

KEYWORDS = []

def kwPull():
    try:
        req = requests.get('https://motion-backend.herokuapp.com/api/monitors/keywords/shopify?apiKey=Uo4oJzjbX9kpCnl')
        return req.json()
    except:
        return []

def kwUpdater():
    global KEYWORDS
    while True:
        kwReq = kwPull()
        if kwReq:
            KEYWORDS = kwReq
        time.sleep(KW_SYNC_DELAY)

t = Thread(target=kwUpdater)
t.daemon = True
t.start()

def checkKeywords(filterStr, kwStr):
    positiveKws = []
    negativeKws = []

    for kw in kwStr.split(','): 
        if kw.startswith("+"):
            positiveKws.append(kw[1:])
        elif kw.startswith("-"):
            negativeKws.append(kw[1:])
    
    for negKw in negativeKws:
        if negKw in filterStr:
            return False

    for posKw in positiveKws:
        if posKw not in filterStr:
            return False

    return kwStr #-> true


def isFiltered(filterStr):
    filterStr = filterStr.lower()
    for kwStr in KEYWORDS:
        check = checkKeywords(filterStr, kwStr)
        if check:
            return check #-> true
    return "" #-> false



