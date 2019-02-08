import json, time, requests
from threading import Thread

from config.schema import SCHEMA
from classes.logger import log

endpoints = [
    ["https://kithnyc.myshopify.com/api/graphql.json", "08430b96c47dd2ac8e17e305db3b71e8"],
    ["https://tylertesting11.myshopify.com/api/graphql.json", "02d3ad0e2d6c2274a844c22e82da5075"]
]

def sendReq(site):
    print(site)
    headers = {
            "X-Shopify-Storefront-Access-Token": site[1],
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
            "content-type": "application/json"
        }
    schema1 = SCHEMA.replace("{PRODUCT_CONNECTION}", "first: 250, reverse: false")
    req = requests.post(site[0], json={"query": schema1}, headers=headers)
    print(req.status_code)
    if req.status_code != 200 or "thro" in req.text:
        log("[Fail] - request throttled")
    else:
        log("[Successful] - verified request")

for x in range(150):
    time.sleep(1)
    if x % 2 == 0:
        Thread(target=sendReq, args=(endpoints[0],)).start()
    else:
        Thread(target=sendReq, args=(endpoints[1],)).start()

