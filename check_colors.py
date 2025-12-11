#!/usr/bin/env python3
"""
Color Scheme Checker for TN Political Realignment Map

This script extracts and validates the color scheme used in the map,
checking for consistency, accessibility, and proper color coding.
"""

import re
import json
from collections import defaultdict

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_contrast_ratio(rgb1, rgb2):
    """Calculate WCAG contrast ratio between two RGB colors"""
    def relative_luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def extract_colors_from_html(filepath):
    """Extract color definitions from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    colors = {
        'republican': {},
        'democratic': {},
        'neutral': {},
        'other': {}
    }
    
    # Pattern to find color definitions in legend
    legend_pattern = r'<div class="legend-item"><div class="legend-color" style="background:\s*([#\w]+);"></div>(.+?)</div>'
    matches = re.findall(legend_pattern, content)
    
    for color, description in matches:
        desc_lower = description.lower()
        if 'republican' in desc_lower:
            colors['republican'][description.strip()] = color
        elif 'democratic' in desc_lower:
            colors['democratic'][description.strip()] = color
        elif 'tossup' in desc_lower:
            colors['neutral'][description.strip()] = color
        else:
            colors['other'][description.strip()] = color
    
    # Extract color definitions from JavaScript/CSS
    css_colors = re.findall(r'(?:color|background|fill):\s*([#][0-9a-fA-F]{6})', content)
    
    return colors, css_colors

def check_color_progression(colors, party):
    """Check if colors progress logically from light to dark"""
    if party not in colors or not colors[party]:
        return True, "No colors defined"
    
    # Expected order from most competitive to least
    expected_order = [
        f'Tilt {party}',
        f'Lean {party}',
        f'Likely {party}',
        f'Safe {party}',
        f'Stronghold {party}',
        f'Dominant {party}',
        f'Annihilation {party}'
    ]
    
    found_colors = []
    for category in expected_order:
        for key in colors[party]:
            if category.lower() in key.lower():
                found_colors.append((category, colors[party][key]))
                break
    
    # Check if colors get darker/more saturated
    issues = []
    for i in range(len(found_colors) - 1):
        cat1, color1 = found_colors[i]
        cat2, color2 = found_colors[i + 1]
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        # Sum of RGB values as rough brightness measure
        brightness1 = sum(rgb1)
        brightness2 = sum(rgb2)
        
        if brightness1 < brightness2:
            issues.append(f"{cat1} ({color1}) is darker than {cat2} ({color2})")
    
    return len(issues) == 0, issues

def main():
    html_file = 'New folder/index.html'
    
    print("=" * 70)
    print("TN Political Realignment Map - Color Scheme Checker")
    print("=" * 70)
    print()
    
    try:
        colors, all_css_colors = extract_colors_from_html(html_file)
    except FileNotFoundError:
        print(f"Error: Could not find {html_file}")
        return
    
    # Display extracted colors
    print("LEGEND COLORS")
    print("-" * 70)
    
    for party in ['republican', 'democratic', 'neutral']:
        if colors[party]:
            print(f"\n{party.upper()} Colors:")
            for desc, color in sorted(colors[party].items()):
                rgb = hex_to_rgb(color)
                print(f"  {desc:40} {color:8} RGB{rgb}")
    
    print("\n" + "=" * 70)
    print("COLOR VALIDATION")
    print("=" * 70)
    
    # Check Republican color progression
    print("\nRepublican Color Progression:")
    is_valid, issues = check_color_progression(colors, 'Republican')
    if is_valid:
        print("  ✓ Colors progress correctly from light to dark")
    else:
        print("  ✗ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    
    # Check Democratic color progression
    print("\nDemocratic Color Progression:")
    is_valid, issues = check_color_progression(colors, 'Democratic')
    if is_valid:
        print("  ✓ Colors progress correctly from light to dark")
    else:
        print("  ✗ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    
    # Check contrast ratios for accessibility
    print("\n" + "=" * 70)
    print("ACCESSIBILITY CHECK (WCAG Contrast Ratios)")
    print("=" * 70)
    
    # Check contrast with white background (for map)
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    print("\nContrast with White Background (map fills):")
    for party in ['republican', 'democratic']:
        if colors[party]:
            for desc, color in colors[party].items():
                rgb = hex_to_rgb(color)
                ratio = calculate_contrast_ratio(rgb, white)
                status = "✓" if ratio >= 3.0 else "✗"
                print(f"  {status} {desc:40} Ratio: {ratio:.2f}:1")
    
    print("\nContrast with Black Text:")
    for party in ['republican', 'democratic']:
        if colors[party]:
            for desc, color in colors[party].items():
                rgb = hex_to_rgb(color)
                ratio = calculate_contrast_ratio(rgb, black)
                status = "✓" if ratio >= 4.5 else "⚠" if ratio >= 3.0 else "✗"
                print(f"  {status} {desc:40} Ratio: {ratio:.2f}:1")
    
    # Color uniqueness check
    print("\n" + "=" * 70)
    print("COLOR UNIQUENESS")
    print("=" * 70)
    
    all_legend_colors = {}
    for party_colors in colors.values():
        all_legend_colors.update(party_colors)
    
    color_counts = defaultdict(list)
    for desc, color in all_legend_colors.items():
        color_counts[color].append(desc)
    
    duplicates_found = False
    for color, descs in color_counts.items():
        if len(descs) > 1:
            duplicates_found = True
            print(f"\n✗ Duplicate color {color} used for:")
            for desc in descs:
                print(f"    - {desc}")
    
    if not duplicates_found:
        print("  ✓ All legend colors are unique")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total Republican categories: {len(colors['republican'])}")
    print(f"Total Democratic categories: {len(colors['democratic'])}")
    print(f"Total Neutral categories: {len(colors['neutral'])}")
    print(f"Total unique colors in CSS: {len(set(all_css_colors))}")
    print()

if __name__ == "__main__":
    main()
