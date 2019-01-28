import json, time, requests

endpoint = "https://tylertesting11.myshopify.com/api/graphql.json"

schema = """
{
  products(first: 10) {
    edges {
      node {
        id
        handle
        title
        availableForSale
        updatedAt
				description
        variants(first: 20) {
          edges {
            node {
              id
              title
              availableForSale
              price
            }
          }
        }
        images(first: 1) {
          edges {
            node {
              transformedSrc
            }
          }
        }
      }
    }
  }
}
"""

headers = {
    'x-shopify-storefront-access-token': "02d3ad0e2d6c2274a844c22e82da5075",
    'content-type': "application/json"
}

response = requests.post(endpoint, json={"query": schema}, headers=headers)

reqJson = response.json()

for product in reqJson['data']['products']['edges']:
    product = product['node']
    print("title > " + product['title'])
    print("")