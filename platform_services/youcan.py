import httpx
import os

class YouCanService:
    def __init__(self):
        self.client_id = os.getenv("YOUCAN_CLIENT_ID")
        self.client_secret = os.getenv("YOUCAN_CLIENT_SECRET")
        self.redirect_uri = os.getenv("YOUCAN_REDIRECT_URI")

    def get_auth_url(self):
        # YouCan OAuth url pattern (example)
        scopes = "read_products,read_orders"
        return f"https://seller-area.youcan.shop/admin/oauth/authorize?client_id={self.client_id}&scope={scopes}&redirect_uri={self.redirect_uri}&response_type=code"

    async def get_access_token(self, code: str):
        url = "https://api.youcan.shop/oauth/token"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri
            })
            return response.json()

    async def get_products(self, access_token: str):
        url = "https://api.youcan.shop/products"
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json().get("data", [])

    async def get_orders(self, access_token: str):
        url = "https://api.youcan.shop/orders"
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"DEBUG: Fetching orders from {url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            print(f"DEBUG: YouCan Orders Response Status: {response.status_code}")
            print(f"DEBUG: YouCan Orders Response Body: {response.text[:500]}")
            return response.json().get("data", [])
