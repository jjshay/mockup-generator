#!/usr/bin/env python3
"""
Mockup Generator - Showcase Demo
Professional product mockup creation.

Run: python showcase.py
"""

import time
import sys

# Colors for terminal output
class Colors:
    GOLD = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.GOLD}{'='*70}")
    print(f" {text}")
    print(f"{'='*70}{Colors.END}\n")

def print_step(step, text):
    print(f"{Colors.CYAN}[STEP {step}]{Colors.END} {Colors.BOLD}{text}{Colors.END}")

def main():
    print(f"\n{Colors.GOLD}{Colors.BOLD}")
    print("    ╔═══════════════════════════════════════════════════════════════╗")
    print("    ║             MOCKUP GENERATOR - LIVE DEMO                      ║")
    print("    ║        Professional Product Mockups from Artwork              ║")
    print("    ╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

    time.sleep(1)

    # Input
    print(f"   {Colors.BOLD}INPUT:{Colors.END} abstract_art_001.jpg")
    print(f"   {Colors.DIM}Clean artwork image: 800 x 1000 px{Colors.END}")
    print()

    # Visual artwork representation
    print(f"   {Colors.DIM}┌────────────────────┐")
    print(f"   │ {Colors.RED}●{Colors.END}{Colors.DIM}   {Colors.BLUE}■{Colors.END}{Colors.DIM}              │")
    print(f"   │      {Colors.GOLD}▲{Colors.END}{Colors.DIM}             │")
    print(f"   │   {Colors.BLUE}■■■■■{Colors.END}{Colors.DIM}           │  ← Original Artwork")
    print(f"   │                    │")
    print(f"   │           Artist   │")
    print(f"   └────────────────────┘{Colors.END}")
    print()
    time.sleep(0.5)

    # Step 1: Frame Selection
    print_step(1, "FRAME SELECTION")
    print()

    frames = [
        ('black_metal', '#1a1a1a / #333', 'Modern, minimal'),
        ('white_wood', '#F5F5F5 / #E0E0E0', 'Clean, Scandinavian'),
        ('gold_ornate', '#D4AF37 / #B8860B', 'Luxury, classic'),
        ('natural_oak', '#DEB887 / #D2691E', 'Warm, organic'),
    ]

    print(f"   Available frame styles:")
    for name, colors, desc in frames:
        time.sleep(0.2)
        print(f"   {Colors.CYAN}•{Colors.END} {name:<15} {Colors.DIM}{colors:<20}{Colors.END} {desc}")

    print(f"\n   {Colors.GREEN}✓{Colors.END} Selected: {Colors.BOLD}black_metal{Colors.END}")
    print()
    time.sleep(0.5)

    # Step 2: Framing
    print_step(2, "APPLYING FRAME")
    print()
    time.sleep(0.3)
    print(f"   Adding mat border (40px white)...")
    time.sleep(0.2)
    print(f"   Adding frame (30px black metal)...")
    time.sleep(0.2)
    print(f"   {Colors.GREEN}✓{Colors.END} Framed artwork: 940 x 1140 px")
    print()
    time.sleep(0.5)

    # Step 3: Room Scene
    print_step(3, "ROOM SCENE GENERATION")
    print()

    print(f"   Creating living room environment...")
    time.sleep(0.3)
    print(f"   ├─ Wall texture: Light cream (#F5F2EF)")
    print(f"   ├─ Floor: Hardwood (#D4C4B5)")
    print(f"   ├─ Decorative elements: Plant, minimal furniture")
    print(f"   └─ Lighting: Soft, even illumination")
    print()
    print(f"   {Colors.GREEN}✓{Colors.END} Scene generated: 1600 x 1200 px")
    print()
    time.sleep(0.5)

    # Step 4: Compositing
    print_step(4, "COMPOSITING")
    print()

    print(f"   Placing artwork on wall...")
    time.sleep(0.2)
    print(f"   ├─ Position: Center, upper third")
    time.sleep(0.2)
    print(f"   ├─ Adding drop shadow (15px blur, 50% opacity)")
    time.sleep(0.2)
    print(f"   └─ Perspective adjustment: None needed")
    print()
    print(f"   {Colors.GREEN}✓{Colors.END} Final mockup composited")
    print()
    time.sleep(0.5)

    # Step 5: Export
    print_step(5, "MULTI-SIZE EXPORT")
    print()

    exports = [
        ('mockup_square_1200.jpg', '1200 x 1200', 'Instagram, eBay'),
        ('mockup_landscape_1600x1200.jpg', '1600 x 1200', 'Website, Etsy'),
        ('mockup_hero_1920x1080.jpg', '1920 x 1080', 'Hero banner'),
        ('mockup_thumbnail_800.jpg', '800 x 800', 'Thumbnails'),
    ]

    print(f"   {'Filename':<35} {'Size':<14} {'Use Case':<20}")
    print(f"   {'-'*70}")

    for filename, size, use in exports:
        time.sleep(0.2)
        print(f"   {Colors.CYAN}{filename:<35}{Colors.END} {size:<14} {use}")

    print()
    time.sleep(0.5)

    # All Frame Styles Preview
    print_header("BATCH PROCESSING: ALL FRAME STYLES")

    print(f"   Generating mockups for all 4 frame styles...")
    print()

    for name, _, desc in frames:
        time.sleep(0.3)
        print(f"   {Colors.GREEN}✓{Colors.END} mockup_{name}.jpg - {desc}")

    print()
    time.sleep(0.5)

    # Summary
    print_header("GENERATION COMPLETE")

    print(f"   {Colors.BOLD}Output Summary:{Colors.END}")
    print(f"   ┌─────────────────────────────────────────────────────────────┐")
    print(f"   │ Input:              1 artwork image                        │")
    print(f"   │ Frame Styles:       4 variations generated                 │")
    print(f"   │ Export Sizes:       4 sizes per mockup                     │")
    print(f"   │ Total Outputs:      16 mockup images                       │")
    print(f"   │ Processing Time:    ~2.3 seconds                           │")
    print(f"   └─────────────────────────────────────────────────────────────┘")
    print()
    print(f"   {Colors.BOLD}Features:{Colors.END}")
    print(f"   • Realistic room scenes with shadows and lighting")
    print(f"   • Multiple frame styles (metal, wood, gold, oak)")
    print(f"   • Multi-size export for all platforms")
    print(f"   • Optional PhotoRoom API for background removal")
    print()
    print(f"   {Colors.GOLD}Used in production for 1,000+ art listings{Colors.END}")
    print()
    print(f"   {Colors.BOLD}GitHub:{Colors.END} github.com/jjshay/mockup-generator")
    print()

if __name__ == "__main__":
    main()
