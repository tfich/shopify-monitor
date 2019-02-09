import json, time, requests
from threading import Thread
from base64 import b64decode

from classes.logger import log
from classes.distribute import Distribute
from classes.filter import isFiltered

PRODUCT_LIST = {}

def getCurrentDict(productId):
    return PRODUCT_LIST[productId]

def isNew(productId):
    return productId not in list(PRODUCT_LIST)

def updateList(productId, productInfo):
    PRODUCT_LIST[productId] = productInfo

CURRENCIES = {
    "USD": "$",
	"CAD": "CAD$",
	"AUD": "AUD$",
	"GBP": "£",
	"EUR": "€"
}

class Compare:
    def __init__(self, product, link, siteName, notifGroup, isBase, sendNotif):
        self.product = product
        self.link = link
        self.siteName = siteName
        self.notifGroup = notifGroup
        self.isBase = isBase
        self.sendNotif = sendNotif

        self.productInfo = {}

        self.compare()

    def isRestock(self, newVars):
        oldVarList = []
        if len(self.productInfo['variants']) > 0:
            for oldVar in self.productInfo['variants']:
                oldVarList.append(oldVar['id'])
            for newVar in newVars:
                if newVar['id'] not in oldVarList:
                    self.productInfo['variants'] = newVars
                    return True

        elif len(newVars) > 0:
            self.productInfo['variants'] = newVars
            return True

        else:
            self.productInfo['variants'] = newVars
            return False

    def compare(self):
        productId = int(b64decode(self.product['id']).decode("utf-8").split("/")[-1:][0])

        if isNew(productId):
            self.productInfo['link'] = self.link + "/products/" + self.product['handle']
            self.productInfo['title'] = self.product['title']
            
            try:
                currencyBase = CURRENCIES[self.product['priceRange']['maxVariantPrice']['currencyCode']]
            except:
                currencyBase = ''

            price = self.product['priceRange']['maxVariantPrice']['amount']
            if price.endswith(".0"):
                self.productInfo['price'] = currencyBase + price + "0"
            else:
                self.productInfo['price'] = currencyBase + price

            self.productInfo['available'] = self.product['availableForSale']

            try:
                self.productInfo['image'] = self.product['images']['edges'][0]['node']['transformedSrc'].replace("https:\/\/cdn.shopify.com", "https://cdn.shopify.com").replace("\/", "/")
            except:
                self.productInfo['image'] = "https://www.unesale.com/ProductImages/Large/notfound.png"

            if isFiltered(self.productInfo['title']):
                self.productInfo['filtered'] = True
            else:
                try:
                    t = self.product['variants']['edges'][0]['node']['title'] + self.product['variants']['edges'][0]['node']['sku']
                except:
                    t = ''         
                filterStr = self.productInfo['title'] + str(productId) + self.product['handle'].replace('-', ' ') + self.productInfo['image'] + self.product['vendor']  + ''.join(self.product['tags']) + t
                isFilt = isFiltered(filterStr)
                if isFilt:
                    self.productInfo['filtered'] = isFilt
                else:
                    self.productInfo['filtered'] = isFilt


            self.productInfo['variants'] = []

            for var in self.product['variants']['edges']:
                variant = var['node']
                if variant['availableForSale']:
                    varTemp = {}

                    varTemp['id'] = int(b64decode(variant['id']).decode("utf-8").split("/")[-1:][0])
                    varTemp['title'] = variant['title']

                    self.productInfo['variants'].append(varTemp)

            if not self.isBase and self.sendNotif:
                Thread(target=Distribute, args=("New Product", self.link, self.siteName, self.notifGroup), kwargs={"productInfo": self.productInfo}).start()
                log('[Success] Monitor change detected (new) - ' + self.productInfo['link'])

            updateList(productId, self.productInfo)

            # -> TESTING ONLY <- #
            # Thread(target=Distribute, args=("Restock", self.link, self.siteName, self.notifGroup), kwargs={"productInfo": self.productInfo}).start()
            # log('[Success] Monitor change detected (restock) - ' + self.productInfo['link'])
            # -> TESTING ONLY <- #

            return True
        
        self.productInfo = getCurrentDict(productId)

        newVars = []
        for var in self.product['variants']['edges']:
            variant = var['node']
            if variant['availableForSale']:
                varTemp = {}

                varTemp['id'] = int(b64decode(variant['id']).decode("utf-8").split("/")[-1:][0])
                varTemp['title'] = variant['title']

                newVars.append(varTemp)

        if self.isRestock(newVars):
            if not self.isBase and self.sendNotif:
                Thread(target=Distribute, args=("Restock", self.link, self.siteName, self.notifGroup), kwargs={"productInfo": self.productInfo}).start()
                log('[Success] Monitor change detected (restock) - ' + self.productInfo['link'])

            updateList(productId, self.productInfo)
            return True

        return False




        


    