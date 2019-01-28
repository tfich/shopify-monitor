import requests, json, time
from threading import Thread

from config.schema import SCHEMA

from modules.compare import Compare

from classes.logger import log
from classes.timeParser import timeParser
from classes.distribute import Distribute

MONITOR_SLEEP = 10

class Monitor:
    def __init__(self, link, siteInfo):
        self.link = link
        self.siteName = siteInfo['siteName']
        self.shopifyDomain = "https://" + siteInfo['myShopifyDomain']

        self.headers = {
            "X-Shopify-Storefront-Access-Token": siteInfo['apiKey'],
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
            "content-type": "application/json"
        }

        self.isBase = True
        self.isPasswordUp = False
        self.lastUpdated = '0'

        self.run()

    def scrape(self):
        if self.isBase:
            connection = "first: 100, reverse: true"
        else:
            connection = """first: 100, reverse: true, query: "updated_at:>='{}'" """.format(str(self.lastUpdated))

        schema = SCHEMA.replace("{PRODUCT_CONNECTION}", connection)

        try:
            req = requests.post(self.shopifyDomain + '/api/graphql.json', json={"query": schema}, headers=self.headers, proxies=False)
        except Exception as e:
            log('[Error] Unable to make /graphql.json request - ' + str(e) + ' - ' + self.link)
            return False

        if req.status_code == 403 or req.status_code == 430:
            log('[Error] Proxy banned on /graphql.json request!')
            return False

        if req.status_code == 401 or req.status_code == 400:
            if not self.isPasswordUp:
                self.isPasswordUp = True
                if not self.isBase:
                    Thread(target=Distribute, args=("Password Page Up", self.link, self.siteName), kwargs={"isPassword": True}).start()
                    log('Password Page Up - ' + self.link)
            return False

        if self.isPasswordUp:
            self.isPasswordUp = False
            if not self.isBase:
                Thread(target=Distribute, args=("Password Page Down", self.link, self.siteName), kwargs={"isPassword": True}).start()
                log('Password Page Down - ' + self.link)

        if req.status_code == 304:
            pass

        if req.status_code != 200:
            log('[Error] Unknown status code on /graphql.json request - ' + str(req.status_code))
            return False

        try:
            self.parse(req.json())
            return True
        except Exception as e:
            log('[Error] Unable to parse /graphql.json sitemap - ' + self.link)
            return False


    def parse(self, reqJson):
        tempUpdated = '0'

        for product in reqJson['data']['products']['edges']:
            product = product['node']

            updatedAt = str(timeParser(product['updatedAt']))

            if updatedAt > str(self.lastUpdated):
                if updatedAt > str(tempUpdated):
                    tempUpdated = updatedAt

                Thread(target=Compare, args=(product, self.link, self.siteName, self.isBase)).start()

        if tempUpdated > self.lastUpdated:
            self.lastUpdated = tempUpdated

        
    def run(self):
        while True:
            for x in range(3):
                if self.scrape():
                        break
                else:
                    time.sleep(.1)

            if self.isBase:
                log('[Success] Finished inital /graphql.json scrape - ' + self.link)
                self.isBase = False
            else:
                log('[Success] Scraped completed - ' + self.link)
            
            time.sleep(MONITOR_SLEEP)
