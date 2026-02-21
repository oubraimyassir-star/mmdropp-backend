from typing import Dict, Any, Optional
import random

class BannerService:
    """
    Service for generating promotional banners with AI backgrounds and text overlays.
    """
    
    # Template definitions with dimensions and layouts
    # Visual Theme Templates with pre-designed aesthetics
    TEMPLATES = {
        "trend_steps": {
            "name": "Trend Steps",
            "width": 1200,
            "height": 628,
            "description": "Style tendance avec dégradé rouge moderne",
            "theme": {
                "primary_color": "#E63946",
                "secondary_color": "#F1FAEE",
                "accent_color": "#A8DADC",
                "text_color": "#FFFFFF",
                "background_style": "gradient_red"
            },
            "text_layout": {
                "headline": {"x": 60, "y": 200, "max_width": 1080, "font_size": 64, "font_weight": "bold", "align": "left"},
                "subheadline": {"x": 60, "y": 300, "max_width": 900, "font_size": 32, "font_weight": "normal", "align": "left"},
                "cta": {"x": 60, "y": 480, "max_width": 250, "font_size": 24, "font_weight": "bold", "align": "left"}
            }
        },
        "pure_beaute": {
            "name": "Pure Beauté",
            "width": 1080,
            "height": 1080,
            "description": "Élégance minimaliste avec tons pastel",
            "theme": {
                "primary_color": "#D4A5A5",
                "secondary_color": "#FFFFFF",
                "accent_color": "#9D8189",
                "text_color": "#2D2D2D",
                "background_style": "soft_pastel"
            },
            "text_layout": {
                "headline": {"x": 90, "y": 400, "max_width": 900, "font_size": 72, "font_weight": "bold", "align": "center"},
                "subheadline": {"x": 90, "y": 550, "max_width": 900, "font_size": 36, "font_weight": "normal", "align": "center"},
                "cta": {"x": 340, "y": 800, "max_width": 400, "font_size": 28, "font_weight": "bold", "align": "center"}
            }
        },
        "style_elle": {
            "name": "Style Elle",
            "width": 1080,
            "height": 1920,
            "description": "Design féminin et sophistiqué",
            "theme": {
                "primary_color": "#FF6B9D",
                "secondary_color": "#FFF0F5",
                "accent_color": "#C9184A",
                "text_color": "#FFFFFF",
                "background_style": "elegant_pink"
            },
            "text_layout": {
                "headline": {"x": 90, "y": 800, "max_width": 900, "font_size": 80, "font_weight": "bold", "align": "center"},
                "subheadline": {"x": 90, "y": 1050, "max_width": 900, "font_size": 42, "font_weight": "normal", "align": "center"},
                "cta": {"x": 290, "y": 1500, "max_width": 500, "font_size": 32, "font_weight": "bold", "align": "center"}
            }
        },
        "tech_modern": {
            "name": "Tech Modern",
            "width": 1280,
            "height": 720,
            "description": "Style technologique avec bleu électrique",
            "theme": {
                "primary_color": "#0066FF",
                "secondary_color": "#00D9FF",
                "accent_color": "#1A1A2E",
                "text_color": "#FFFFFF",
                "background_style": "tech_gradient"
            },
            "text_layout": {
                "headline": {"x": 80, "y": 200, "max_width": 1120, "font_size": 88, "font_weight": "bold", "align": "left"},
                "subheadline": {"x": 80, "y": 350, "max_width": 900, "font_size": 40, "font_weight": "normal", "align": "left"},
                "cta": {"x": 80, "y": 550, "max_width": 300, "font_size": 26, "font_weight": "bold", "align": "left"}
            }
        },
        "minimal_chic": {
            "name": "Minimal Chic",
            "width": 1920,
            "height": 600,
            "description": "Minimalisme noir et blanc épuré",
            "theme": {
                "primary_color": "#000000",
                "secondary_color": "#FFFFFF",
                "accent_color": "#808080",
                "text_color": "#000000",
                "background_style": "minimal_white"
            },
            "text_layout": {
                "headline": {"x": 100, "y": 180, "max_width": 1200, "font_size": 76, "font_weight": "bold", "align": "left"},
                "subheadline": {"x": 100, "y": 300, "max_width": 900, "font_size": 38, "font_weight": "normal", "align": "left"},
                "cta": {"x": 100, "y": 450, "max_width": 280, "font_size": 24, "font_weight": "bold", "align": "left"}
            }
        },
        "bold_impact": {
            "name": "Bold Impact",
            "width": 1200,
            "height": 628,
            "description": "Impact visuel fort avec jaune vibrant",
            "theme": {
                "primary_color": "#FFD60A",
                "secondary_color": "#000814",
                "accent_color": "#FFC300",
                "text_color": "#000000",
                "background_style": "bold_yellow"
            },
            "text_layout": {
                "headline": {"x": 60, "y": 200, "max_width": 1080, "font_size": 64, "font_weight": "bold", "align": "left"},
                "subheadline": {"x": 60, "y": 300, "max_width": 900, "font_size": 32, "font_weight": "normal", "align": "left"},
                "cta": {"x": 60, "y": 480, "max_width": 250, "font_size": 24, "font_weight": "bold", "align": "left"}
            }
        },
        "elegant_gold": {
            "name": "Elegant Gold",
            "width": 600,
            "height": 300,
            "description": "Luxe et raffinement avec or",
            "theme": {
                "primary_color": "#D4AF37",
                "secondary_color": "#1A1A1A",
                "accent_color": "#F4E5C3",
                "text_color": "#FFFFFF",
                "background_style": "luxury_dark"
            },
            "text_layout": {
                "headline": {"x": 40, "y": 100, "max_width": 520, "font_size": 44, "font_weight": "bold", "align": "center"},
                "subheadline": {"x": 40, "y": 170, "max_width": 520, "font_size": 20, "font_weight": "normal", "align": "center"},
                "cta": {"x": 200, "y": 230, "max_width": 200, "font_size": 16, "font_weight": "bold", "align": "center"}
            }
        },
        "fresh_green": {
            "name": "Fresh Green",
            "width": 1080,
            "height": 1080,
            "description": "Fraîcheur naturelle avec vert",
            "theme": {
                "primary_color": "#52B788",
                "secondary_color": "#D8F3DC",
                "accent_color": "#2D6A4F",
                "text_color": "#FFFFFF",
                "background_style": "nature_green"
            },
            "text_layout": {
                "headline": {"x": 90, "y": 400, "max_width": 900, "font_size": 72, "font_weight": "bold", "align": "center"},
                "subheadline": {"x": 90, "y": 550, "max_width": 900, "font_size": 36, "font_weight": "normal", "align": "center"},
                "cta": {"x": 340, "y": 800, "max_width": 400, "font_size": 28, "font_weight": "bold", "align": "center"}
            }
        },
        "sunset_vibes": {
            "name": "Sunset Vibes",
            "width": 1080,
            "height": 1920,
            "description": "Ambiance coucher de soleil chaleureux",
            "theme": {
                "primary_color": "#FF6B35",
                "secondary_color": "#F7931E",
                "accent_color": "#C1121F",
                "text_color": "#FFFFFF",
                "background_style": "warm_sunset"
            },
            "text_layout": {
                "headline": {"x": 90, "y": 800, "max_width": 900, "font_size": 80, "font_weight": "bold", "align": "center"},
                "subheadline": {"x": 90, "y": 1050, "max_width": 900, "font_size": 42, "font_weight": "normal", "align": "center"},
                "cta": {"x": 290, "y": 1500, "max_width": 500, "font_size": 32, "font_weight": "bold", "align": "center"}
            }
        }
    }
    
    COLOR_SCHEMES = {
        "brand": {"primary": "#6366f1", "secondary": "#ec4899", "text": "#ffffff", "background": "#1e293b"},
        "vibrant": {"primary": "#f59e0b", "secondary": "#10b981", "text": "#ffffff", "background": "#0f172a"},
        "elegant": {"primary": "#8b5cf6", "secondary": "#06b6d4", "text": "#ffffff", "background": "#1e1b4b"},
        "minimal": {"primary": "#000000", "secondary": "#ffffff", "text": "#000000", "background": "#f8fafc"},
        "sunset": {"primary": "#ef4444", "secondary": "#f59e0b", "text": "#ffffff", "background": "#7c2d12"}
    }
    
    def __init__(self):
        pass
    
    async def generate_banner(
        self,
        template: str,
        headline: str,
        subheadline: Optional[str] = None,
        cta_text: Optional[str] = None,
        background_prompt: str = "",
        color_scheme: str = "brand",  # Kept for backward compatibility but not used
        style: str = "banner"
    ) -> Dict[str, Any]:
        """
        Generate a promotional banner with AI background and text overlay metadata.
        
        Intelligently uses product information to create a cohesive design.
        """
        
        if template not in self.TEMPLATES:
            return {"error": f"Template '{template}' not found"}
        
        template_config = self.TEMPLATES[template]
        
        # Use theme colors from template
        theme = template_config.get("theme", {})
        colors = {
            "primary": theme.get("primary_color", "#6366f1"),
            "secondary": theme.get("secondary_color", "#ec4899"),
            "text": theme.get("text_color", "#ffffff"),
            "background": theme.get("accent_color", "#1e293b")
        }
        
        # Intelligent Prompt Construction
        # AI "understands" the product by combining name, description, and audience
        product_name = headline
        product_desc = subheadline or ""
        target_audience = cta_text or "everyone"
        visual_style = style or "modern"
        
        # Construct a rich AI prompt for the background image
        # We describe the product in a professional setting suited for the audience
        base_prompt = f"Professional product advertisement for {product_name}. "
        if product_desc:
            base_prompt += f"Highlighting: {product_desc}. "
        
        category_desc = template_config["name"]
        background_style = theme.get("background_style", "professional studio")
        
        # Merge with user's specific context if provided
        user_context = background_prompt if background_prompt else f"elegant composition, premium feel, perfect for {target_audience}"
        
        # Final enhanced prompt for image generation
        image_prompt = (
            f"{base_prompt} "
            f"Set in a {background_style} environment. "
            f"{user_context}. "
            f"Style: {visual_style}, high-end commercial photography, bokeh background, sharp product focus."
        )
        
        # Generate AI background using image service
        from services.image_service import image_service
        
        size = f"{template_config['width']}x{template_config['height']}"
        
        background_result = await image_service.generate_image(
            prompt=image_prompt,
            size=size,
            style="banner" # Force banner style logic for aspect ratio and lighting
        )
        
        # Intelligent Text Refinement
        # If the user's description is too long, we truncate or refine for the banner
        refined_headline = product_name[:40] + ("..." if len(product_name) > 40 else "")
        refined_subheadline = product_desc[:60] + ("..." if len(product_desc) > 60 else "") if product_desc else ""
        
        # If no specific CTA text was for audience, use a default professional one
        display_cta = "Acheter Maintenant" if not cta_text or len(cta_text) > 20 else cta_text
        
        # Return banner data with text overlay metadata
        return {
            "template": template,
            "template_name": template_config["name"],
            "dimensions": {
                "width": template_config["width"],
                "height": template_config["height"]
            },
            "background_url": background_result.get("url"),
            "text_overlays": {
                "headline": {
                    "text": refined_headline,
                    "position": template_config["text_layout"]["headline"],
                    "color": colors["text"],
                    "font_weight": template_config["text_layout"]["headline"].get("font_weight", "bold")
                },
                "subheadline": {
                    "text": refined_subheadline,
                    "position": template_config["text_layout"]["subheadline"],
                    "color": colors["text"],
                    "font_weight": template_config["text_layout"]["subheadline"].get("font_weight", "normal")
                } if refined_subheadline else None,
                "cta": {
                    "text": display_cta,
                    "position": template_config["text_layout"]["cta"],
                    "color": colors["text"],
                    "background_color": colors["primary"],
                    "font_weight": template_config["text_layout"]["cta"].get("font_weight", "bold")
                }
            },
            "color_scheme": colors,
            "theme": theme,
            "provider": background_result.get("provider"),
            "enhanced_prompt": background_result.get("enhanced_prompt")
        }
    
    def get_templates(self) -> Dict[str, Any]:
        """Get all available banner templates."""
        return {
            key: {
                "name": value["name"],
                "width": value["width"],
                "height": value["height"],
                "description": value["description"]
            }
            for key, value in self.TEMPLATES.items()
        }
    
    def get_color_schemes(self) -> Dict[str, Any]:
        """Get all available color schemes."""
        return self.COLOR_SCHEMES

# Singleton instance
banner_service = BannerService()
