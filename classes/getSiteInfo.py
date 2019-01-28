import json, requests
from bs4 import BeautifulSoup as BS

from classes.logger import log


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
        log("[Fatal] - Unable to get site info - Site ommited - " + site)
        return {}