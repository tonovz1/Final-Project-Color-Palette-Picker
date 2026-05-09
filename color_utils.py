"""
Color theory utilities for palette generation.
Handles color space conversions and harmony calculations.
"""

import colorsys
import math


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-255 range)."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    """Convert RGB tuple to hex color string."""
    return '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))


def rgb_to_hsl(r, g, b):
    """Convert RGB (0-255) to HSL (H: 0-360, S: 0-1, L: 0-1)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s, l)


def hsl_to_rgb(h, s, l):
    """Convert HSL (H: 0-360, S: 0-1, L: 0-1) to RGB (0-255)."""
    h = h / 360.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def normalize_hue(hue):
    """Normalize hue to 0-360 range."""
    return hue % 360


def complementary(base_hex):
    """Generate complementary color (180° opposite)."""
    rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(*rgb)
    comp_h = normalize_hue(h + 180)
    comp_rgb = hsl_to_rgb(comp_h, s, l)
    return rgb_to_hex(*comp_rgb)


def analogous(base_hex):
    """Generate two analogous colors (±30° from base)."""
    rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(*rgb)
    
    colors = [base_hex]
    for offset in [30, -30]:
        new_h = normalize_hue(h + offset)
        new_rgb = hsl_to_rgb(new_h, s, l)
        colors.append(rgb_to_hex(*new_rgb))
    
    return colors


def triadic(base_hex):
    """Generate triadic colors (120° apart)."""
    rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(*rgb)
    
    colors = [base_hex]
    for offset in [120, 240]:
        new_h = normalize_hue(h + offset)
        new_rgb = hsl_to_rgb(new_h, s, l)
        colors.append(rgb_to_hex(*new_rgb))
    
    return colors


def tetradic(base_hex):
    """Generate tetradic colors (90° apart)."""
    rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(*rgb)
    
    colors = [base_hex]
    for offset in [90, 180, 270]:
        new_h = normalize_hue(h + offset)
        new_rgb = hsl_to_rgb(new_h, s, l)
        colors.append(rgb_to_hex(*new_rgb))
    
    return colors


def split_complementary(base_hex):
    """Generate split complementary colors (150° and 210° from base)."""
    rgb = hex_to_rgb(base_hex)
    h, s, l = rgb_to_hsl(*rgb)
    
    colors = [base_hex]
    for offset in [150, 210]:
        new_h = normalize_hue(h + offset)
        new_rgb = hsl_to_rgb(new_h, s, l)
        colors.append(rgb_to_hex(*new_rgb))
    
    return colors


def get_harmony_rules():
    """Return available harmony rules."""
    return {
        'Complementary': complementary,
        'Analogous': analogous,
        'Triadic': triadic,
        'Tetradic': tetradic,
        'Split Complementary': split_complementary
    }


def generate_random_palette(num_colors=5):
    """Generate a random aesthetically pleasing palette using HSL constraints."""
    import random
    
    palette = []
    
    # Generate base hue randomly
    base_hue = random.uniform(0, 360)
    
    for i in range(num_colors):
        # Vary hue with some spacing to avoid similar colors
        hue = normalize_hue(base_hue + (i * (360 / num_colors)) + random.uniform(-20, 20))
        
        # Keep saturation and lightness in pleasing ranges (avoid muddy colors)
        saturation = random.uniform(0.5, 0.9)  # Mid to high saturation
        lightness = random.uniform(0.4, 0.7)   # Mid lightness (not too dark, not too light)
        
        rgb = hsl_to_rgb(hue, saturation, lightness)
        palette.append(rgb_to_hex(*rgb))
    
    return palette


def is_valid_hex(hex_color):
    """Check if a hex color string is valid."""
    hex_color = hex_color.lstrip('#')
    return len(hex_color) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_color)


def is_valid_rgb(r, g, b):
    """Check if RGB values are valid (0-255)."""
    try:
        r, g, b = int(r), int(g), int(b)
        return 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
    except (ValueError, TypeError):
        return False
