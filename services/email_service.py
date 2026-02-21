import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.demo_mode = not self.api_key or self.api_key == "re_..."

    async def send_marketing_email(self, to_email: str, subject: str, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a marketing email using a template.
        """
        if self.demo_mode:
            return self._send_mock_email(to_email, subject, template_name, context)
        
        return await self._send_real_email(to_email, subject, template_name, context)

    def _send_mock_email(self, to_email: str, subject: str, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[MOCK EMAIL] To: {to_email} | Subject: {subject} | Template: {template_name}")
        return {
            "status": "sent_mock",
            "to": to_email,
            "subject": subject,
            "template": template_name,
            "message_id": f"mock-{os.urandom(8).hex()}"
        }

    async def _send_real_email(self, to_email: str, subject: str, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for Resend API
        # import resend
        # resend.api_key = self.api_key
        # r = resend.Emails.send({ ... })
        return {"error": "Real email API integration pending configuration", "fallback": self._send_mock_email(to_email, subject, template_name, context)}

# Singleton instance
email_service = EmailService()
