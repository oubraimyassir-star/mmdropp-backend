from typing import Dict, Any, List, Optional, Tuple
import colorsys
import random

class ColorPaletteService:
    """
    Service for generating color palettes and extracting colors from images.
    """
    
    # Predefined theme-based palettes
    THEME_PALETTES = {
        "modern": {
            "base_hues": [210, 280, 340],  # Blue, Purple, Pink
            "saturation_range": (0.6, 0.8),
            "lightness_range": (0.4, 0.7)
        },
        "vintage": {
            "base_hues": [30, 45, 200],  # Orange, Yellow, Blue
            "saturation_range": (0.3, 0.5),
            "lightness_range": (0.5, 0.7)
        },
        "vibrant": {
            "base_hues": [0, 120, 240],  # Red, Green, Blue
            "saturation_range": (0.8, 1.0),
            "lightness_range": (0.4, 0.6)
        },
        "pastel": {
            "base_hues": [180, 300, 60],  # Cyan, Magenta, Yellow
            "saturation_range": (0.2, 0.4),
            "lightness_range": (0.7, 0.9)
        },
        "earth": {
            "base_hues": [30, 40, 120],  # Browns, Greens
            "saturation_range": (0.3, 0.6),
            "lightness_range": (0.3, 0.6)
        },
        "ocean": {
            "base_hues": [180, 200, 220],  # Blues, Teals
            "saturation_range": (0.5, 0.8),
            "lightness_range": (0.4, 0.7)
        },
        "sunset": {
            "base_hues": [0, 20, 40],  # Reds, Oranges, Yellows
            "saturation_range": (0.7, 0.9),
            "lightness_range": (0.5, 0.7)
        }
    }
    
    HARMONY_TYPES = {
        "complementary": lambda h: [(h, 1.0), ((h + 180) % 360, 1.0)],
        "analogous": lambda h: [(h, 1.0), ((h + 30) % 360, 0.8), ((h - 30) % 360, 0.8)],
        "triadic": lambda h: [(h, 1.0), ((h + 120) % 360, 1.0), ((h + 240) % 360, 1.0)],
        "tetradic": lambda h: [(h, 1.0), ((h + 90) % 360, 1.0), ((h + 180) % 360, 1.0), ((h + 270) % 360, 1.0)],
        "split_complementary": lambda h: [(h, 1.0), ((h + 150) % 360, 0.9), ((h + 210) % 360, 0.9)],
        "monochromatic": lambda h: [(h, 1.0), (h, 0.7), (h, 0.4)]
    }
    
    def __init__(self):
        pass
    
    def hsl_to_hex(self, h: float, s: float, l: float) -> str:
        """Convert HSL to hex color."""
        r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
    
    def hex_to_hsl(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex to HSL."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h * 360, s, l)
    
    def calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate WCAG contrast ratio between two colors."""
        def get_luminance(hex_color: str) -> float:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
            
            # Apply gamma correction
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        l1 = get_luminance(color1)
        l2 = get_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    async def generate_palette(
        self,
        theme: str = "modern",
        base_color: Optional[str] = None,
        harmony_type: str = "complementary",
        count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a color palette based on theme and harmony rules.
        """
        
        if base_color:
            # Use provided base color
            h, s, l = self.hex_to_hsl(base_color)
        else:
            # Generate from theme
            if theme not in self.THEME_PALETTES:
                theme = "modern"
            
            theme_config = self.THEME_PALETTES[theme]
            h = random.choice(theme_config["base_hues"])
            s = random.uniform(*theme_config["saturation_range"])
            l = random.uniform(*theme_config["lightness_range"])
        
        # Generate colors based on harmony type
        if harmony_type not in self.HARMONY_TYPES:
            harmony_type = "complementary"
        
        harmony_func = self.HARMONY_TYPES[harmony_type]
        harmony_colors = harmony_func(h)
        
        # Generate palette
        colors = []
        for hue, weight in harmony_colors[:count]:
            # Add main color
            color_hex = self.hsl_to_hex(hue, s, l)
            colors.append({
                "hex": color_hex,
                "hsl": {"h": hue, "s": s, "l": l},
                "name": self._generate_color_name(hue, s, l),
                "role": "primary" if len(colors) == 0 else "accent"
            })
            
            # Add variations if we need more colors
            if len(colors) < count:
                # Lighter variant
                lighter_hex = self.hsl_to_hex(hue, s * 0.7, min(l + 0.2, 0.9))
                colors.append({
                    "hex": lighter_hex,
                    "hsl": {"h": hue, "s": s * 0.7, "l": min(l + 0.2, 0.9)},
                    "name": self._generate_color_name(hue, s * 0.7, min(l + 0.2, 0.9)),
                    "role": "light"
                })
            
            if len(colors) >= count:
                break
        
        # Ensure we have exactly 'count' colors
        colors = colors[:count]
        
        # Calculate accessibility
        contrast_with_white = self.calculate_contrast_ratio(colors[0]["hex"], "#ffffff")
        contrast_with_black = self.calculate_contrast_ratio(colors[0]["hex"], "#000000")
        
        return {
            "theme": theme,
            "harmony_type": harmony_type,
            "colors": colors,
            "accessibility": {
                "contrast_white": round(contrast_with_white, 2),
                "contrast_black": round(contrast_with_black, 2),
                "wcag_aa_large": contrast_with_white >= 3.0 or contrast_with_black >= 3.0,
                "wcag_aa_normal": contrast_with_white >= 4.5 or contrast_with_black >= 4.5,
                "wcag_aaa": contrast_with_white >= 7.0 or contrast_with_black >= 7.0
            },
            "exports": self._generate_exports(colors)
        }
    
    def _generate_color_name(self, h: float, s: float, l: float) -> str:
        """Generate a descriptive name for a color."""
        hue_names = {
            (0, 30): "Red",
            (30, 60): "Orange",
            (60, 90): "Yellow",
            (90, 150): "Green",
            (150, 210): "Cyan",
            (210, 270): "Blue",
            (270, 330): "Purple",
            (330, 360): "Pink"
        }
        
        hue_name = "Gray"
        for (start, end), name in hue_names.items():
            if start <= h < end:
                hue_name = name
                break
        
        if l > 0.7:
            prefix = "Light"
        elif l < 0.3:
            prefix = "Dark"
        else:
            prefix = ""
        
        if s < 0.2:
            return f"{prefix} Gray".strip()
        
        return f"{prefix} {hue_name}".strip()
    
    def _generate_exports(self, colors: List[Dict]) -> Dict[str, str]:
        """Generate export formats for the palette."""
        
        # CSS Variables
        css_vars = ":root {\n"
        for i, color in enumerate(colors):
            css_vars += f"  --color-{color['role']}-{i+1}: {color['hex']};\n"
        css_vars += "}"
        
        # Tailwind Config
        tailwind = "module.exports = {\n  theme: {\n    extend: {\n      colors: {\n"
        for i, color in enumerate(colors):
            tailwind += f"        '{color['role']}-{i+1}': '{color['hex']}',\n"
        tailwind += "      }\n    }\n  }\n}"
        
        # JSON
        json_export = "{\n"
        for i, color in enumerate(colors):
            json_export += f'  "{color["role"]}-{i+1}": "{color["hex"]}",\n'
        json_export = json_export.rstrip(",\n") + "\n}"
        
        return {
            "css": css_vars,
            "tailwind": tailwind,
            "json": json_export
        }
    
    def get_themes(self) -> List[str]:
        """Get all available themes."""
        return list(self.THEME_PALETTES.keys())
    
    def get_harmony_types(self) -> List[str]:
        """Get all available harmony types."""
        return list(self.HARMONY_TYPES.keys())

# Singleton instance
color_palette_service = ColorPaletteService()
