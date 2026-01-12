#!/usr/bin/env python3
"""Marketing Demo - Mockup Generator"""
import time
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    console = Console()
except ImportError:
    print("Run: pip install rich")
    sys.exit(1)

def pause(seconds=2):
    time.sleep(seconds)

def clear():
    console.clear()

# SCENE 1: Hook
clear()
console.print("\n" * 5)
console.print("[bold yellow]        SELLING ART WITHOUT LIFESTYLE PHOTOS?[/bold yellow]", justify="center")
pause(2)

# SCENE 2: Problem
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold red]BUYERS CAN'T VISUALIZE:[/bold red]

   • Flat product shots bore them
   • "How will it look in MY home?"
   • No frame reference
   • Competitors have better photos

[dim]Lifestyle mockups = 3x more sales.[/dim]
""", title="❌ Boring Photos Don't Sell", border_style="red", width=60), justify="center")
pause(3)

# SCENE 3: Solution
clear()
console.print("\n" * 3)
console.print(Panel("""
[bold green]INSTANT LIFESTYLE MOCKUPS:[/bold green]

   ✓ Drop in your artwork
   ✓ Auto-frames in 4 styles
   ✓ Places in room scenes
   ✓ Export-ready for eBay

[bold]Professional mockups in 10 seconds.[/bold]
""", title="✅ Mockup Generator", border_style="green", width=60), justify="center")
pause(3)

# SCENE 4: Demo
clear()
console.print("\n\n")
console.print("[bold cyan]              🎨 DROP YOUR ARTWORK[/bold cyan]", justify="center")
console.print()
pause(1)

console.print("[bold white]                 abstract-art.jpg[/bold white]", justify="center")
pause(2)

# SCENE 5: Generating
clear()
console.print("\n\n")
console.print("[bold magenta]              ⚡ GENERATING MOCKUPS...[/bold magenta]", justify="center")
console.print()

frames = ["Black Metal", "White Wood", "Gold Ornate", "Natural Oak"]
for frame in frames:
    console.print(f"[dim]                Creating {frame} frame...[/dim]", justify="center")
    pause(0.8)

pause(1)

# SCENE 6: Results
clear()
console.print("\n\n")
console.print("[bold green]              ✅ 4 MOCKUPS READY![/bold green]", justify="center")
console.print()

table = Table(box=box.ROUNDED, width=55)
table.add_column("File", style="cyan")
table.add_column("Frame Style", style="gold1")
table.add_column("Size", style="dim")

mockups = [
    ("mockup_black_metal.jpg", "Modern Minimal", "1600x1200"),
    ("mockup_white_wood.jpg", "Light & Airy", "1600x1200"),
    ("mockup_gold_ornate.jpg", "Classical", "1600x1200"),
    ("mockup_natural_oak.jpg", "Rustic Warm", "1600x1200"),
]

for f, style, size in mockups:
    table.add_row(f, style, size)

console.print(table, justify="center")
pause(2)

# SCENE 7: Before/After
clear()
console.print("\n\n")
console.print("[bold yellow]              📸 THE DIFFERENCE[/bold yellow]", justify="center")
console.print()

console.print(Panel("""
[red]BEFORE:[/red]  Flat artwork image

[green]AFTER:[/green]   Framed art in beautiful room
          → Buyers can VISUALIZE owning it
          → Looks professional
          → Stands out in search results
""", border_style="cyan", width=50), justify="center")
pause(3)

# SCENE 8: CTA
clear()
console.print("\n" * 4)
console.print("[bold yellow]           ⭐ MOCKUPS THAT SELL ⭐[/bold yellow]", justify="center")
console.print()
console.print("[bold white]            github.com/jjshay/mockup-generator[/bold white]", justify="center")
console.print()
console.print("[dim]                       python demo.py[/dim]", justify="center")
pause(3)
