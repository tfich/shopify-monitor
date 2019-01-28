SCHEMA = """
{
  products({PRODUCT_CONNECTION}) {
    edges {
      node {
        id
        handle
        title
        availableForSale
        updatedAt
        vendor
        tags
        priceRange {
          maxVariantPrice {
            amount
            currencyCode
          }
        }
        variants(first: 20) {
          edges {
            node {
              id
              title
              sku
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

