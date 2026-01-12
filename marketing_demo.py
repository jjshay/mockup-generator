#!/usr/bin/env python3
"""Mockup Generator - Marketing Demo"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich import box
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

console = Console()

def pause(s=1.5):
    time.sleep(s)

def step(text):
    console.print(f"\n[bold white on #1a1a2e]  {text}  [/]\n")
    pause(0.8)

# INTRO
console.clear()
console.print()
intro = Panel(
    Align.center("[bold yellow]MOCKUP GENERATOR[/]\n\n[white]Professional Product Mockups in Seconds[/]"),
    border_style="cyan",
    width=60,
    padding=(1, 2)
)
console.print(intro)
pause(2)

# STEP 1
step("STEP 1: LOAD ARTWORK")

console.print("[dim]$[/] python mockup_generator.py [cyan]./artwork/abstract_painting.jpg[/]\n")
pause(1)

console.print("  Loading artwork..........", end="")
pause(0.5)
console.print(" [green]3000x2400 pixels[/]")

console.print("  Analyzing dimensions.....", end="")
pause(0.4)
console.print(" [green]Landscape 5:4[/]")

console.print("  Detecting edges..........", end="")
pause(0.4)
console.print(" [green]Clean borders[/]")

pause(0.8)

artwork = Panel(
    "[bold]abstract_painting.jpg[/]\n\n"
    "[dim]Dimensions:[/]  3000 x 2400\n"
    "[dim]Aspect:[/]      5:4 Landscape\n"
    "[dim]Style:[/]       Abstract / Contemporary",
    title="[cyan]Artwork Loaded[/]",
    border_style="cyan",
    width=45
)
console.print(artwork)
pause(1.5)

# STEP 2
step("STEP 2: SELECT FRAME STYLES")

frames = Table(box=box.SIMPLE, width=50)
frames.add_column("Style", style="white")
frames.add_column("Best For", style="dim")
frames.add_column("", justify="center")

frames.add_row("Black Metal", "Modern, minimalist", "[green]Selected[/]")
frames.add_row("White Wood", "Light, airy pieces", "[green]Selected[/]")
frames.add_row("Natural Oak", "Rustic themes", "[green]Selected[/]")
frames.add_row("Floating", "Gallery look", "[green]Selected[/]")

console.print(frames)
console.print("\n  [cyan]4 frame styles selected[/]")
pause(1.5)

# STEP 3
step("STEP 3: SELECT ROOM SCENES")

rooms = [
    ("Living Room", "Cozy home setting"),
    ("Modern Office", "Professional workspace"),
    ("Gallery Wall", "White gallery backdrop"),
    ("Minimal", "Plain wall background"),
]

for room, desc in rooms:
    console.print(f"  [green]>[/] [bold]{room}[/] - [dim]{desc}[/]")
    pause(0.15)

console.print("\n  [cyan]4 room scenes selected[/]")
pause(1)

# STEP 4
step("STEP 4: GENERATING MOCKUPS (4 x 4 = 16)")

console.print("  Rendering mockups...\n")
pause(0.5)

# Progress bar
for i in range(0, 101, 5):
    bar_len = int(i / 100 * 35)
    bar = "[green]" + "█" * bar_len + "[/][dim]" + "░" * (35 - bar_len) + "[/]"
    console.print(f"\r  {bar} [cyan]{i}%[/]    ", end="")
    time.sleep(0.08)

console.print("\n\n  [green]16 mockups generated[/]")
pause(1)

# STEP 5
step("STEP 5: EXPORT SIZES")

sizes = [
    ("1200x1200", "Instagram, Etsy"),
    ("1600x1200", "eBay, product page"),
    ("1920x1080", "Website banner"),
    ("800x800", "Thumbnail, email"),
]

for size, use in sizes:
    console.print(f"  [green]>[/] {size} - [dim]{use}[/]")
    pause(0.2)

console.print(f"\n  [bold]Total:[/] 16 mockups x 4 sizes = [cyan]64 images[/]")
pause(1.5)

# STEP 6
step("STEP 6: OUTPUT COMPLETE")

output = Panel(
    Align.center(
        "[bold green]MOCKUPS GENERATED[/]\n\n"
        "[bold]Output:[/] ./output/abstract_painting/\n"
        "[bold]Files:[/]  64 images + manifest\n"
        "[bold]Time:[/]   8.4 seconds"
    ),
    title="[bold yellow]COMPLETE[/]",
    border_style="green",
    width=45
)
console.print(output)
pause(2)

# FOOTER
console.print()
footer = Panel(
    Align.center(
        "[dim]Pillow + PhotoRoom API[/]\n"
        "[bold cyan]github.com/jjshay/mockup-generator[/]"
    ),
    title="[dim]Mockup Generator v1.3[/]",
    border_style="dim",
    width=50
)
console.print(footer)
pause(3)
