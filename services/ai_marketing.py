import os
import json
import google.generativeai as genai
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class AIMarketingService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_response(self, context: Dict[str, Any]) -> str:
        """
        Generates a WhatsApp message based on context.
        """
        if not self.api_key:
            return "Bonjour ! Comment pouvons-nous vous aider aujourd'hui ?"

        customer_name = context.get("customer_name", "Client")
        history = context.get("conversation_history", [])
        intent = context.get("intent", "general")
        cart_info = context.get("cart_info")

        system_prompt = """
        Tu es un assistant commercial expert pour une boutique e-commerce.
        Tu communiques via WhatsApp de manière professionnelle mais amicale.

        RÈGLES:
        - Messages courts et directs (max 2-3 phrases)
        - Utilise des emojis avec parcimonie (1 ou 2 max)
        - Pose UNE seule question à la fois
        - Réponds en français
        - Sois empathique et à l'écoute
        """

        user_prompt = f"Client: {customer_name}\nIntention: {intent}\n"
        if cart_info:
            user_prompt += f"Panier: {json.dumps(cart_info)}\n"
        
        if history:
            user_prompt += "Historique récent:\n"
            for msg in history[-5:]:
                role = "Assistant" if msg.get("role") == "assistant" else "Client"
                user_prompt += f"{role}: {msg.get('content')}\n"

        prompt = f"{system_prompt}\n\n{user_prompt}\n\nGénère la réponse WhatsApp optimale:"

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"AI Marketing Error: {e}")
            return "Désolé, je rencontre une petite difficulté technique. Comment puis-je vous aider ?"

    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Analyzes the intent of an incoming WhatsApp message.
        """
        if not self.api_key:
            return {"intent": "other", "sentiment": "neutral", "urgency": "low"}

        prompt = f"""
        Analyse ce message WhatsApp et retourne un JSON avec:
        {{
          "intent": "greeting|product_inquiry|order_status|complaint|closing_signal|other",
          "sentiment": "positive|neutral|negative",
          "urgency": "high|medium|low",
          "entities": {{
            "product_mentioned": "nom du produit si présent",
            "price_mentioned": true/false
          }}
        }}

        Message: "{message}"
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            return json.loads(text[start:end])
        except Exception as e:
            print(f"Intent Analysis Error: {e}")
            return {"intent": "other", "sentiment": "neutral", "urgency": "low"}

ai_marketing_service = AIMarketingService()
