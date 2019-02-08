import json, os, requests
from bs4 import BeautifulSoup as BS

def getSiteInfo(site):

    siteInfo = {}
    try:
        reqHtml = requests.get(site + "/index.js")
        reqSoup = BS(reqHtml.text, "html.parser")
        siteInfo['apiKey'] = json.loads(reqSoup.find("script", {'id': 'shopify-features'}).text)['accessToken']

        reqMeta = requests.get(site + "/meta.json")
        metaJson = reqMeta.json()
        siteInfo['siteName'] = metaJson['name']
        siteInfo['myShopifyDomain'] = metaJson['myshopify_domain']
        return siteInfo
    except Exception as e:
        print("[Fatal] - Unable to get site info - Site ommited - " + site)
        return {}

newSiteUrl = input("Site URL > ")

filename = '../config/sites.json'
with open(filename, 'r') as f:
    data = json.load(f)

siteInfo = getSiteInfo(newSiteUrl)
siteInfo['notifGroup'] = 'main'
siteInfo['active'] = True
siteInfo['url'] = newSiteUrl

data[newSiteUrl] = siteInfo
print(data[newSiteUrl])

os.remove(filename)
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)