import requests, time, json
from threading import Thread

from classes.logger import log

CLIENT_SYNC_DELAY = 180

CLIENTS = []

def clientPull():
    try:
        req = requests.get('https://motion-backend.herokuapp.com/api/clients/shopify?apiKey=Uo4oJzjbX9kpCnl')
        return req.json()
    except:
        return []

def clientUpdater():
    global CLIENTS
    while True:
        clientReq = clientPull()
        if clientReq:
            CLIENTS = clientReq
        time.sleep(CLIENT_SYNC_DELAY)

t = Thread(target=clientUpdater)
t.daemon = True
t.start()

def builtAtcLinks(variants, isDiscord):
    if isDiscord:
        boldOpp = ''
    else:
        boldOpp = '*'
        
    if len(variants) % 2 == 0:
        vars1 = variants[:len(variants)//2]
        vars2 = variants[len(variants)//2:]
    else:
        vars1 = variants[:len(variants)//2 + 1]
        vars2 = variants[len(variants)//2 + 1:]
    
    varList1 = ''
    varList2 = ''

    for var in vars1:
        atcLink = self.link + "/cart/" + var['id'] + ":1"
        varList1 += f"<{atcLink}|{boldOpp}{var['title']}{boldOpp}>"
    
    for var in vars2:
        atcLink = self.link + "/cart/" + var['id'] + ":1"
        varList2 += f"<{atcLink}|{boldOpp}{var['title']}{boldOpp}>"

    return varList1, varList2

def sendPassword(notifType, siteLink, siteName, client):
    embed = {
        "fallback": notifType + ' - ' + siteName,
        "attachments": [
            {
                "title": notifType + ' - ' + siteName,
                "color": "#" + client['color'],
                "fields": [
                {
                    "title": "Site Link:",
                    "value": siteLink,
                    "short": False
                }
                ],
                "footer_icon": client['icon'],
                "footer": client['footer'],
                "ts": time.time()
            }
        ]
    }

    for x in range(3):
        req = requests.post(client['password'], json=embed, headers={"Content-Type": "application/json"})
        if req.status_code == 200:
            break

def buildAtc(productInfo, link, isDiscord):
    variants = productInfo['variants']

    if isDiscord:
        boldOpp = ''
    else:
        boldOpp = '*'
        
    if len(variants) % 2 == 0:
        vars1 = variants[:len(variants)//2]
        vars2 = variants[len(variants)//2:]
    else:
        vars1 = variants[:len(variants)//2 + 1]
        vars2 = variants[len(variants)//2 + 1:]
    
    varList1 = ''
    varList2 = ''

    try:
        qtBase = client['quicktask']
        if qtBase.endswith('/'):
            qtBase += 'quicktasks?link='
        else:
            qtBase += '/quicktasks?link='
    except:
        qtBase = ''

    print(qtBase)
    print("fsadf")

    for var in vars1:
        atcLink = link + "/cart/" + var['id'] + ":1"
        varList1 += f"<{qtBase}{atcLink}|{boldOpp}{var['title']}{boldOpp}>"
    
    for var in vars2:
        atcLink = link + "/cart/" + var['id'] + ":1"
        varList2 += f"<{qtBase}{atcLink}|{boldOpp}{var['title']}{boldOpp}>"

    return varList1, varList2

def sendProduct(notifType, siteLink, siteName, productInfo, client):
    isDiscord = client['filtered'].startswith("https://discordapp.com")

    atc1, atc2 = buildAtc(productInfo, link, isDiscord)

    embed = {
        "fallback": notifType + ' - ' + productInfo['title'],
        "attachments": [
            {
                "author_name": siteName + " - " + notifType,
                "author_url": siteLink,
                "title": productInfo['title'],
                "title_link": productInfo['link'],
                "color": "#" + client['color'],
                "fields": [
                {
                    "title": "Price:",
                    "value": productInfo['price'],
                    "short": False
                }
                ],
                "thumb_url": productInfo['image'],
                "footer_icon": client['icon'],
                "footer": client['footer'],
                "ts": time.time()
            }
        ]
    }

    if atc1:
        embed['attachments'][0]['fields'].append({
            "title": "Variants:",
            "value": atc1,
            "short": True
        })

    if atc2:
        embed['attachments'][0]['fields'].append({
            "title": "Variants:",
            "value": atc2,
            "short": True
        })

    if productInfo['filtered']:
        webhook = client['filtered']
    else:
        webhook = client['unfiltered']

    for x in range(3):
        req = requests.post(webhook, json=embed, headers={"Content-Type": "application/json"})
        if req.status_code == 200:
            break

class Distribute:
    def __init__(self, notifType, siteLink, siteName, isPassword=False, productInfo={}):
        self.notifType = notifType
        self.siteLink = siteLink
        self.siteName = siteName
        self.productInfo = productInfo

        if isPassword:
            for client in CLIENTS:
                Thread(target=sendPassword, args=(client)).start()

        else:
            for client in CLIENTS:
                print(client)
                Thread(target=sendProduct, args=(client)).start()

