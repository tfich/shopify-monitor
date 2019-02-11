import requests, time, json
from threading import Thread

from classes.logger import log

CLIENT_SYNC_DELAY = 180
SEND_LOGS = False

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

class Distribute:
    def __init__(self, notifType, siteLink, siteName, notifGroup, productInfo={}):
        self.notifType = notifType
        self.siteLink = siteLink
        self.siteName = siteName
        self.notifGroup = notifGroup.lower()
        self.productInfo = productInfo

        if self.notifGroup == 'password':
            for client in CLIENTS:
                Thread(target=self.sendPassword, args=(client,)).start()

        else:
            for client in CLIENTS:
                Thread(target=self.sendProduct, args=(client,)).start()

        if SEND_LOGS and self.productInfo['filtered']:
            Thread(target=(self.sendLog)).start()

    def sendPassword(self, client):
        embed = {
            "fallback": self.notifType + ' - ' + self.siteName,
            "attachments": [
                {
                    "title": self.notifType + ' - ' + self.siteName,
                    "color": "#" + client['color'],
                    "fields": [
                    {
                        "title": "Site Link:",
                        "value": self.siteLink,
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


    def buildAtc(self, isDiscord, qtBase):
        variants = self.productInfo['variants']

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
            atcLink = self.siteLink + "/cart/" + str(var['id']) + ":1"
            varList1 += f"<{qtBase}{atcLink}|{boldOpp}{var['title']}{boldOpp}>\n"
        
        for var in vars2:
            atcLink = self.siteLink + "/cart/" + str(var['id']) + ":1"
            varList2 += f"<{qtBase}{atcLink}|{boldOpp}{var['title']}{boldOpp}>\n"

        return varList1, varList2

    def sendProduct(self, client):
        isDiscord = client['filtered'].startswith("https://discordapp.com")

        try:
            qtBase = client['quicktask']
            if qtBase.endswith('/'):
                qtBase += 'quicktasks?link='
            else:
                qtBase += '/quicktasks?link='
        except:
            qtBase = ''

        atc1, atc2 = self.buildAtc(isDiscord, qtBase)

        embed = {
            "fallback": self.notifType + ' - ' + self.productInfo['title'],
            "attachments": [
                {
                    "author_name": self.siteName + " - " + self.notifType,
                    "author_url": self.siteLink,
                    "title": self.productInfo['title'],
                    "title_link": self.productInfo['link'],
                    "color": "#" + client['color'],
                    "fields": [
                        {
                            "title": "Price:",
                            "value": self.productInfo['price'],
                            "short": False
                        }
                    ],
                    "thumb_url": self.productInfo['image'],
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
        
        if self.notifGroup == 'main':
            if self.productInfo['filtered']:
                webhook = client['filtered']
            else:
                webhook = client['unfiltered']
        else:
            webhook = client[self.notifGroup]

        for x in range(3):
            req = requests.post(webhook, json=embed, headers={"Content-Type": "application/json"})
            if req.status_code == 200:
                break

    def sendLog(self):
        payload = {
            "platform": "shopify",
            "product": self.productInfo['title'],
            "keywords": self.productInfo['filtered'],
            "site": self.siteLink,
            "link": self.productInfo['link']
        }

        for x in range(3):
            req = requests.post("https://motion-backend.herokuapp.com/api/logs", json=payload, headers={"Content-Type": "application/json"})
            if req.status_code == 200:
                break