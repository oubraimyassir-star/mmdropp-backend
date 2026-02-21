import os
import random
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class ImageGeneratorService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("IMAGE_GENERATOR_API_KEY")
        self.demo_mode = True 

    async def generate_image(self, prompt: str, size: str = "1024x1024", style: str = "photorealistic") -> Dict[str, Any]:
        """
        Generate an image based on a prompt and style.
        """
        try:
            w, h = size.split('x')
        except:
            w, h = "1024", "1024"

        # Style Modifiers
        style_map = {
            "photorealistic": "professional studio photography, extremely detailed, 8k, sharp focus, cinematic lighting",
            "studio": "clean white background, professional product photography, soft shadows, minimalist",
            "3d_render": "octane render, unreal engine 5, 3d product mockup, volumetric lighting, vibrant",
            "minimalist": "flat design, minimalist aesthetic, clean lines, contemporary style",
            "banner": "cinematic advertising banner, wide shot, text-friendly space, high contrast",
            "modern": "modern sleek design, clean composition, contemporary aesthetic, high-end",
            "vibrant": "vibrant colors, energetic lighting, dynamic composition, saturated tones",
            "elegant": "elegant sophisticated style, soft lighting, professional lighting, graceful lines",
            "bold": "bold high-contrast design, impactful visuals, strong colors, dramatic lighting",
            "luxury": "luxury premium aesthetic, golden accents, exquisite textures, world-class photography"
        }
        
        modifier = style_map.get(style, style_map["photorealistic"])
        enhanced_prompt = f"{modifier} of {prompt}, high quality, e-commerce style, commercial intent"
        
        # Pollinations AI URL
        encoded_prompt = enhanced_prompt.replace(" ", "%20")
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={w}&height={h}&seed={random.randint(1, 100000)}&nologo=true"

        return {
            "url": image_url,
            "provider": "V3-Visual-Engine-Slab",
            "prompt": prompt,
            "enhanced_prompt": enhanced_prompt,
            "style": style,
            "size": size
        }
# Singleton instance
image_service = ImageGeneratorService()
