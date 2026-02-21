import logging
import asyncio

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.version}/{self.phone_number_id}"
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def send_text_message(self, to: str, message: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """Sends a plain text message via Meta API with retry logic."""
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        for attempt in range(max_retries):
            try:
                response = await self.client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_data = e.response.json()
                error_code = error_data.get("error", {}).get("code", 0)
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                
                # Non-retryable errors
                if error_code in [131031, 131026]: # Invalid phone, restricted
                    logger.error(f"WhatsApp Non-retryable error: {error_msg}")
                    return {"error": error_msg, "code": error_code}
                
                # Rate limit backoff
                if error_code == 130429:
                    wait_time = 2 ** attempt
                    logger.warning(f"WhatsApp Rate limit hit, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    continue

                if attempt == max_retries - 1:
                    logger.error(f"WhatsApp API persistent error: {error_msg}")
                    return {"error": error_msg, "code": error_code}
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"WhatsApp Unexpected error: {e}")
                if attempt == max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(1)
        return None

    async def send_template_message(self, to: str, template_name: str, language_code: str = "fr", components: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sends a template message."""
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": components or []
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """Marks a message as read."""
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    def generate_whatsapp_link(self, phone: str, message: str) -> str:
        """Generates a wa.me link with a pre-filled message."""
        encoded_message = urllib.parse.quote(message)
        clean_phone = "".join(filter(str.isdigit, phone))
        return f"https://wa.me/{clean_phone}?text={encoded_message}"

# Singleton instance
whatsapp_service = WhatsAppService()

