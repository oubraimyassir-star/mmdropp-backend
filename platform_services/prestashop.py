import httpx
import xml.etree.ElementTree as ET

class PrestaShopService:
    async def get_products(self, shop_url: str, api_key: str):
        # PrestaShop uses key as username, empty password in Basic Auth
        url = f"{shop_url}/api/products?display=full&output_format=JSON"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=(api_key, ""))
            return response.json().get("products", [])
