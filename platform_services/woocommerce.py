import httpx

class WooCommerceService:
    async def get_products(self, shop_url: str, api_key: str, api_secret: str):
        # WooCommerce uses Basic Auth for REST API
        url = f"{shop_url}/wp-json/wc/v3/products"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=(api_key, api_secret))
            return response.json()
