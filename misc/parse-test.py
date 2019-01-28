import json, requests, time

url = "https://kithnyc.myshopify.com/api/product_listings.json?limit=1"

headers = {
    'x-shopify-storefront-access-token': "08430b96c47dd2ac8e17e305db3b71e8",
    'content-type': "application/json"
}

response = requests.get(url, headers=headers)

reqJson = response.json()

for product in reqJson['product_listings']:
    productInfo = {}
    productInfo['title'] = product['title']
    productInfo['handle'] = product['handle']
    productInfo['isAvailable'] = product['available']

    variants = []
    for var in product['variants']:
        varInfo = {}
        varInfo['id'] = var['id']
        varInfo['title'] = var['title']
        varInfo['isAvailable'] = var['available']
        variants.append(varInfo)
    
    productInfo['variants'] = variants
    print(productInfo)
    
