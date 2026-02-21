import google.generativeai as genai
import json
import os
from typing import Dict, Any

class ContentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_landing_page(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-converting landing page content using Gemini AI."""
        if not self.api_key:
            return self._get_mock_landing_page(product_data)

        prompt = f"""
        Tu es un expert en e-commerce et en copywriting de luxe. 
        Génère les textes pour une landing page haut de gamme pour le produit suivant:
        Nom: {product_data.get('product_name')}
        Catégorie: {product_data.get('category')}
        Cible: {product_data.get('target_audience')}
        Bénéfice principal: {product_data.get('main_benefit')}
        Ton: {product_data.get('brand_voice')}
        Style Visuel souhaité: {product_data.get('style')}

        Réponds UNIQUEMENT avec un objet JSON structuré comme suit:
        {{
            "brand_name": "Nom de la marque",
            "hero": {{
                "badge": "Petit texte au-dessus du titre",
                "headline": "Titre accrocheur et puissant",
                "subheadline": "Sous-titre persuasif",
                "cta_text": "Texte du bouton",
                "image_prompt": "Prompt détaillé pour générer une image réaliste du produit dans un style {product_data.get('style')}"
            }},
            "stats": [
                {{"value": "Chiffre", "label": "Légende"}},
                {{"value": "Chiffre", "label": "Légende"}}
            ],
            "problem": {{
                "title": "Le défi que vos clients rencontrent",
                "pain_points": [
                    {{"text": "Point de douleur 1"}},
                    {{"text": "Point de douleur 2"}}
                ]
            }},
            "solution": {{
                "title": "Pourquoi {product_data.get('product_name')} est la solution",
                "description": "Description détaillée orientée bénéfices",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"
            }},
            "features": [
                {{"title": "Caractéristique 1", "description": "Bénéfice 1"}},
                {{"title": "Caractéristique 2", "description": "Bénéfice 2"}},
                {{"title": "Caractéristique 3", "description": "Bénéfice 3"}}
            ],
            "expert_endorsement": {{
                "quote": "Une citation d'expert ou de client",
                "name": "Nom",
                "role": "Expert / Client",
                "image_prompt": "Prompt pour un portrait d'expert professionnel"
            }},
            "express_checkout": {{
                "urgency_msg": "Message d'urgence",
                "product_name": "{product_data.get('product_name')}",
                "product_image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
                "options": [
                    {{"name": "Standard", "price": 29, "old_price": 49, "desc": "Pack de démarrage", "featured": false}},
                    {{"name": "Premium", "price": 49, "old_price": 89, "desc": "Pack complet", "featured": true}}
                ]
            }},
            "seo": {{
                "title": "Titre SEO",
                "description": "Meta description"
            }}
        }}

        Les textes doivent être en Français, percutants et adaptés au style {product_data.get('style')}.
        """

        try:
            response = self.model.generate_content(prompt)
            # Find JSON in the response
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            json_str = text[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return self._get_mock_landing_page(product_data)

    def _get_mock_landing_page(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "theme": "LUXE",
            "brand_name": product_data.get("product_name", "Brand"),
            "hero": {
                "badge": "Édition Limitée",
                "headline": f"Redéfinissez votre {product_data.get('category', 'style')}",
                "subheadline": f"Le futur de {product_data.get('product_name', 'votre expérience')} est ici.",
                "cta_text": "Découvrir maintenant",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"
            },
            "stats": [
                {"value": "99.9%", "label": "Satisfaction"},
                {"value": "24h", "label": "Expédition"}
            ],
            "problem": {
                "title": "Ne vous contentez plus du standard",
                "pain_points": [{"text": "Qualité médiocre"}, {"text": "Design obsolète"}]
            },
            "solution": {
                "title": "L'Excellence ConvertAI",
                "description": f"{product_data.get('product_name')} allie performance et esthétique pour un résultat incomparable.",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"
            },
            "features": [],
            "express_checkout": {
                "urgency_msg": "Plus que quelques exemplaires en stock",
                "product_name": product_data.get("product_name", "Produit"),
                "product_image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
                "options": []
            }
        }

    async def generate_seo(self, product: Any) -> Dict[str, Any]:
        return {"title": "SEO Placeholder", "description": "SEO Description"}

    async def generate_social(self, product: Any) -> Dict[str, Any]:
        return {"caption": "Social Post Placeholder"}

    async def generate_technical_sheet(self, req: Any) -> Dict[str, Any]:
        return {"content": "Technical Sheet Placeholder"}

    async def generate_image(self, req: Any) -> Dict[str, Any]:
        return {"url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"}

