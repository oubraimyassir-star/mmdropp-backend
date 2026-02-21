import httpx
import os

class ShopifyService:
    def __init__(self):
        self.client_id = os.getenv("SHOPIFY_CLIENT_ID")
        self.client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SHOPIFY_REDIRECT_URI")

    def get_auth_url(self, shop_domain: str):
        scopes = "read_products,write_products,read_orders"
        return f"https://{shop_domain}/admin/oauth/authorize?client_id={self.client_id}&scope={scopes}&redirect_uri={self.redirect_uri}"

    async def get_access_token(self, shop_domain: str, code: str):
        url = f"https://{shop_domain}/admin/oauth/access_token"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code
            })
            return response.json()

    async def get_products(self, shop_domain: str, access_token: str):
        url = f"https://{shop_domain}/admin/api/2024-01/products.json"
        headers = {"X-Shopify-Access-Token": access_token}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json().get("products", [])

    async def get_orders(self, shop_domain: str, access_token: str):
        url = f"https://{shop_domain}/admin/api/2024-01/orders.json?status=any"
        headers = {"X-Shopify-Access-Token": access_token}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json().get("orders", [])
